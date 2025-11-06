from typing import List

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from movielibrary.database import get_db
from movielibrary.models import Country, Film, FilmCountry, FilmGenre, Genre
from movielibrary.schemas.film import FilmRead

templates = Jinja2Templates(directory="movielibrary/templates")
router = APIRouter()

COMMON_FILM_OPTIONS = [
    selectinload(Film.genres).selectinload(FilmGenre.genre),
    selectinload(Film.countries).selectinload(FilmCountry.country),
]


@router.get(
    "/genres", summary="List Genres", description="Возвращает список всех жанров"
)
async def list_genres(db: AsyncSession = Depends(get_db)):
    stmt = select(Genre)
    result = await db.execute(stmt)
    genres = result.scalars().all()
    return [g.name for g in genres]


@router.get(
    "/countries", summary="List Countries", description="Возвращает список всех стран"
)
async def list_countries(db: AsyncSession = Depends(get_db)):
    stmt = select(Country)
    result = await db.execute(stmt)
    countries = result.scalars().all()
    return [c.name for c in countries]


@router.get(
    "/genres/{genre_name}",
    response_model=List[FilmRead],
    summary="List Films By Genre",
    description="Возвращает список всех фильмов, отфильтрованными по выбранному жанру",
)
async def read_films_by_genre(genre_name: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .join(Film.genres)
        .join(FilmGenre.genre)
        .filter(Genre.name == genre_name)
        .order_by(desc(Film.id))
    )
    result = await db.execute(stmt)
    films = result.scalars().all()
    films_for_response = [FilmRead.model_validate(film) for film in films]
    return films_for_response


@router.get(
    "/countries/{country_name}",
    response_model=List[FilmRead],
    summary="List Films By Country",
    description="Возвращает список всех фильмов, отфильтрованными по выбранной стране",
)
async def read_films_by_country(country_name: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .join(Film.countries)
        .join(FilmCountry.country)
        .filter(Country.name == country_name)
        .order_by(desc(Film.id))
    )

    result = await db.execute(stmt)
    films = result.scalars().all()
    films_for_response = [FilmRead.model_validate(film) for film in films]
    return films_for_response


@router.get(
    "/years/{year}",
    response_model=List[FilmRead],
    summary="List Films By Year",
    description="Возвращает список всех фильмов, отфильтрованными по выбранному году выпуска",
)
async def read_films_by_year(year: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .filter(Film.year == year)
        .order_by(desc(Film.id))
    )

    result = await db.execute(stmt)
    films = result.scalars().all()
    films_for_response = [FilmRead.model_validate(film) for film in films]
    return films_for_response


@router.get(
    "/series",
    response_model=List[FilmRead],
    summary="List Films",
    description="Возвращает список всех сериалов с жанрами и странами",
)
async def list_series(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .filter(Film.type == "series")
        .order_by(desc(Film.id))
    )
    result = await db.execute(stmt)
    films = result.scalars().all()
    return films
