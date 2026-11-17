import pytest

from shortener import InvalidUrlError, UnknownCodeError, UrlShortener
from shortener.service import _encode


@pytest.fixture
def svc():
    return UrlShortener()


def test_create_and_resolve_roundtrip(svc):
    code = svc.create("https://example.com/page?x=1")
    assert svc.resolve(code) == "https://example.com/page?x=1"


def test_same_url_gets_same_code(svc):
    assert svc.create("https://example.com") == svc.create("https://example.com")
    assert len(svc) == 1


def test_different_urls_get_different_codes(svc):
    assert svc.create("https://a.example") != svc.create("https://b.example")
    assert len(svc) == 2


def test_codes_are_deterministic_and_short(svc):
    code = svc.create("https://example.com")
    assert code == "g8"  # 1000 в base62
    assert len(code) <= 6


def test_url_is_stripped_before_saving(svc):
    code = svc.create("  https://example.com/a  ")
    assert svc.resolve(code) == "https://example.com/a"


def test_short_url_has_base_prefix():
    svc = UrlShortener(base_url="http://sho.rt")
    full = svc.short_url("https://example.com")
    assert full.startswith("http://sho.rt/")
    assert svc.resolve(full.rsplit("/", 1)[1]) == "https://example.com"


@pytest.mark.parametrize(
    "bad",
    ["", "example.com", "ftp://example.com", "javascript:alert(1)", "http://", "   "],
)
def test_invalid_urls_are_rejected(svc, bad):
    with pytest.raises(InvalidUrlError):
        svc.create(bad)
    assert len(svc) == 0


def test_non_string_url_is_rejected(svc):
    with pytest.raises(InvalidUrlError):
        svc.create(None)


def test_unknown_code_raises(svc):
    with pytest.raises(UnknownCodeError):
        svc.resolve("nope")


@pytest.mark.parametrize("number,expected", [(0, "0"), (61, "Z"), (62, "10"), (1000, "g8")])
def test_base62_encoding(number, expected):
    assert _encode(number) == expected
