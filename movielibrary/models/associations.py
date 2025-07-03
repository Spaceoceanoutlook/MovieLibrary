from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from models import Film, Country, Genre
from sqlalchemy import ForeignKey

class FilmGenre(Base):
    __tablename__ = "film_genre"

    film_id: Mapped[int] = mapped_column(ForeignKey("films.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)

    film: Mapped["Film"] = relationship(back_populates="genres")
    genre: Mapped["Genre"] = relationship(back_populates="films")


class FilmCountry(Base):
    __tablename__ = "film_country"

    film_id: Mapped[int] = mapped_column(ForeignKey("films.id"), primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), primary_key=True)

    film: Mapped["Film"] = relationship(back_populates="countries")
    country: Mapped["Country"] = relationship(back_populates="films")
