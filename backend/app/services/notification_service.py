"""Notification Service – email / push notifications."""
import smtplib
from email.message import EmailMessage
from app.config.settings import settings
from app.utils.logger import logger


class NotificationService:
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        try:
            msg = EmailMessage()
            msg["From"] = settings.SMTP_USER
            msg["To"] = to
            msg["Subject"] = subject
            msg.set_content(body)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"Email error: {e}")
            return False