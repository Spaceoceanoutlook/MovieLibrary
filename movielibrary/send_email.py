import os
from email.mime.text import MIMEText

import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("EMAIL", "")
password = os.getenv("EMAIL_APP_PASSWORD", "")
receiver_emails = [
    email.strip()
    for email in os.getenv("RECEIVER_EMAILS", "").split(",")
    if email.strip()
]


async def send_email_async(title: str) -> None:
    for receiver_email in receiver_emails:
        text = f"На https://filmlibrary.ru добавлен новый фильм: {title}"
        msg = MIMEText(text, "plain")
        msg["From"] = f'"FilmLibrary" <{sender_email}>'
        msg["To"] = receiver_email
        msg["Subject"] = "Привет от FilmLibrary!"

        await aiosmtplib.send(
            msg,
            sender=sender_email,
            recipients=[receiver_email],
            hostname="smtp.yandex.ru",
            port=465,
            username=sender_email,
            password=password,
            use_tls=True,
        )
