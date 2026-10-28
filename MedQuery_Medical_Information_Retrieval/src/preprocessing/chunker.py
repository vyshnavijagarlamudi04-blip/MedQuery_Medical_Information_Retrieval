"""
Document Chunking for Medical Information Retrieval.
Splits documents into coherent passages or chunks while preserving semantic integrity.
"""

from typing import List, Dict, Any
import nltk
from .cleaner import clean_text

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)

from nltk.tokenize import sent_tokenize


class DocumentChunker:
    """Handles splitting structured and unstructured medical documents into passages."""

    @staticmethod
    def chunk_structured_document(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunks a structured medical record into 3 distinct, high-relevance semantic passages:
        1. Overview & Pathophysiology (content + title)
        2. Symptoms, Signs & Causes (symptoms + causes)
        3. Treatment, Management & Prevention (treatment + prevention)
        """
        doc_id = doc.get("document_id", "DOC_UNKNOWN")
        title = doc.get("title", "")
        category = doc.get("category", "")
        disease = doc.get("disease", "")
        source = doc.get("source", "")
        
        chunks = []

        # Chunk 1: Comprehensive Overview & Clinical Discussion
        content_text = doc.get("content", "").strip()
        if content_text:
            text_1 = f"{title}. Disease: {disease}. {content_text}"
            chunks.append({
                "chunk_id": f"{doc_id}_c1",
                "document_id": doc_id,
                "title": title,
                "category": category,
                "disease": disease,
                "source": source,
                "section": "Overview & Pathophysiology",
                "chunk_text": text_1,
                "clean_chunk_text": clean_text(text_1)
            })

        # Chunk 2: Symptoms, Signs and Causes
        symptoms = doc.get("symptoms", "").strip()
        causes = doc.get("causes", "").strip()
        if symptoms or causes:
            parts = []
            if symptoms:
                parts.append(f"Symptoms and Signs: {symptoms}")
            if causes:
                parts.append(f"Causes and Etiology: {causes}")
            text_2 = f"{title} ({disease}). " + " ".join(parts)
            chunks.append({
                "chunk_id": f"{doc_id}_c2",
                "document_id": doc_id,
                "title": title,
                "category": category,
                "disease": disease,
                "source": source,
                "section": "Symptoms & Causes",
                "chunk_text": text_2,
                "clean_chunk_text": clean_text(text_2)
            })

        # Chunk 3: Treatment and Prevention
        treatment = doc.get("treatment", "").strip()
        prevention = doc.get("prevention", "").strip()
        if treatment or prevention:
            parts = []
            if treatment:
                parts.append(f"Treatment and Clinical Management: {treatment}")
            if prevention:
                parts.append(f"Prevention and Lifestyle Recommendations: {prevention}")
            text_3 = f"{title} ({disease}). " + " ".join(parts)
            chunks.append({
                "chunk_id": f"{doc_id}_c3",
                "document_id": doc_id,
                "title": title,
                "category": category,
                "disease": disease,
                "source": source,
                "section": "Treatment & Prevention",
                "chunk_text": text_3,
                "clean_chunk_text": clean_text(text_3)
            })

        return chunks

    @staticmethod
    def chunk_free_text(
        text: str,
        doc_id: str,
        title: str = "",
        category: str = "General",
        disease: str = "",
        source: str = "Uploaded Document",
        max_words: int = 150,
        overlap_sentences: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Splits arbitrary unstructured free text into passages by sentence boundaries,
        ensuring sentences are never split in half.
        """
        if not text or not text.strip():
            return []

        try:
            sentences = sent_tokenize(text.strip())
        except Exception:
            # Fallback if punkt tokenizer encounters unexpected formatting
            sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]

        chunks = []
        current_sentences = []
        current_word_count = 0
        chunk_idx = 1

        for sent in sentences:
            sent_words = len(sent.split())
            if current_word_count + sent_words > max_words and current_sentences:
                chunk_passage = " ".join(current_sentences)
                chunks.append({
                    "chunk_id": f"{doc_id}_c{chunk_idx}",
                    "document_id": doc_id,
                    "title": title or f"Document {doc_id}",
                    "category": category,
                    "disease": disease or title,
                    "source": source,
                    "section": f"Passage {chunk_idx}",
                    "chunk_text": chunk_passage,
                    "clean_chunk_text": clean_text(chunk_passage)
                })
                chunk_idx += 1
                # Retain overlap sentences
                current_sentences = current_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
                current_word_count = sum(len(s.split()) for s in current_sentences)

            current_sentences.append(sent)
            current_word_count += sent_words

        if current_sentences:
            chunk_passage = " ".join(current_sentences)
            chunks.append({
                "chunk_id": f"{doc_id}_c{chunk_idx}",
                "document_id": doc_id,
                "title": title or f"Document {doc_id}",
                "category": category,
                "disease": disease or title,
                "source": source,
                "section": f"Passage {chunk_idx}",
                "chunk_text": chunk_passage,
                "clean_chunk_text": clean_text(chunk_passage)
            })

        return chunks
