#!/usr/bin/env python3

import argparse
import csv
import io
import re
import zipfile
from pathlib import Path

from lxml import etree


NAMESPACE = {"v3": "urn:hl7-org:v3"}

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
]

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
        "//*[local-name()='ingredient'][@classCode='ACTIB']"
        "//*[local-name()='ingredientSubstance']"
        "/*[local-name()='name']/text()"
    )

    # Manufacturer / labeler
    manufacturers = root.xpath(
        "//*[local-name()='representedOrganization']"
        "/*[local-name()='name']/text()"
    )

    # LOINC section codes
    dosage = get_section_text(root, "34068-7")
    interactions = get_section_text(root, "34073-7")

    return {
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
    }


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

    args = parser.parse_args()

    input_path = Path(args.input_zip)
    output_path = Path(args.output_csv)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return

    if not zipfile.is_zipfile(input_path):
        print("The input file is not a valid ZIP file.")
        return

    total = 0
    errors = 0

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=FIELDS
        )

        writer.writeheader()

        for xml_data, source_file in iter_zip(
            input_path,
            input_path.name
        ):
            try:
                medication = extract_medication(
                    xml_data,
                    source_file
                )

                writer.writerow(medication)
                total += 1

                if total % 500 == 0:
                    print(f"Processed {total} medication labels...")

            except etree.XMLSyntaxError as error:
                errors += 1

                if errors <= 5:
                    print(f"XML error in {source_file}: {error}")

            except Exception as error:
                errors += 1
                print(f"Error processing {source_file}: {error}")

    print("\nExtraction complete!")
    print(f"Medication labels processed: {total}")
    print(f"Files with errors: {errors}")
    print(f"CSV saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()