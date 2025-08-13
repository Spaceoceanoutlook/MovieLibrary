from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float
from .base import Base
from .associations import FilmGenre, FilmCountry


class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
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
