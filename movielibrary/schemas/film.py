from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from .genre import GenreRead
from .country import CountryRead


class FilmBase(BaseModel):
    id: int
    title: str
    year: int
    description: Optional[str] = None
    rating: float


class FilmRead(FilmBase):
    photo: str
    genres: List[GenreRead] = Field(..., alias="genre_list")
    countries: List[CountryRead] = Field(..., alias="country_list")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
