from pydantic import BaseModel
from typing import Optional
from typing import List
from .genre import GenreRead
from .country import CountryRead

class FilmBase(BaseModel):
    title: str
    year: int
    description: Optional[str] = None
    rating: int

class FilmCreate(FilmBase):
    pass

class FilmRead(FilmBase):
    id: int
    photo: str

    class Config:
        from_attributes = True

class FilmReadWithRelations(FilmRead):
    genres: List[GenreRead]
    countries: List[CountryRead]
