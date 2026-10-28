"""
scripts/preprocess.py
Preprocesses the cleaned dataset and extracts chunks for indexing.
Saves data/chunked_medical_documents.csv.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.preprocessing.chunker import DocumentChunker

def preprocess_and_chunk(
    input_path: str = "data/processed_medical_documents.csv",
    output_path: str = "data/chunked_medical_documents.csv"
) -> pd.DataFrame:
    print(f"Reading processed documents from {input_path}...")
    if not os.path.exists(input_path):
        from scripts.load_dataset import load_and_process_dataset
        load_and_process_dataset()

    df = pd.read_csv(input_path, encoding="utf-8")
    all_chunks = []
    for _, row in df.iterrows():
        doc_dict = row.to_dict()
        chunks = DocumentChunker.chunk_structured_document(doc_dict)
        all_chunks.extend(chunks)

    chunk_df = pd.DataFrame(all_chunks)
    chunk_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Generated {len(chunk_df)} chunks from {len(df)} documents. Saved to {output_path}.")
    return chunk_df

if __name__ == "__main__":
    preprocess_and_chunk()
