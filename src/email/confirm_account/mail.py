import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from loguru import logger
from html_builder import build_email_confirm_html
from src.core import settings


class EmailSender:
    def __init__(self):
        self.sender = settings.email.EMAIL_ADDRESS
        self.password = settings.email.EMAIL_SECRET
        self.server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
        self.server.login(self.sender, self.password)
        logger.info("Email logged in successfully")

    def send_email_confirm(self, email: str, confirm_url: str):
        msg = MIMEMultipart()  # Создаем сообщение
        html = build_email_confirm_html(confirm_url)
        msg["From"] = self.sender
        msg["To"] = email
        msg["Subject"] = "Confirm registration"
        msg.attach(MIMEText(html, "html", "utf-8"))
        self.server.send_message(msg)
        logger.info(f"Message to {email!r} send successfully")

    def __delete__(self, instance):
        self.server.quit()


def sand_confirm_email(email: str, confirm_url: str):
    sender = EmailSender()
    sender.send_email_confirm(email, confirm_url)


if __name__ == "__main__":
    sand_confirm_email("beiov2004.mail@gmail.com", "https://leetcode.com")
