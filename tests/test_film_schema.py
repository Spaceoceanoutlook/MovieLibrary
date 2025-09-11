import pytest
from pydantic import ValidationError

from movielibrary.schemas.film import FilmRead


class DummyGenre:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class DummyCountry:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class DummyFilm:
    def __init__(self):
        self.id = 1
        self.title = "Test Film"
        self.rating = 7.5
        self.description = "A test description"
        self.year = 2021
        self.photo = "test.jpg"
        self.genres = [DummyGenre(1, "Action"), DummyGenre(2, "Thriller")]
        self.countries = [DummyCountry(1, "USA"), DummyCountry(2, "France")]


class IncompleteFilm:
    """Фильм без rating"""

    def __init__(self):
        self.id = 2
        self.title = "Film 2"
        self.description = "A test description"
        self.year = 2022
        self.genres = []
        self.countries = []


def test_filmread_from_object():
    film = DummyFilm()
    fr = FilmRead.model_validate(film)
    assert fr.title == film.title
    assert fr.rating == film.rating
    assert fr.genres[0].name == "Action"
    assert fr.countries[0].name == "USA"


def test_filmread_missing_required_field_raises():
    with pytest.raises(ValidationError):
        FilmRead.model_validate(IncompleteFilm())
