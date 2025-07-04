from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from movielibrary.models import Film
from movielibrary.database import get_db
from movielibrary.schemas.film import FilmRead


router = APIRouter(
    prefix="/films",
    tags=["films"],
)

@router.get("/", response_model=List[FilmRead])
def get_films(db: Session = Depends(get_db)):
    films = db.query(Film).all()
    return films

@router.get("/{film_id}", response_model=FilmRead)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    return film
