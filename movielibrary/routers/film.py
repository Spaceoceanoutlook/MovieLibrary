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

    result = []
    for film in films:
        film_data = film.__dict__
        film_data["genres"] = [fg.genre for fg in film.genres]
        film_data["countries"] = [fc.country for fc in film.countries]
        result.append(film_data)

    return result


@router.get("/{film_id}", response_model=FilmRead)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    return film
