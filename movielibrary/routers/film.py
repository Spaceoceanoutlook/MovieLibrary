from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from movielibrary.models import Film, FilmCountry, FilmGenre
from movielibrary.database import get_db
from movielibrary.schemas.film import FilmRead


film_router = APIRouter()

@film_router.get(
    "/",
    response_model=List[FilmRead],
    summary="Get Films",
    description="Возвращает список всех фильмов с жанрами и странами. Используется для API."
)
def get_films(db: Session = Depends(get_db)):
    films = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).all()
    return films

@film_router.get(
    "/{film_id}",
    response_model=FilmRead,
    summary="Get Film",
    description="Возвращает подробную информацию о фильме по его ID, включая жанры и страны."
)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).options(
            joinedload(Film.genres).joinedload(FilmGenre.genre),
            joinedload(Film.countries).joinedload(FilmCountry.country)
        ).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return film
