from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .country import CountryRead
from .genre import GenreRead


class FilmBase(BaseModel):
    id: int
    title: str
    year: int
    description: Optional[str] = None
    rating: float

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v):
        if v < 0 or v > 10:
            raise ValueError("Рейтинг должен быть от 0 до 10")
        return v

    @field_validator("year")
    @classmethod
    def validate_year(cls, v):
        current_year = datetime.now().year
        if v > current_year:
            raise ValueError(f"Год не может быть больше {current_year}")
        if v < 1888:
            raise ValueError("Год не может быть меньше 1888 (год первого фильма)")
        return v


class FilmRead(FilmBase):
    photo: str
    genres: List[GenreRead] = Field(..., alias="genre_list")
    countries: List[CountryRead] = Field(..., alias="country_list")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
