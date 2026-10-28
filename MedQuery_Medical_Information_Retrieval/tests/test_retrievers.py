"""
Unit and integration tests for IR retrievers (TF-IDF, BM25, Semantic, Hybrid)
and edge cases.
"""

import pytest
import os
from src.indexing.indexer import MedicalIndexer
from src.retrieval.tfidf_retriever import TfidfRetriever
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.semantic_retriever import SemanticRetriever
from src.retrieval.hybrid_retriever import HybridRetriever


@pytest.fixture(scope="module")
def indexer():
    idx = MedicalIndexer(index_dir="indexes")
    assert idx.load() is True
    return idx


def test_empty_query(indexer):
    hybrid = HybridRetriever(indexer)
    res = hybrid.retrieve("")
    assert res == []

    bm25 = BM25Retriever(indexer)
    assert bm25.retrieve("   ") == []

    tfidf = TfidfRetriever(indexer)
    assert tfidf.retrieve("") == []

    sem = SemanticRetriever(indexer)
    assert sem.retrieve("") == []


def test_short_query(indexer):
    hybrid = HybridRetriever(indexer)
    res = hybrid.retrieve("flu", top_k=3)
    assert len(res) <= 3
    assert any("influenza" in r["title"].lower() or "cold" in r["title"].lower() for r in res)


def test_long_query(indexer):
    long_q = "A middle aged patient presents with chronic cough lasting three weeks with night sweats, weight loss and hemoptysis. What infectious etiology is suspected?"
    hybrid = HybridRetriever(indexer)
    res = hybrid.retrieve(long_q, top_k=5)
    assert len(res) > 0
    top_doc = res[0]
    assert "tuberculosis" in top_doc["title"].lower() or "tuberculosis" in top_doc["disease"].lower()


def test_unknown_medical_term(indexer):
    unknown_q = "xyznonexistentpathology9999"
    hybrid = HybridRetriever(indexer)
    res = hybrid.retrieve(unknown_q, top_k=5)
    # Should not crash; SBERT produces low semantic similarity, BM25 produces 0
    assert isinstance(res, list)


def test_spelling_variation(indexer):
    query = "diabtes mellitus high blood sugar"
    sem = SemanticRetriever(indexer)
    res = sem.retrieve(query, top_k=5)
    assert len(res) > 0
    assert any("diabetes" in r["title"].lower() for r in res)


def test_disease_name_query(indexer):
    query = "Hypertension"
    bm25 = BM25Retriever(indexer)
    res = bm25.retrieve(query, top_k=5)
    assert len(res) > 0
    assert "hypertension" in res[0]["title"].lower() or "hypertension" in res[0]["disease"].lower()


def test_symptom_query(indexer):
    query = "substernal chest pain radiating to left arm diaphoresis dyspnea"
    hybrid = HybridRetriever(indexer)
    res = hybrid.retrieve(query, top_k=5)
    assert len(res) > 0
    top_titles = [r["title"].lower() for r in res]
    assert any("coronary" in t or "heart" in t or "infarction" in t for t in top_titles)


def test_treatment_query(indexer):
    query = "What antibiotics are used to treat community acquired pneumonia?"
    hybrid = HybridRetriever(indexer)
    res = hybrid.retrieve(query, top_k=5)
    assert len(res) > 0
    assert any("pneumonia" in r["title"].lower() for r in res)


def test_prevention_query(indexer):
    query = "How to prevent dengue fever and mosquito breeding?"
    bm25 = BM25Retriever(indexer)
    res = bm25.retrieve(query, top_k=5)
    assert len(res) > 0
    assert any("dengue" in r["title"].lower() for r in res)


def test_category_filtering(indexer):
    query = "treatment and causes"
    hybrid = HybridRetriever(indexer)
    res = hybrid.retrieve(query, top_k=5, category_filter="Cardiovascular")
    for r in res:
        assert r["category"] == "Cardiovascular"


def test_top_k_changes(indexer):
    hybrid = HybridRetriever(indexer)
    res_1 = hybrid.retrieve("asthma triggers", top_k=1)
    res_3 = hybrid.retrieve("asthma triggers", top_k=3)
    res_8 = hybrid.retrieve("asthma triggers", top_k=8)

    assert len(res_1) == 1
    assert len(res_3) == 3
    assert len(res_8) == 8


def test_hybrid_configurable_weights(indexer):
    query = "vitamin d deficiency and bone pain"
    hybrid = HybridRetriever(indexer)
    res_bm25_heavy = hybrid.retrieve(query, top_k=3, bm25_weight=0.8, semantic_weight=0.2)
    res_sem_heavy = hybrid.retrieve(query, top_k=3, bm25_weight=0.2, semantic_weight=0.8)

    assert len(res_bm25_heavy) == 3
    assert len(res_sem_heavy) == 3
    assert res_bm25_heavy[0]["bm25_weight"] == 0.8
    assert res_sem_heavy[0]["semantic_weight"] == 0.8
