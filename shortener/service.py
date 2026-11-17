"""Мини-сервис коротких ссылок. Хранилище — в памяти процесса."""

from urllib.parse import urlsplit

_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class InvalidUrlError(ValueError):
    """URL не является корректной http(s)-ссылкой."""


class UnknownCodeError(KeyError):
    """Короткий код не найден."""


def _encode(number: int) -> str:
    """Переводит неотрицательное число в строку base62."""
    if number == 0:
        return _ALPHABET[0]
    digits = []
    while number:
        number, rest = divmod(number, len(_ALPHABET))
        digits.append(_ALPHABET[rest])
    return "".join(reversed(digits))


def _validate(url: str) -> str:
    if not isinstance(url, str):
        raise InvalidUrlError("URL должен быть строкой")
    url = url.strip()
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise InvalidUrlError(f"Ожидается http(s)-ссылка, получено: {url!r}")
    return url


class UrlShortener:
    """Создаёт короткие коды и возвращает по ним исходные URL.

    Один и тот же URL всегда получает один и тот же код.
    """

    def __init__(self, base_url: str = "http://sho.rt/", start_id: int = 1000) -> None:
        self._base_url = base_url if base_url.endswith("/") else base_url + "/"
        self._next_id = start_id
        self._code_to_url: dict[str, str] = {}
        self._url_to_code: dict[str, str] = {}

    def create(self, url: str) -> str:
        """Возвращает короткий код для URL (создаёт, если ссылки ещё нет)."""
        url = _validate(url)
        if url in self._url_to_code:
            return self._url_to_code[url]
        code = _encode(self._next_id)
        self._next_id += 1
        self._code_to_url[code] = url
        self._url_to_code[url] = code
        return code

    def short_url(self, url: str) -> str:
        """Полная короткая ссылка: base_url + код."""
        return self._base_url + self.create(url)

    def resolve(self, code: str) -> str:
        """Возвращает исходный URL по коду; для неизвестного кода — UnknownCodeError."""
        try:
            return self._code_to_url[code]
        except KeyError:
            raise UnknownCodeError(code) from None

    def __len__(self) -> int:
        return len(self._code_to_url)
