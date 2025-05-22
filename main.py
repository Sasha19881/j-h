import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.start import router as start_router
from handlers.excel import router as excel_router
from handlers.mailing import router as mailing_router
from config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)

async def main():
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(start_router)
    dp.include_router(excel_router)
    dp.include_router(mailing_router)
    
    await bot.send_message(config.ADMIN_IDS[0], "🤖 Бот запущен! /start")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())