#!/usr/bin/env python3
"""
Extract medication information from DailyMed ZIP files.

This is the original script with only two additions (marked NEW):
  1. An "adverse_reactions" column (side effects) in the medications CSV.
  2. A second CSV with one row per NDC code, linked to set_id
     (named <output name>_ndcs.csv, saved next to the medications CSV).

Everything else works exactly as before.

Usage:
  python extract_medications_v3.py INPUT.zip OUTPUT.csv
  python extract_medications_v3.py INPUT.zip OUTPUT.csv --limit 500   # quick test
"""

import argparse
import csv
import io
import re
import zipfile
from pathlib import Path

from lxml import etree


NAMESPACE = {"v3": "urn:hl7-org:v3"}

# Original columns first, in the original order. New columns go at the end.
FIELDS = [
    "set_id",
    "version",
    "effective_date",
    "title",
    "brand_names",
    "generic_names",
    "active_ingredients",
    "manufacturer",
    "dosage_and_administration",
    "drug_interactions",
    "source_file",
    "adverse_reactions",  # NEW
    "indications_and_usage" ##review if we can find
]

# NEW: columns for the NDC file
NDC_FIELDS = ["set_id", "ndc", "ndc_digits"]

# NEW: code system ID used for NDCs inside DailyMed files
# (verify against one real XML file if the NDC file comes out empty)
NDC_CODE_SYSTEM = "2.16.840.1.113883.6.69"

PARSER = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    huge_tree=True
)


def clean_text(text):
    """Clean up whitespace in extracted text."""
    return re.sub(r"\s+", " ", text or "").strip()


def element_text(element):
    """Extract readable text from an XML element and its children."""
    if element is None:
        return ""

    return clean_text(" ".join(element.itertext()))


def unique(values):
    """Remove duplicate values while keeping their original order."""
    results = []

    for value in values:
        value = clean_text(value)

        if value and value not in results:
            results.append(value)

    return results


def get_section_text(root, loinc_code):
    """Find a section using its LOINC code."""
    sections = root.xpath(
        ".//v3:section[v3:code/@code=$code]",
        namespaces=NAMESPACE,
        code=loinc_code
    )

    return unique([element_text(section) for section in sections])


def normalize_ndc(ndc):
    """NEW: Turn an NDC like 1234-5678-90 into digits (padded to 5-4-2)."""
    parts = ndc.split("-")

    if len(parts) == 3:
        return parts[0].zfill(5) + parts[1].zfill(4) + parts[2].zfill(2)

    if len(parts) == 2:
        return parts[0].zfill(5) + parts[1].zfill(4)

    return re.sub(r"\D", "", ndc)


def get_ndcs(root, set_id):
    """NEW: Find every NDC code in the label, linked to its set_id."""
    codes = root.xpath(
        "//*[local-name()='code'][@codeSystem=$system]/@code",
        system=NDC_CODE_SYSTEM
    )

    return [
        {
            "set_id": set_id,
            "ndc": ndc,
            "ndc_digits": normalize_ndc(ndc),
        }
        for ndc in unique(codes)
    ]


def extract_medication(xml_data, source_file):
    """Extract medication information from one SPL XML file."""
    root = etree.fromstring(xml_data, parser=PARSER)

    set_id = root.xpath(
        "string(./v3:setId/@root)",
        namespaces=NAMESPACE
    )

    version = root.xpath(
        "string(./v3:versionNumber/@value)",
        namespaces=NAMESPACE
    )

    effective_date = root.xpath(
        "string(./v3:effectiveTime/@value)",
        namespaces=NAMESPACE
    )

    title = root.xpath(
        "string(./v3:title)",
        namespaces=NAMESPACE
    )

    # Brand/product names
    brand_names = root.xpath(
        "//*[local-name()='manufacturedProduct']"
        "/*[local-name()='name']/text()"
    )

    # Generic medication names
    generic_names = root.xpath(
        "//*[local-name()='genericMedicine']"
        "/*[local-name()='name']/text()"
    )

    # Active ingredients
    ingredients = root.xpath(
        "//*[local-name()='ingredient'][starts-with(@classCode, 'ACTI')]"
        "//*[local-name()='ingredientSubstance']"
        "/*[local-name()='name']/text()"
    )

    #if we can't identify the proper active ingredients 
    if not unique(ingredients):
        ingredients = generic_names

    # Manufacturer / labeler
    manufacturers = root.xpath(
        "//*[local-name()='representedOrganization']"
        "/*[local-name()='name']/text()"
    )

    # LOINC section codes
    dosage = get_section_text(root, "34068-7")
    interactions = get_section_text(root, "34073-7")
    adverse_reactions = get_section_text(root, "34084-4") 
    indications = get_section_text(root, "34067-9") # NEW

    medication = {
        "set_id": clean_text(set_id),
        "version": clean_text(version),
        "effective_date": clean_text(effective_date),
        "title": clean_text(title),
        "brand_names": "; ".join(unique(brand_names)),
        "generic_names": "; ".join(unique(generic_names)),
        "active_ingredients": "; ".join(unique(ingredients)),
        "manufacturer": "; ".join(unique(manufacturers)),
        "dosage_and_administration": " ".join(dosage),
        "drug_interactions": " ".join(interactions),
        "source_file": source_file,
        "adverse_reactions": " ".join(adverse_reactions),  # NEW
        "indications_and_usage":"".join(indications),#review if we can find
    }

    # NEW: NDC rows for the second file
    ndc_rows = get_ndcs(root, clean_text(set_id))

    return medication, ndc_rows


