from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from movielibrary.database import get_db
from movielibrary.models import Film, FilmCountry, FilmGenre
from movielibrary.schemas.film import FilmBase, FilmRead

router = APIRouter()

COMMON_FILM_OPTIONS = [
    selectinload(Film.genres).selectinload(FilmGenre.genre),
    selectinload(Film.countries).selectinload(FilmCountry.country),
]


@router.get(
    "",
    response_model=List[FilmRead],
    summary="List Films",
    description="Возвращает список всех фильмов с жанрами и странами",
)
async def list_films(db: AsyncSession = Depends(get_db)):
    stmt = select(Film).options(*COMMON_FILM_OPTIONS).order_by(desc(Film.id))
    result = await db.execute(stmt)
    films = result.unique().scalars().all()
    return films


@router.get(
    "/search",
    response_model=List[FilmBase],
    summary="Search Films by Title",
    description="Позволяет искать фильмы по названию (частичное совпадение)",
)
async def search_films(
    q: str = Query(..., min_length=3, description="Название фильма"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Film).filter(Film.title.ilike(f"%{q}%"))
    result = await db.execute(stmt)
    films = result.scalars().all()
    return films


@router.get(
    "/statistics",
    response_model=dict[str, float],
    summary="Get films statistics",
    description="Показывает общую информацию о библиотеке фильмов",
)
async def get_films_statistics(db: AsyncSession = Depends(get_db)):
    result_count = await db.execute(select(func.count(Film.id)))
    films_count = result_count.scalar() or 0

    result_avg = await db.execute(select(func.avg(Film.rating)))
    average_rating = result_avg.scalar() or 0.0

    return {"total_films": films_count, "average_rating": round(average_rating, 2)}


@router.get(
    "/{film_id}",
    response_model=FilmRead,
    summary="Retrieve Film",
    description="Возвращает подробную информацию о фильме по его ID, включая жанры и страны",
)
async def retrieve_film(film_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Film).options(*COMMON_FILM_OPTIONS).filter(Film.id == film_id)
    result = await db.execute(stmt)
    film = result.unique().scalars().first()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return film
