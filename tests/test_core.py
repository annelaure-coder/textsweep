import pytest

from textsweep import TextCleaner, clean_text


def test_basic_lowercase_and_punctuation():
    assert clean_text("Hello, World!!") == "hello world"


def test_removes_urls_and_emails():
    out = clean_text("Visit https://example.com or mail me@site.org now")
    assert out == "visit or mail now"


def test_removes_html():
    assert clean_text("<p>Hi &amp; bye</p>") == "hi bye"


def test_emojis_removed():
    assert clean_text("great job 🎉🔥") == "great job"


def test_numbers_optional():
    assert clean_text("room 101") == "room 101"
    assert clean_text("room 101", remove_numbers=True) == "room"


def test_mentions_optional():
    assert clean_text("hi @bob #ml", remove_mentions=True) == "hi"


def test_strip_accents():
    assert clean_text("café naïve", strip_accents=True) == "cafe naive"


def test_stopwords():
    assert clean_text("this is a test of the cleaner", remove_stopwords=True) == "test cleaner"


def test_custom_stopwords():
    assert clean_text("foo bar baz", remove_stopwords=True, stopwords={"bar"}) == "foo baz"


def test_min_word_length():
    assert clean_text("a bb ccc", min_word_length=2) == "bb ccc"


def test_hyphen_becomes_space():
    assert clean_text("well-known") == "well known"


def test_apostrophes_dropped():
    assert clean_text("don't stop") == "dont stop"


def test_type_error():
    with pytest.raises(TypeError):
        clean_text(123)


def test_empty_string():
    assert clean_text("") == ""


def test_class_api():
    c = TextCleaner(remove_stopwords=True)
    assert c.fit_transform(["The cat sat!", "A dog"]) == ["cat sat", "dog"]
    assert c("The END") == "end"


def test_class_rejects_bad_option():
    with pytest.raises(TypeError):
        TextCleaner(not_a_real_option=True)
