import os
from typing import List

from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Form,
    HTTPException,
    Query,
    Request,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from movielibrary.database import get_db
from movielibrary.models import Country, Film, FilmCountry, FilmGenre, Genre
from movielibrary.models.enums import MediaType
from movielibrary.schemas.film import FilmRead
from movielibrary.send_email import send_email_async

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="movielibrary/templates")

COMMON_FILM_OPTIONS = [
    selectinload(Film.genres).selectinload(FilmGenre.genre),
    selectinload(Film.countries).selectinload(FilmCountry.country),
]


async def get_all_genres(db: AsyncSession):
    result = await db.execute(select(Genre))
    return result.scalars().all()


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Read Films",
    description="Главная страница с HTML-шаблоном. Показывает список жанров и семь последних фильмов",
)
async def read_films(request: Request, db: AsyncSession = Depends(get_db)):
    stmt = select(Film).options(*COMMON_FILM_OPTIONS).order_by(desc(Film.id)).limit(5)
    result = await db.execute(stmt)
    films = result.scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]
    genres_for_template = await get_all_genres(db)

    page = 1
    total_pages = 1

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
            "page": page,
            "total_pages": total_pages,
        },
    )


@router.get(
    "/series/",
    summary="List Films with pagination",
    description="Возвращает список всех сериалов с жанрами и странами",
)
async def list_series(
    request: Request,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = 5,
):
    total_stmt = select(func.count()).select_from(Film).filter(Film.type == "series")
    total_result = await db.execute(total_stmt)
    total_films = total_result.scalar()

    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .filter(Film.type == "series")
        .order_by(desc(Film.rating))
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    result = await db.execute(stmt)
    films = result.scalars().all()

    genres_for_template = await get_all_genres(db)
    films_for_template = [FilmRead.model_validate(film) for film in films]

    total_pages = (total_films + page_size - 1) // page_size

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
            "page": page,
            "total_pages": total_pages,
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
    page: int = Query(1, ge=1),
    page_size: int = 5,
):
    total_stmt = (
        select(func.count())
        .select_from(Film)
        .join(Film.genres)
        .join(FilmGenre.genre)
        .filter(Genre.name == genre_name)
    )
    total_result = await db.execute(total_stmt)
    total_films = total_result.scalar()

    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .join(Film.genres)
        .join(FilmGenre.genre)
        .filter(Genre.name == genre_name)
        .order_by(desc(Film.rating))
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    result = await db.execute(stmt)
    films = result.scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]

    genres_for_template = await get_all_genres(db)

    total_pages = (total_films + page_size - 1) // page_size

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
            "page": page,
            "total_pages": total_pages,
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
    page: int = Query(1, ge=1),
    page_size: int = 5,
):
    total_stmt = (
        select(func.count())
        .select_from(Film)
        .join(Film.countries)
        .join(FilmCountry.country)
        .filter(Country.name == country_name)
    )
    total_result = await db.execute(total_stmt)
    total_films = total_result.scalar()

    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .join(Film.countries)
        .join(FilmCountry.country)
        .filter(Country.name == country_name)
        .order_by(desc(Film.rating))
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    result = await db.execute(stmt)
    films = result.scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]

    genres_for_template = await get_all_genres(db)

    total_pages = (total_films + page_size - 1) // page_size

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
            "page": page,
            "total_pages": total_pages,
        },
    )


@router.get(
    "/years/{year}",
    response_class=HTMLResponse,
    summary="Read Films By Year",
    description="Возвращает HTML-страницу с фильмами, отфильтрованными по выбранному году выпуска",
)
async def read_films_by_year(
    year: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = 5,
):
    total_stmt = select(func.count()).select_from(Film).filter(Film.year == year)
    total_result = await db.execute(total_stmt)
    total_films = total_result.scalar()

    stmt = (
        select(Film)
        .options(*COMMON_FILM_OPTIONS)
        .filter(Film.year == year)
        .order_by(desc(Film.rating))
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    result = await db.execute(stmt)
    films = result.scalars().all()
    films_for_template = [FilmRead.model_validate(film) for film in films]

    genres_for_template = await get_all_genres(db)

    total_pages = (total_films + page_size - 1) // page_size

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "films": films_for_template,
            "genres": genres_for_template,
            "page": page,
            "total_pages": total_pages,
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
    film = result.scalars().first()
    film = FilmRead.model_validate(film)
    page_title = film.title
    genres_for_template = await get_all_genres(db)
    return templates.TemplateResponse(
        "film_details.html",
        {
            "request": request,
            "film": film,
            "genres": genres_for_template,
            "page_title": page_title,
        },
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
    background_tasks: BackgroundTasks,
    title: str = Form(..., min_length=1),
    year: int = Form(..., ge=1895),
    rating: float = Form(..., ge=0, le=10),
    description: str = Form(""),
    photo: str = Form(""),
    code: str = Form(...),
    genres: List[int] = Form([]),
    countries: List[int] = Form([]),
    type: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    if code != os.getenv("VALID_CODE"):
        raise HTTPException(status_code=400, detail="Неверный код доступа")

    try:
        media_type = MediaType(type)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Недопустимый тип контента"
        ) from None

    if media_type != MediaType.movie:
        title += " (Сериал)"

    new_film = Film(
        title=title,
        year=year,
        description=description,
        rating=rating,
        photo=photo,
        type=media_type,
    )

    try:
        db.add(new_film)
        await db.flush()

        for genre_id in genres:
            db.add(FilmGenre(film_id=new_film.id, genre_id=genre_id))
        for country_id in countries:
            db.add(FilmCountry(film_id=new_film.id, country_id=country_id))

        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Ошибка при создании фильма"
        ) from None

    background_tasks.add_task(send_email_async, new_film.title)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
