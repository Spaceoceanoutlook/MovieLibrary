from fastapi import APIRouter, Depends, Request
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from movielibrary.database import get_db
from movielibrary.schemas.film import FilmRead
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from movielibrary.models import Film, FilmGenre, FilmCountry, Country, Genre

templates = Jinja2Templates(directory="movielibrary/templates")
router = APIRouter()


@router.get(
    "/genres/",
    summary="List Genres",
    description="Возвращает список всех жанров фильмов"
)
def list_genres(db: Session = Depends(get_db)):
    genres = db.query(Genre).all()
    return [g.name for g in genres]


@router.get(
    "/countries/",
    summary="List Countries",
    description="Возвращает список всех стран"
)
def list_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    return [c.name for c in countries]


@router.get(
    "/genres/{genre_name}",
    response_class=HTMLResponse,
    summary="Read Films By Genre",
    description="Возвращает HTML-страницу с фильмами, отфильтрованными по выбранному жанру"
)
def read_films_by_genre(genre_name: str, request: Request, db: Session = Depends(get_db)):
    query = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).join(Film.genres).join(FilmGenre.genre).filter(Genre.name == genre_name)

    films = query.order_by(desc(Film.rating)).all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})


@router.get(
    "/countries/{country_name}",
    response_class=HTMLResponse,
    summary="Read Films By Country",
    description="Возвращает HTML-страницу с фильмами, отфильтрованными по выбранной стране"
)
def read_films_by_country(country_name: str, request: Request, db: Session = Depends(get_db)):
    query = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).join(Film.countries).join(FilmCountry.country).filter(Country.name == country_name)

    films = query.order_by(desc(Film.rating)).all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})


@router.get(
    "/years/{year}",
    response_class=HTMLResponse,
    summary="Read Films By Year",
    description="Возвращает HTML-страницу с фильмами, отфильтрованными по выбранному году выпуска"
)
def read_films_by_year(year: int, request: Request, db: Session = Depends(get_db)):
    query = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).filter(Film.year == year)

    films = query.order_by(desc(Film.rating)).all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})