def iter_zip(zip_file, source_name=""):
    """Read XML files from a ZIP and recursively open nested ZIP files."""
    try:
        with zipfile.ZipFile(zip_file) as archive:

            for info in archive.infolist():
                name = info.filename
                lower_name = name.lower()

                # Skip Mac metadata files and folders
                if "__macosx" in lower_name or name.startswith("._"):
                    continue

                if info.is_dir():
                    continue

                if lower_name.endswith(".xml"):
                    try:
                        xml_data = archive.read(info)
                        yield xml_data, f"{source_name}/{name}"

                    except Exception as error:
                        print(f"Could not read {name}: {error}")

                elif lower_name.endswith(".zip"):
                    try:
                        nested_data = archive.read(info)

                        yield from iter_zip(
                            io.BytesIO(nested_data),
                            f"{source_name}/{name}"
                        )

                    except zipfile.BadZipFile:
                        print(f"Skipping invalid ZIP: {name}")

    except zipfile.BadZipFile:
        print(f"Skipping invalid ZIP: {source_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract medication information from DailyMed ZIP files."
    )

    parser.add_argument("input_zip", help="Main ZIP file")
    parser.add_argument("output_csv", help="Output CSV file")

    # NEW: optional, for quick tests
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Stop after this many labels (0 = no limit)"
    )

    args = parser.parse_args()

    input_path = Path(args.input_zip)
    output_path = Path(args.output_csv)

    # NEW: the NDC file is saved next to the main CSV
    ndc_path = output_path.with_name(output_path.stem + "_ndcs.csv")

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    if not zipfile.is_zipfile(input_path):
        print("The input file is not a valid ZIP file.")
        return

    # NEW: create the output folder (e.g. data/) if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    errors = 0
    ndc_total = 0

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file, ndc_path.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as ndc_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=FIELDS
        )

        ndc_writer = csv.DictWriter(
            ndc_file,
            fieldnames=NDC_FIELDS
        )

        writer.writeheader()
        ndc_writer.writeheader()

        for xml_data, source_file in iter_zip(
            input_path,
            input_path.name
        ):
            try:
                medication, ndc_rows = extract_medication(
                    xml_data,
                    source_file
                )

                writer.writerow(medication)
                ndc_writer.writerows(ndc_rows)  # NEW

                total += 1
                ndc_total += len(ndc_rows)

                if total % 500 == 0:
                    print(f"Processed {total} medication labels...")

                # NEW: stop early if --limit was given
                if args.limit and total >= args.limit:
                    print(f"Reached --limit of {args.limit} labels.")
                    break

            except etree.XMLSyntaxError as error:
                errors += 1

                if errors <= 5:
                    print(f"XML error in {source_file}: {error}")

            except Exception as error:
                errors += 1
                print(f"Error processing {source_file}: {error}")

    print("\nExtraction complete!")
    print(f"Medication labels processed: {total}")
    print(f"NDC rows written: {ndc_total}")
    print(f"Files with errors: {errors}")
    print(f"CSV saved to: {output_path.resolve()}")
    print(f"NDC CSV saved to: {ndc_path.resolve()}")


if __name__ == "__main__":
    main()
