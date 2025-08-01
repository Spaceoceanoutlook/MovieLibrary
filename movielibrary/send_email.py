import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv('EMAIL', '')
password = os.getenv('EMAIL_APP_PASSWORD', '')
receiver_emails = os.getenv('RECEIVER_EMAILS', '').split(',')

def send_email(title: str):
    text = f'На https://spaceocean.ru добавлен новый фильм: {title}'
    msg = MIMEText(text, 'plain')
    msg['From'] = sender_email
    msg['Subject'] = 'Привет от Spaceocean!'

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
        server.login(sender_email, password)
        for receiver_email in receiver_emails:
            msg['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, msg.as_string())
