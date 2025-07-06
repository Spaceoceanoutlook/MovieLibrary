from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from movielibrary.schemas.film import FilmRead
from movielibrary.database import get_db
from movielibrary.models import Film, FilmGenre, FilmCountry

homepage_router = APIRouter()
templates = Jinja2Templates(directory="movielibrary/templates")

@homepage_router.get(
    "/",
    response_class=HTMLResponse,
    summary="Read Films",
    description="Главная страница с HTML-шаблоном. Показывает список всех фильмов с жанрами и странами."
)
def read_films(request: Request, db: Session = Depends(get_db)):
    films = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).order_by(desc(Film.id)).all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})
