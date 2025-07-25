from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
from movielibrary.models import Film, FilmCountry, FilmGenre
from movielibrary.database import get_db
from movielibrary.schemas.film import FilmRead, FilmBase


router = APIRouter()


@router.get(
    "",
    response_model=List[FilmBase],
    summary="List Films",
    description="Возвращает список всех фильмов с жанрами и странами"
)
def list_films(db: Session = Depends(get_db)):
    films = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).all()
    return films

@router.get(
    "/search",
    response_model=List[FilmRead],
    summary="Search Films by Title",
    description="Позволяет искать фильмы по названию (частичное совпадение)"
)
def search_films(
    q: str = Query(..., min_length=3, description="Название фильма"),
    db: Session = Depends(get_db)
):
    films = db.query(Film).filter(Film.title.ilike(f"%{q}%")).all()
    return films

@router.get(
    "/statistics",
    response_model=dict[str, float],
    summary="Get films statistics",
    description="Показывает общую информацию о библиотеке фильмов"
)
def get_films_statistics(db: Session = Depends(get_db)):
    films_count = db.query(Film).count()
    average_rating = db.query(func.avg(Film.rating)).scalar() or 0.0

    return {
        "total_films": films_count,
        "average_rating": round(average_rating, 2)
    }

@router.get(
    "/{film_id}",
    response_model=FilmRead,
    summary="Retrieve Film",
    description="Возвращает подробную информацию о фильме по его ID, включая жанры и страны"
)
def retrieve_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).options(
            joinedload(Film.genres).joinedload(FilmGenre.genre),
            joinedload(Film.countries).joinedload(FilmCountry.country)
        ).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return film
