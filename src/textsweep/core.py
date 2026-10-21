"""Core cleaning functions."""

from __future__ import annotations

import html
import re
import string
import unicodedata
from typing import Iterable, List, Optional

# A small built-in English stopword list (no NLTK needed).
STOPWORDS = frozenset(
    """
    a about above after again against all am an and any are as at be because
    been before being below between both but by can did do does doing down
    during each few for from further had has have having he her here hers
    herself him himself his how i if in into is it its itself just me more
    most my myself no nor not now of off on once only or other our ours
    ourselves out over own same she should so some such than that the their
    theirs them themselves then there these they this those through to too
    under until up very was we were what when where which while who whom why
    will with you your yours yourself yourselves
    """.split()
)

_URL_RE = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_NUMBER_RE = re.compile(r"\d+")
_MENTION_RE = re.compile(r"[@#]\w+")
_WHITESPACE_RE = re.compile(r"\s+")
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "\U0000FE00-\U0000FE0F"
    "]+",
    flags=re.UNICODE,
)
_PUNCT_TABLE = str.maketrans("", "", string.punctuation)


def clean_text(
    text: str,
    *,
    lowercase: bool = True,
    remove_html: bool = True,
    remove_urls: bool = True,
    remove_emails: bool = True,
    remove_mentions: bool = False,
    remove_emojis: bool = True,
    remove_numbers: bool = False,
    remove_punctuation: bool = True,
    strip_accents: bool = False,
    remove_stopwords: bool = False,
    stopwords: Optional[Iterable[str]] = None,
    min_word_length: int = 1,
) -> str:
    """Clean a string for NLP use.

    Parameters
    ----------
    text : str
        The raw text.
    lowercase, remove_html, remove_urls, remove_emails, remove_mentions,
    remove_emojis, remove_numbers, remove_punctuation, strip_accents,
    remove_stopwords : bool
        Toggle each cleaning step.
    stopwords : iterable of str, optional
        Custom stopword set. Defaults to the built-in English list.
    min_word_length : int
        Drop tokens shorter than this many characters.

    Returns
    -------
    str
        The cleaned text with single spaces between tokens.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")

    if remove_html:
        text = html.unescape(_HTML_TAG_RE.sub(" ", text))
    if remove_urls:
        text = _URL_RE.sub(" ", text)
    if remove_emails:
        text = _EMAIL_RE.sub(" ", text)
    if remove_mentions:
        text = _MENTION_RE.sub(" ", text)
    if remove_emojis:
        text = _EMOJI_RE.sub(" ", text)
    if strip_accents:
        text = "".join(
            c for c in unicodedata.normalize("NFKD", text)
            if not unicodedata.combining(c)
        )
    if lowercase:
        text = text.lower()
    if remove_numbers:
        text = _NUMBER_RE.sub(" ", text)
    if remove_punctuation:
        # Keep apostrophes inside words ("don't") by dropping them with the rest;
        # replace other punctuation with a space so "well-known" -> "well known".
        text = text.replace("'", "")
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)

    tokens = _WHITESPACE_RE.sub(" ", text).strip().split(" ")
    tokens = [t for t in tokens if t]

    if remove_stopwords:
        sw = frozenset(stopwords) if stopwords is not None else STOPWORDS
        tokens = [t for t in tokens if t.lower() not in sw]
    if min_word_length > 1:
        tokens = [t for t in tokens if len(t) >= min_word_length]

    return " ".join(tokens)


class TextCleaner:
    """Reusable cleaner with fixed settings, sklearn-style API.

    >>> cleaner = TextCleaner(remove_stopwords=True)
    >>> cleaner.transform(["Hello, World!"])
    ['hello world']
    """

    def __init__(self, **options) -> None:
        self.options = options
        # Validate options early by running a dry call.
        clean_text("", **options)

    def clean(self, text: str) -> str:
        return clean_text(text, **self.options)

    def transform(self, texts: Iterable[str]) -> List[str]:
        return [self.clean(t) for t in texts]

    # sklearn compatibility, so it can sit inside a Pipeline.
    def fit(self, X=None, y=None):
        return self

    def fit_transform(self, X, y=None):
        return self.transform(X)

    def __call__(self, text: str) -> str:
        return self.clean(text)

    def __repr__(self) -> str:
        opts = ", ".join(f"{k}={v!r}" for k, v in self.options.items())
        return f"TextCleaner({opts})"
