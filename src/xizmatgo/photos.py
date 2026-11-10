"""FR-03 / SR-08 (ПР-10): проверка фото, прикладываемых к заказу."""
from dataclasses import dataclass

MAX_PHOTOS = 5
MAX_SIZE = 5 * 1024 * 1024                       # 5 МБ
SIGNATURES = {b"\xff\xd8\xff": "jpg", b"\x89PNG\r\n\x1a\n": "png"}


class PhotoError(ValueError):
    pass


@dataclass
class Photo:
    name: str
    content: bytes


def detect_type(content: bytes) -> str:
    """Тип определяется по сигнатуре содержимого, а не по расширению файла."""
    for sig, kind in SIGNATURES.items():
        if content.startswith(sig):
            return kind
    raise PhotoError("Допустимы только изображения JPG и PNG")


def validate_photos(photos: list) -> list:
    if len(photos) > MAX_PHOTOS:
        raise PhotoError(f"Можно приложить не более {MAX_PHOTOS} фото")
    kinds = []
    for p in photos:
        if len(p.content) > MAX_SIZE:
            raise PhotoError(f"Файл {p.name} больше 5 МБ")
        kinds.append(detect_type(p.content))
    return kinds
