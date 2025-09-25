import pytest
from pydantic import ValidationError

from movielibrary.schemas.film import FilmRead


def test_filmread_valid_data():
    data = {
        "id": 1,
        "title": "Test Film",
        "year": 2021,
        "rating": 7.5,
        "photo": "test.webp",
        "description": "A test description",
        "genre_list": [
            {"id": 1, "name": "Драма"},
            {"id": 2, "name": "Триллер"},
        ],
        "country_list": [
            {"id": 1, "name": "США"},
            {"id": 2, "name": "Россия"},
        ],
    }
    film = FilmRead.model_validate(data)

    assert film.id == 1
    assert film.title == "Test Film"
    assert film.rating == 7.5
    assert film.genres[1].name == "Триллер"
    assert film.countries[0].name == "США"


def test_filmread_invalid_rating():
    """Рейтинг вне диапазона"""
    data = {
        "id": 2,
        "title": "Bad Rating Film",
        "year": 2020,
        "rating": 17.0,
        "photo": "test.jpg",
        "genre_list": [],
        "country_list": [],
    }
    with pytest.raises(ValidationError):
        FilmRead.model_validate(data)


def test_filmread_invalid_year():
    """Год больше текущего"""
    data = {
        "id": 3,
        "title": "Future Film",
        "year": 2028,
        "rating": 5.0,
        "photo": "test.jpg",
        "genre_list": [],
        "country_list": [],
    }
    with pytest.raises(ValidationError):
        FilmRead.model_validate(data)


def test_filmread_missing_required_field():
    """Нет обязательного поля rating"""
    data = {
        "id": 4,
        "title": "Film without rating",
        "year": 2022,
        "photo": "test.jpg",
        "genre_list": [],
        "country_list": [],
    }
    with pytest.raises(ValidationError):
        FilmRead.model_validate(data)
