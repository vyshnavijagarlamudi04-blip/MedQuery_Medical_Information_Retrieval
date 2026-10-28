"""
scripts/load_dataset.py
Loads data/medical_documents.csv, validates columns, removes empty/duplicate documents,
normalizes text fields, and saves data/processed_medical_documents.csv.
"""

import os
import sys
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.preprocessing.cleaner import clean_text

REQUIRED_COLUMNS = [
    "document_id", "title", "category", "disease", "symptoms",
    "causes", "treatment", "prevention", "content", "source"
]

def load_and_process_dataset(
    raw_path: str = "data/medical_documents.csv",
    output_path: str = "data/processed_medical_documents.csv"
) -> pd.DataFrame:
    print(f"Loading raw dataset from {raw_path}...")
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw dataset file not found at {raw_path}. Run generate_datasets.py first.")

    df = pd.read_csv(raw_path, encoding="utf-8")
    initial_count = len(df)
    print(f"Loaded {initial_count} raw documents.")

    # 1. Validate required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    # 2. Remove empty documents (where title or content is null/empty)
    df = df.dropna(subset=["title", "content"])
    df = df[df["title"].str.strip() != ""]
    df = df[df["content"].str.strip() != ""]
    print(f"After removing empty documents: {len(df)} documents remaining.")

    # 3. Remove duplicate documents (by document_id and title)
    df = df.drop_duplicates(subset=["document_id"])
    df = df.drop_duplicates(subset=["title"])
    print(f"After removing duplicates: {len(df)} documents remaining.")

    # 4. Normalize text fields while keeping original text intact
    # We clean whitespace, symbols, and create a normalized representation
    for col in ["title", "category", "disease", "symptoms", "causes", "treatment", "prevention", "content", "source"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Create a unified processed_content column for indexing baseline
    df["processed_text"] = df.apply(
        lambda row: clean_text(
            f"{row['title']} {row['disease']} {row['category']} {row['symptoms']} {row['causes']} {row['treatment']} {row['prevention']} {row['content']}"
        ),
        axis=1
    )

    # 5. Save cleaned processed dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Cleaned dataset saved successfully to {output_path} with {len(df)} documents.")
    return df

if __name__ == "__main__":
    load_and_process_dataset()
