from typing import List

from sqlalchemy import Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import FilmCountry, FilmGenre
from .base import Base
from .enum import MediaType


class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(Enum(MediaType), default=MediaType.movie)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    photo: Mapped[str] = mapped_column(String, nullable=False)

    genres: Mapped[List["FilmGenre"]] = relationship(
        back_populates="film", cascade="all, delete-orphan", passive_deletes=True
    )
    countries: Mapped[List["FilmCountry"]] = relationship(
        back_populates="film", cascade="all, delete-orphan", passive_deletes=True
    )

    @property
    def genre_list(self):
        return [fg.genre for fg in self.genres]

    @property
    def country_list(self):
        return [fc.country for fc in self.countries]
