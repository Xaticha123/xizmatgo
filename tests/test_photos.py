"""Тесты проверки фото: классы эквивалентности и граничные значения (FR-03, SR-08)."""
import pytest
from xizmatgo.photos import validate_photos, Photo, PhotoError, MAX_SIZE

JPG = b"\xff\xd8\xff" + b"0" * 100
PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100


def test_five_photos_ok():
    assert validate_photos([Photo(f"{i}.jpg", JPG) for i in range(5)]) == ["jpg"] * 5


def test_six_photos_rejected():
    with pytest.raises(PhotoError):
        validate_photos([Photo(f"{i}.jpg", JPG) for i in range(6)])


def test_size_boundary():
    assert validate_photos([Photo("max.png", PNG.ljust(MAX_SIZE, b"0"))]) == ["png"]
    with pytest.raises(PhotoError):
        validate_photos([Photo("big.png", PNG.ljust(MAX_SIZE + 1, b"0"))])


def test_fake_extension_rejected():
    with pytest.raises(PhotoError):
        validate_photos([Photo("script.jpg", b"#!/bin/sh\nrm -rf /")])
