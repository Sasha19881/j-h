from telethon import TelegramClient, errors
from config import config
import asyncio
import logging

logger = logging.getLogger(__name__)

tg_client = TelegramClient(
    'tg_session',
    config.TELEGRAM_API_ID,
    config.TELEGRAM_API_HASH
)

async def send_telegram_message(user_id: str, message: str) -> tuple[bool, str]:
    try:
        if not tg_client.is_connected():
            await tg_client.start(config.TELEGRAM_PHONE)
        
        user_id = user_id.strip().lstrip('@')
        await tg_client.send_message(user_id, message)
        await asyncio.sleep(1)  # Anti-flood
        return True, None
    except errors.FloodWaitError as e:
        return False, f"Флуд-контроль: {e.seconds} сек."
    except errors.UserIsBlockedError:
        return False, "Пользователь заблокировал бота"
    except Exception as e:
        logger.error(f"Ошибка Telegram: {e}")
        return False, str(e)