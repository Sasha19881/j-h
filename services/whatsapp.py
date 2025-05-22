import urllib.parse
from config import config
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

def clean_phone(phone: str) -> str:
    """Очистка номера телефона"""
    phone = ''.join(c for c in str(phone) if c.isdigit())
    if phone.startswith('8'):
        phone = '7' + phone[1:]
    elif phone.startswith('+'):
        phone = phone[1:]
    return phone

async def send_whatsapp(phone: str, message: str) -> Tuple[bool, str]:
    try:
        phone = clean_phone(phone)
        if not phone:
            return False, "Неверный формат номера"
            
        if not phone.startswith('7') or len(phone) != 11:
            return False, "Номер должен быть в формате 7XXXXXXXXXX"
            
        link = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"
        logger.info(f"WhatsApp ссылка сгенерирована: {link}")
        
        # Для реальной отправки можно использовать:
        # from selenium import webdriver
        # driver = webdriver.Chrome()
        # driver.get(link)
        # time.sleep(5)  # Даем время на отправку
        # driver.quit()
        
        return True, link
    except Exception as e:
        logger.error(f"Ошибка WhatsApp: {e}")
        return False, str(e)