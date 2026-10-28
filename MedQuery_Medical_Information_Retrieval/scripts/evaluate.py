"""
scripts/evaluate.py
Executes standard IR evaluation across TF-IDF, BM25, Semantic (SBERT), and Hybrid retrievers
using ground-truth queries in data/evaluation_queries.csv.
Saves results/evaluation_results.csv and results/evaluation_comparison.png.
"""

import os
import sys
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.indexing.indexer import MedicalIndexer
from src.retrieval.tfidf_retriever import TfidfRetriever
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.semantic_retriever import SemanticRetriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.evaluation.evaluator import IREvaluator


def run_benchmark():
    print("=" * 65)
    print(" MedQuery Information Retrieval Benchmark & Evaluation ")
    print("=" * 65)

    eval_queries_path = "data/evaluation_queries.csv"
    if not os.path.exists(eval_queries_path):
        raise FileNotFoundError(f"Evaluation dataset {eval_queries_path} not found.")

    queries_df = pd.read_csv(eval_queries_path, encoding="utf-8")
    queries = queries_df.to_dict(orient="records")
    print(f"Loaded {len(queries)} evaluation queries.")

    # Load search indexes
    indexer = MedicalIndexer(index_dir="indexes", sbert_model_name="all-MiniLM-L6-v2")
    if not indexer.load():
        print("Indexes not found. Building indexes first...")
        from scripts.build_index import main as build_index_main
        build_index_main()
        indexer.load()

    retrievers = {
        "tfidf": TfidfRetriever(indexer),
        "bm25": BM25Retriever(indexer),
        "semantic": SemanticRetriever(indexer),
        "hybrid": HybridRetriever(indexer, bm25_weight=0.5, semantic_weight=0.5)
    }

    results_list = []
    query_details_all = {}

    for name, retriever in retrievers.items():
        print(f"\nEvaluating retriever: {name.upper()}...")
        eval_output = IREvaluator.evaluate_retriever_on_queries(
            retriever,
            queries,
            method_name=name,
            k_values=[5, 10]
        )
        summary = eval_output["summary"]
        results_list.append(summary)
        query_details_all[name] = eval_output["query_details"]

    results_df = pd.DataFrame(results_list)

    # Format numbers for clean display
    display_df = results_df[[
        "method", "precision@5", "recall@5", "f1@5", "precision@10", "recall@10", "f1@10", "map", "mrr", "ndcg@5"
    ]].copy()

    for col in display_df.columns:
        if col != "method":
            display_df[col] = display_df[col].apply(lambda v: f"{v:.4f}")

    print("\n" + "=" * 65)
    print(" EVALUATION RESULTS TABLE ")
    print("=" * 65)
    print(display_df.to_string(index=False))
    print("=" * 65)

    # Save to CSV
    os.makedirs("results", exist_ok=True)
    out_csv = "results/evaluation_results.csv"
    results_df.to_csv(out_csv, index=False)
    print(f"\nDetailed evaluation results saved to: {out_csv}")

    # Generate Chart
    out_chart = "results/evaluation_comparison.png"
    IREvaluator.generate_comparison_chart(results_df, out_chart)
    print("Benchmark complete!\n")

    return results_df


if __name__ == "__main__":
    run_benchmark()
