from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from movielibrary.models import Film, FilmCountry, FilmGenre
from movielibrary.database import get_db
from movielibrary.schemas.film import FilmRead


film_router = APIRouter(
    prefix="/api",
    tags=["films"],
)

@film_router.get("/", response_model=List[FilmRead], summary="Get Films")
def get_films(db: Session = Depends(get_db)):
    films = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).all()
    return films

@film_router.get("/{film_id}", response_model=FilmRead, summary="Get Film")
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).options(
            joinedload(Film.genres).joinedload(FilmGenre.genre),
            joinedload(Film.countries).joinedload(FilmCountry.country)
        ).filter(Film.id == film_id).first()
    return film
