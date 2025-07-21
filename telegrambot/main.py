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
    types.BotCommand("start", "Запустить бота")
])

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Я помогу тебе найти фильм по части его названия:",
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
            f"🎞 <b>{film_data.get('title', 'Без названия')}</b>\n\n"
            f"🗓️ Год: {film_data.get('year', 'Н/Д')}\n"
            f"🌟 Рейтинг: {film_data.get('rating', 'Н/Д')}\n"
            f"📖 Описание: {film_data.get('description', 'Нет описания')}"
        )

    bot.send_message(
        call.message.chat.id, message_text,
        parse_mode="HTML"
    )

if __name__ == '__main__':
    bot.infinity_polling()
