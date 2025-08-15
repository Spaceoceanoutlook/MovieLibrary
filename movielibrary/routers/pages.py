import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from movielibrary.database import get_db
from movielibrary.models import Country, Film, FilmCountry, FilmGenre, Genre
from movielibrary.schemas.film import FilmRead
from movielibrary.send_email import send_email

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="movielibrary/templates")

COMMON_FILM_OPTIONS = [
    joinedload(Film.genres).joinedload(FilmGenre.genre),
    joinedload(Film.countries).joinedload(FilmCountry.country),
]


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Read Films",
    description="Главная страница с HTML-шаблоном. Показывает список жанров и семь последних фильмов с жанрами и странами",
)
async def read_films(request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(Film).options(*COMMON_FILM_OPTIONS).order_by(desc(Film.id)).limit(7)
    result = await db.execute(stmt)
    films = result.unique().scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    stmt = select(Genre)
    result = await db.execute(stmt)
    genres = result.scalars().all()
    genres_for_template = list(genres)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
        },
    )


@router.get(
    "/series/",
    response_model=List[FilmRead],
    summary="List Films",
    description="Возвращает список всех сериалов с жанрами и странами",
)
async def list_series(request: Request, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .filter(Film.title.ilike("%Сериал%"))
        .order_by(desc(Film.rating))
    )
    result = await db.execute(stmt)
    films = result.unique().scalars().all()
    stmt = select(Genre)
    result = await db.execute(stmt)
    genres = result.scalars().all()
    genres_for_template = list(genres)
    films_for_template = [FilmRead.model_validate(film) for film in films]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
        },
    )


@router.get(
    "/genres/{genre_name}",
    response_class=HTMLResponse,
    summary="Read Films By Genre",
    description="Возвращает HTML-страницу с фильмами, отфильтрованными по выбранному жанру",
)
async def read_films_by_genre(
    genre_name: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .join(Film.genres)
        .join(FilmGenre.genre)
        .filter(Genre.name == genre_name)
        .order_by(desc(Film.rating))
    )
    result = await db.execute(stmt)
    films = result.unique().scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    stmt = select(Genre)
    result = await db.execute(stmt)
    genres = result.scalars().all()
    genres_for_template = list(genres)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
        },
    )


@router.get(
    "/countries/{country_name}",
    response_class=HTMLResponse,
    summary="Read Films By Country",
    description="Возвращает HTML-страницу с фильмами, отфильтрованными по выбранной стране",
)
async def read_films_by_country(
    country_name: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .join(Film.countries)
        .join(FilmCountry.country)
        .filter(Country.name == country_name)
        .order_by(desc(Film.rating))
    )

    result = await db.execute(stmt)
    films = result.unique().scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    stmt = select(Genre)
    result = await db.execute(stmt)
    genres = result.scalars().all()
    genres_for_template = list(genres)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
        },
    )


@router.get(
    "/years/{year}",
    response_class=HTMLResponse,
    summary="Read Films By Year",
    description="Возвращает HTML-страницу с фильмами, отфильтрованными по выбранному году выпуска",
)
async def read_films_by_year(
    year: int, request: Request, db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .filter(Film.year == year)
        .order_by(desc(Film.rating))
    )

    result = await db.execute(stmt)
    films = result.unique().scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    stmt = select(Genre)
    result = await db.execute(stmt)
    genres = result.scalars().all()
    genres_for_template = list(genres)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
        },
    )


@router.get(
    "/film/{id}",
    response_class=HTMLResponse,
    summary="Read Film By Id",
    description="Возвращает HTML-страницу с выбранным фильмом",
)
async def read_film(id: int, request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(Film).options(*COMMON_FILM_OPTIONS).filter(Film.id == id)
    result = await db.execute(stmt)
    result = result.unique()
    films = result.scalars().all()
    films = [FilmRead.model_validate(film) for film in films]
    stmt = select(Genre)
    result = await db.execute(stmt)
    genres = result.scalars().all()
    genres_for_template = list(genres)
    return templates.TemplateResponse(
        "film_details.html",
        {"request": request, "films": films, "genres": genres_for_template},
    )


@router.get(
    "/create",
    response_class=HTMLResponse,
    summary="Show Create Film Form",
    description="Показывает html-форму для создания нового фильма",
)
async def show_create_film_form(request: Request, db: AsyncSession = Depends(get_db)):
    stmt_genre = select(Genre)
    result_genre = await db.execute(stmt_genre)
    genre_list = result_genre.scalars().all()

    stmt_country = select(Country)
    result_country = await db.execute(stmt_country)
    country_list = result_country.scalars().all()

    return templates.TemplateResponse(
        "create.html",
        {"request": request, "genre_list": genre_list, "country_list": country_list},
    )


@router.post(
    "/create",
    status_code=status.HTTP_302_FOUND,
    summary="Create Film",
    description="Обрабатывает отправку формы создания фильма, сохраняет фильм в базе и выполняет редирект на главную страницу",
)
async def create_film(
    title: str = Form(..., min_length=1),
    year: int = Form(..., ge=1895),
    rating: float = Form(..., ge=0, le=10),
    description: str = Form(""),
    photo: str = Form(""),
    code: str = Form(...),
    genres: List[int] = Form([]),
    countries: List[int] = Form([]),
    db: AsyncSession = Depends(get_db),
):
    if code != os.getenv("VALID_CODE"):
        raise HTTPException(status_code=400, detail="Неверный код доступа")

    new_film = Film(
        title=title, year=year, description=description, rating=rating, photo=photo
    )
    try:
        db.add(new_film)
        await db.commit()
        await db.refresh(new_film)

        for genre_id in genres:
            db.add(FilmGenre(film_id=new_film.id, genre_id=genre_id))
        for country_id in countries:
            db.add(FilmCountry(film_id=new_film.id, country_id=country_id))

        await db.commit()
        send_email(new_film.title)
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Ошибка при создании фильма"
        ) from None

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
