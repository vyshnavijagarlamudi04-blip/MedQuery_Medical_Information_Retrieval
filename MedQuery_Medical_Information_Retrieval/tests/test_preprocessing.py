"""
Tests for text preprocessing, cleaning, tokenization, and chunking.
"""

import pytest
from src.preprocessing.cleaner import TextCleaner, clean_text, tokenize
from src.preprocessing.chunker import DocumentChunker


def test_clean_text_normalizes_whitespace():
    raw = "  Type 2   diabetes   mellitus \n\t has hyperglycemia.   "
    cleaned = clean_text(raw)
    assert cleaned == "type 2 diabetes mellitus has hyperglycemia."


def test_medical_terms_preservation():
    raw = "Patient with SARS-CoV-2, H1N1, Vitamin B12 deficiency and acute Type-2 diabetes."
    tokens = tokenize(raw, lowercase=True)
    assert "sars-cov-2" in tokens or "sars" in tokens
    assert "b12" in tokens
    assert "type-2" in tokens or ("type" in tokens and "2" in tokens)


def test_stopwords_preserve_negation_and_critical_terms():
    # 'not', 'no', 'without', 'acute' should be retained
    raw = "acute condition without diabetes and not responding"
    tokens = tokenize(raw, remove_stopwords=True)
    assert "acute" in tokens
    assert "not" in tokens or "without" in tokens


def test_document_chunker_structured():
    doc = {
        "document_id": "DOC_TEST_01",
        "title": "Test Bronchitis",
        "category": "Respiratory",
        "disease": "Acute Bronchitis",
        "symptoms": "Cough and sputum",
        "causes": "Viral infection",
        "treatment": "Rest and fluids",
        "prevention": "Hand hygiene",
        "content": "Bronchitis is inflammation of the bronchial tubes.",
        "source": "WHO"
    }
    chunks = DocumentChunker.chunk_structured_document(doc)
    assert len(chunks) == 3
    assert chunks[0]["chunk_id"] == "DOC_TEST_01_c1"
    assert "Overview" in chunks[0]["section"]
    assert chunks[1]["chunk_id"] == "DOC_TEST_01_c2"
    assert chunks[2]["chunk_id"] == "DOC_TEST_01_c3"


def test_document_chunker_free_text():
    text = "Sentence one about health. Sentence two about vitamins. Sentence three about cardiology. Sentence four about recovery."
    chunks = DocumentChunker.chunk_free_text(
        text,
        doc_id="DOC_FREE_01",
        title="Free Doc",
        max_words=10,
        overlap_sentences=1
    )
    assert len(chunks) >= 2
    for c in chunks:
        assert len(c["chunk_text"]) > 0
