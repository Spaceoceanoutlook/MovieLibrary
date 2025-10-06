import asyncio
import os
from typing import Any, Dict, List, Optional

import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def fetch_json(session: aiohttp.ClientSession, url: str) -> Any:
    """Получить JSON с базовой проверкой статуса."""
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json()


@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    await message.answer("Напиши название фильма:")


@dp.message(Command("genres"))
async def cmd_genres(message: types.Message):
    url = "https://filmlibrary.ru/api/filters/genres/"
    async with aiohttp.ClientSession() as session:
        try:
            genres_data: List[str] = await fetch_json(session, url)
        except Exception as e:
            await message.answer(f"Не удалось получить жанры: {e}")
            return

    if not genres_data:
        await message.answer("Жанры не найдены.")
        return

    # каждая строка — список кнопок
    buttons = [
        [types.InlineKeyboardButton(text=genre, callback_data=f"genre_{genre}")]
        for genre in genres_data
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Выбери жанр:", reply_markup=markup)


@dp.callback_query(F.data.startswith("genre_"))
async def handle_genre_callback(call: types.CallbackQuery):
    data = call.data.replace("genre_", "")

    if "|" in data:
        genre, offset_str = data.split("|", 1)
        try:
            offset = int(offset_str)
        except ValueError:
            offset = 0
    else:
        genre = data
        offset = 0

    url = f"https://filmlibrary.ru/api/filters/genres/{genre}"
    async with aiohttp.ClientSession() as session:
        try:
            films: List[Dict[str, Any]] = await fetch_json(session, url)
        except Exception as e:
            await call.message.answer(f"Не удалось получить фильмы жанра {genre}: {e}")
            await call.answer()
            return

    await call.answer()

    if not films:
        await call.message.answer(
            f"Фильмы жанра *{genre}* не найдены.", parse_mode="Markdown"
        )
        return

    if offset == 0:
        await call.message.answer(f"Фильмы жанра *{genre}*:", parse_mode="Markdown")

    films_slice = films[offset : offset + 5]

    for film in films_slice:
        title = film.get("title", "Без названия")
        film_id = film.get("id")
        # разметка через inline_keyboard
        details_markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Подробнее", callback_data=f"film_{film_id}"
                    )
                ]
            ]
        )
        await call.message.answer(f"🎬 {title}", reply_markup=details_markup)

    # кнопка "Еще"
    next_offset = offset + 5
    if next_offset < len(films):
        more_markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Еще", callback_data=f"genre_{genre}|{next_offset}"
                    )
                ]
            ]
        )
        await call.message.answer("🍿", reply_markup=more_markup)


@dp.message(F.text & ~F.via_bot)
async def handle_text(message: types.Message):
    query = (message.text or "").strip()
    if not query:
        return

    url = f"https://filmlibrary.ru/api/films/search?q={query}"
    async with aiohttp.ClientSession() as session:
        try:
            films: List[Dict[str, Any]] = await fetch_json(session, url)
        except Exception as e:
            await message.answer(f"Не удалось выполнить поиск: {e}")
            return

    if not films:
        await message.answer("Ничего не найдено.")
        return

    for film in films:
        title = film.get("title", "Без названия")
        film_id = film.get("id")
        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Подробнее", callback_data=f"film_{film_id}"
                    )
                ]
            ]
        )
        await message.answer(f"🎬 {title}", reply_markup=markup)


@dp.callback_query(F.data.startswith("film_"))
async def handle_film_details(call: types.CallbackQuery):
    film_id = call.data.split("_", 1)[1]
    url = f"https://filmlibrary.ru/api/films/{film_id}"

    async with aiohttp.ClientSession() as session:
        try:
            film_data: Dict[str, Optional[Any]] = await fetch_json(session, url)
        except Exception as e:
            await call.message.answer(f"Не удалось получить информацию о фильме: {e}")
            await call.answer()
            return

    title = film_data.get("title") or "Без названия"
    year = film_data.get("year") or "—"
    rating = film_data.get("rating") or "—"
    description = film_data.get("description") or "Описание отсутствует."

    message_text = (
        f"🎞 <b>{title}</b>\n\n"
        f"🗓️ Год: {year}\n"
        f"🌟 Рейтинг: {rating}\n"
        f"📖 Описание: {description}"
    )

    await call.message.answer(message_text, parse_mode="HTML")
    await call.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
