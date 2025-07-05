from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from .genre import GenreRead
from .country import CountryRead

class FilmBase(BaseModel):
    title: str
    year: int
    description: Optional[str] = None
    rating: float

class FilmCreate(FilmBase):
    pass

class FilmRead(FilmBase):
    id: int
    photo: str
    genres: List[GenreRead] = Field(..., alias="genre_list")
    countries: List[CountryRead] = Field(..., alias="country_list")

    model_config = ConfigDict(
            from_attributes=True,
            populate_by_name=True
        )
