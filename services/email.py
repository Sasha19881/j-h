import smtplib
from email.message import EmailMessage
from config import config
import logging

logger = logging.getLogger(__name__)

async def send_email(to_email: str, subject: str, body: str) -> bool:
    try:
        if not all([config.SMTP_SERVER, config.EMAIL_FROM, config.EMAIL_PASSWORD]):
            logger.error("Не настроены параметры SMTP")
            return False
            
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = config.EMAIL_FROM
        msg["To"] = to_email
        
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_FROM, config.EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email отправлен на {to_email}")
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки email: {e}")
        return False