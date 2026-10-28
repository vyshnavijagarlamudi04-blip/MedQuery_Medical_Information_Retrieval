"""
Text Cleaning and Tokenization for Medical Information Retrieval.
Preserves vital medical acronyms, hyphenated terms, numbers, and disease markers.
"""

import re
import unicodedata
from typing import List, Set
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are loaded
try:
    NLTK_STOPWORDS: Set[str] = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    NLTK_STOPWORDS = set(stopwords.words("english"))

# Medical terms that should NEVER be stripped by stopword filtering
MEDICAL_PRESERVED_WORDS = {
    "no", "not", "type", "stage", "all", "more", "most", "over", "under",
    "between", "without", "with", "against", "high", "low", "acute", "chronic"
}

# Effective stopword list tailored for medical information retrieval
SAFE_STOPWORDS = NLTK_STOPWORDS - MEDICAL_PRESERVED_WORDS


class TextCleaner:
    """Provides methods for cleaning and tokenizing clinical and educational medical texts."""

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Removes duplicate spaces, tabs, and newlines."""
        if not text:
            return ""
        return " ".join(text.split()).strip()

    @staticmethod
    def remove_unnecessary_symbols(text: str) -> str:
        """
        Removes special symbols while keeping medical characters like hyphens,
        periods in abbreviations, slashes in ratios, plus signs, and percent signs.
        """
        if not text:
            return ""
        # Normalize unicode characters (accents, curly quotes)
        text = unicodedata.normalize("NFKD", text)
        # Replace non-breaking spaces
        text = text.replace("\u00a0", " ")
        # Keep letters, numbers, spaces, hyphens, slashes, pluses, periods, percent
        cleaned = re.sub(r"[^\w\s\-\+\/\.\%]", " ", text)
        # Normalize spaces again
        return TextCleaner.normalize_whitespace(cleaned)

    @classmethod
    def clean(
        cls,
        text: str,
        lowercase: bool = True,
        remove_stopwords: bool = False,
        preserve_medical_terms: bool = True
    ) -> str:
        """
        Full text cleaning pipeline.
        Returns a normalized text string.
        """
        if not text:
            return ""
        
        # Whitespace normalization
        cleaned = cls.normalize_whitespace(text)
        
        # Symbol removal
        cleaned = cls.remove_unnecessary_symbols(cleaned)
        
        if lowercase:
            cleaned = cleaned.lower()

        if remove_stopwords:
            tokens = cls.tokenize(cleaned, remove_stopwords=True)
            cleaned = " ".join(tokens)

        return cleaned

    @classmethod
    def tokenize(
        cls,
        text: str,
        lowercase: bool = True,
        remove_stopwords: bool = False,
        min_length: int = 1
    ) -> List[str]:
        """
        Tokenizes text into meaningful tokens.
        Preserves terms like 'type-2', 'covid-19', 'b12', 'h1n1', 'fev1', etc.
        """
        if not text:
            return []

        if lowercase:
            text = text.lower()

        # Tokenize by matching alphanumeric sequences, possibly containing internal hyphens or periods
        # e.g., 'type-2', 'h.pylori', 'covid-19', 'cd4+'
        tokens = re.findall(r"\b[a-zA-Z0-9]+(?:[\-\.][a-zA-Z0-9]+)*\b", text)

        if remove_stopwords:
            tokens = [t for t in tokens if t not in SAFE_STOPWORDS or t in MEDICAL_PRESERVED_WORDS]

        if min_length > 1:
            tokens = [t for t in tokens if len(t) >= min_length]

        return tokens


def clean_text(text: str, lowercase: bool = True, remove_stopwords: bool = False) -> str:
    """Convenience wrapper for TextCleaner.clean."""
    return TextCleaner.clean(text, lowercase=lowercase, remove_stopwords=remove_stopwords)


def tokenize(text: str, lowercase: bool = True, remove_stopwords: bool = False) -> List[str]:
    """Convenience wrapper for TextCleaner.tokenize."""
    return TextCleaner.tokenize(text, lowercase=lowercase, remove_stopwords=remove_stopwords)
