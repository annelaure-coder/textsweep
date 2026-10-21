# textsweep

A tiny, dependency-free text cleaner for NLP preprocessing.

## Install

```bash
pip install textsweep
```

## Quick start

```python
from textsweep import clean_text

clean_text("Check out https://example.com!!! 🎉 It's <b>GREAT</b>.")
# 'check out its great'
```

### Remove stopwords

```python
clean_text("This is a test of the cleaner", remove_stopwords=True)
# 'test cleaner'
```

### Reusable cleaner (sklearn-style)

```python
from textsweep import TextCleaner

cleaner = TextCleaner(remove_stopwords=True, remove_numbers=True)
cleaner.transform(["The 3 cats sat", "A dog barked"])
# ['cats sat', 'dog barked']
```

It has `fit` / `transform` / `fit_transform`, so it works inside a scikit-learn `Pipeline`.

## Options

| Option | Default | What it does |
|---|---|---|
| `lowercase` | `True` | Lowercase everything |
| `remove_html` | `True` | Strip HTML tags and decode entities |
| `remove_urls` | `True` | Remove http(s) and www links |
| `remove_emails` | `True` | Remove email addresses |
| `remove_mentions` | `False` | Remove `@user` and `#tag` |
| `remove_emojis` | `True` | Remove emojis |
| `remove_numbers` | `False` | Remove digits |
| `remove_punctuation` | `True` | Remove punctuation |
| `strip_accents` | `False` | `café` becomes `cafe` |
| `remove_stopwords` | `False` | Drop common English words |
| `stopwords` | built-in | Pass your own set |
| `min_word_length` | `1` | Drop short tokens |

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
