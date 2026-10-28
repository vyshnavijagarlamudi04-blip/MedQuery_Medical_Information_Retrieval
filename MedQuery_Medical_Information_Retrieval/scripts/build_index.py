"""
scripts/build_index.py
Builds TF-IDF, BM25, and Sentence-BERT indexes from chunked documents
and persists them to the indexes/ directory.
"""

import os
import sys
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.indexing.indexer import MedicalIndexer
from src.preprocessing.chunker import DocumentChunker

def main():
    print("=" * 60)
    print(" MedQuery Index Builder ")
    print("=" * 60)

    chunk_file = "data/chunked_medical_documents.csv"
    if not os.path.exists(chunk_file):
        print(f"Chunked dataset {chunk_file} not found. Running preprocessor...")
        from scripts.preprocess import preprocess_and_chunk
        preprocess_and_chunk()

    print(f"Loading chunks from {chunk_file}...")
    df = pd.read_csv(chunk_file, encoding="utf-8")
    chunks = df.to_dict(orient="records")
    print(f"Loaded {len(chunks)} chunks.")

    indexer = MedicalIndexer(index_dir="indexes", sbert_model_name="all-MiniLM-L6-v2")
    indexer.build_indexes(chunks, force_sbert_rebuild=False)
    indexer.save()

    print("\nIndex verification:")
    print(f"  - Total indexed passages: {len(indexer.chunks)}")
    print(f"  - Unique documents: {len(set(c['document_id'] for c in indexer.chunks))}")
    print(f"  - TF-IDF vocabulary size: {len(indexer.tfidf_vectorizer.vocabulary_)}")
    print(f"  - SBERT embeddings shape: {indexer.sbert_embeddings.shape}")
    print("Index build finished successfully!\n")

if __name__ == "__main__":
    main()
