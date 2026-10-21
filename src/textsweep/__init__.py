"""textsweep: a tiny, dependency-free text cleaner for NLP preprocessing."""

from .core import STOPWORDS, TextCleaner, clean_text

__all__ = ["clean_text", "TextCleaner", "STOPWORDS"]
__version__ = "0.1.0"
