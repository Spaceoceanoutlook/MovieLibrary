from fastapi import APIRouter, Depends, Request, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from movielibrary.schemas.film import FilmRead
from movielibrary.database import get_db
from movielibrary.models import Film, FilmGenre, FilmCountry, Genre, Country
from typing import List


router = APIRouter()
templates = Jinja2Templates(directory="movielibrary/templates")


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Read Films",
    description="Главная страница с HTML-шаблоном. Показывает список всех фильмов с жанрами и странами",
    include_in_schema=False
)
def read_films(request: Request, db: Session = Depends(get_db)):
    films = db.query(Film).options(
        joinedload(Film.genres).joinedload(FilmGenre.genre),
        joinedload(Film.countries).joinedload(FilmCountry.country)
    ).order_by(desc(Film.id)).all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse("index.html", {"request": request, "films": films_for_template})


@router.get(
    "/create",
    response_class=HTMLResponse,
    summary="Show Create Film Form",
    description="Показывает html-форму для создания нового фильма",
    include_in_schema=False
)
def show_create_film_form(request: Request, db: Session = Depends(get_db)):
    genre_list = db.query(Genre).all()
    country_list = db.query(Country).all()
    return templates.TemplateResponse("create.html", {"request": request, "genre_list": genre_list, "country_list": country_list})


@router.post(
    "/create",
    status_code=status.HTTP_302_FOUND,
    summary="Create Film",
    description="Обрабатывает отправку формы создания фильма, сохраняет фильм в базе и выполняет редирект на главную страницу",
    include_in_schema=False
)
def create_film(
    title: str = Form(..., min_length=1),
    year: int = Form(..., ge=1895),
    rating: float = Form(..., ge=0, le=10),
    description: str = Form(""),
    photo: str = Form(""),
    genres: List[int] = Form([]),
    countries: List[int] = Form([]),
    db: Session = Depends(get_db),
):
    new_film = Film(
        title=title,
        year=year,
        description=description,
        rating=rating,
        photo=photo
    )

    try:
        db.add(new_film)
        db.commit()
        db.refresh(new_film)

        for genre_id in genres:
            db.add(FilmGenre(film_id=new_film.id, genre_id=genre_id))
        for country_id in countries:
            db.add(FilmCountry(film_id=new_film.id, country_id=country_id))

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании фильма: {e}")

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
