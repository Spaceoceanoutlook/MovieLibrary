import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")
bot = telebot.TeleBot(TOKEN)

bot.set_my_commands([
    types.BotCommand("search", "Поиск фильма"),
    types.BotCommand("genres", "Выбрать жанр")
])

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Загляни в меню",
    )

@bot.message_handler(commands=['search'])
def search(message):
    bot.send_message(
        message.chat.id,
        "Пиши название фильма (можно частично)",
    )

@bot.message_handler(commands=['genres'])
def genres(message):
    url = "https://spaceocean.ru/api/filters/genres/"
    response = requests.get(url)
    genres_data = response.json()

    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text=genre, callback_data=f"genre_{genre}")
        for genre in genres_data
    ]
    markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Выбери жанр:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("genre_"))
def handle_genre_callback(call):
    genre = call.data.replace("genre_", "")

    url = f"https://spaceocean.ru/api/filters/genres/{genre}"
    response = requests.get(url)
    json_data = response.json()

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"🎞 Фильмы жанра *{genre}*:", parse_mode="Markdown")

    for film in json_data:
        title = film.get("title")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Подробнее", callback_data=f"film_{film['id']}"))

        bot.send_message(
            call.message.chat.id,
            f"🎬 {title}",
            reply_markup=markup
        )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    url = f"https://spaceocean.ru/api/films/search?q={message.text}"
    response = requests.get(url)
    json_data = response.json()

    for film in json_data:
        title = film.get("title")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Подробнее", callback_data=f"film_{film['id']}"))

        bot.send_message(
            message.chat.id,
            f"🎬 {title}",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("film_"))
def handle_film_details(call):
    film_id = call.data.split("_")[1]
    url = f"https://spaceocean.ru/api/films/{film_id}"
    response = requests.get(url)
    film_data = response.json()
    message_text = (
            f"🎞 <b>{film_data.get('title')}</b>\n\n"
            f"🗓️ Год: {film_data.get('year')}\n"
            f"🌟 Рейтинг: {film_data.get('rating')}\n"
            f"📖 Описание: {film_data.get('description')}"
        )

    bot.send_message(
        call.message.chat.id, message_text,
        parse_mode="HTML"
    )

if __name__ == '__main__':
    print('Bot запущен')
    bot.infinity_polling()
