from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from movielibrary.models import Film, FilmCountry, FilmGenre
from movielibrary.database import get_db
from movielibrary.schemas.film import FilmRead, FilmReadWithRelations


router = APIRouter(
    prefix="/films",
    tags=["films"],
)

@router.get("/", response_model=List[FilmReadWithRelations])
def get_films(db: Session = Depends(get_db)):
    films = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).all()
    return films


@router.get("/{film_id}", response_model=FilmReadWithRelations)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).options(
            joinedload(Film.genres).joinedload(FilmGenre.genre),
            joinedload(Film.countries).joinedload(FilmCountry.country)
        ).filter(Film.id == film_id).first()
    return film
