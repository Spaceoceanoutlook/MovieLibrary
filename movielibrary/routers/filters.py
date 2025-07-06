from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from movielibrary.database import get_db
from movielibrary.schemas.film import FilmRead
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from movielibrary.models import Film, FilmGenre, FilmCountry, Country, Genre

templates = Jinja2Templates(directory="movielibrary/templates")
filters_router = APIRouter(tags=["filters"])

@filters_router.get("/country/{country_name}", response_class=HTMLResponse, summary="Read Films By Country")
def read_films_by_country(country_name: str, request: Request, db: Session = Depends(get_db)):
    query = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).join(Film.countries).join(FilmCountry.country).filter(Country.name == country_name).order_by(desc(Film.id))

    films = query.all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})

@filters_router.get("/genre/{genre_name}", response_class=HTMLResponse, summary="Read Films By Genre")
def read_films_by_genre(genre_name: str, request: Request, db: Session = Depends(get_db)):
    query = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).join(Film.genres).join(FilmGenre.genre).filter(Genre.name == genre_name).order_by(desc(Film.id))

    films = query.all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})
