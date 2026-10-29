"""
Medication Data Analysis and Validation

This script uses Pandas to analyze the medication data extracted from the DailyMed
XML files.

What the file includes:
- checking dimensions of the dataset
- reviewing the extracted medication fields
- identifying missing values
- previewing medication records
- searching for specific medications

These specific steps evaluate the extracted data to determine if it contains all the relevant information for feature development.
"""

import pandas as pd

# Loading the extracted medication data
df = pd.read_csv("data/sample_medications.csv")

# dimensions of the dataset 
# total number of medication records and columns 
print("Dataset Dimensions:")
print(df.shape)

# column names
# medication fields that were extracted
print("\nDataset Columns:")
print(df.columns.tolist())

# Check for missing values
# Replaces empty strings and whitespace with missing value markers
df = df.replace(r'^\s*$', pd.NA, regex=True)

# counts missing values in each column
print("\nMissing Values:")
print(df.isna().sum())

# viewing first 10 medication records
print("\nFirst 10 Medication Records:")
print(df.head(10).to_string(index=False))

# searching for specific medication
# checks if FANAPT (a medication) appears in medication data
print("\nFANAPT Records:")
print(
    df[df["brand_names"].str.contains(
        "FANAPT", case=False, na=False
    )].to_string(index=False)
)