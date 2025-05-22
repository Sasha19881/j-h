from aiogram import Router, types, F
from aiogram.filters import Command
from config import config
from utils.keyboards import main_menu_keyboard
import os
import pandas as pd
import logging

router = Router()
logger = logging.getLogger(__name__)

def check_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if not check_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещен")
        return
    
    status = "❌ Файл не загружен"
    if os.path.exists(config.CONTACTS_FILE):
        try:
            contacts = pd.read_excel(config.CONTACTS_FILE)
            status = f"✅ Файл загружен ({len(contacts)} контактов)"
        except Exception as e:
            status = f"❌ Ошибка файла: {str(e)}"
    
    await message.answer(
        f"📌 Главное меню\n\nСтатус: {status}",
        reply_markup=main_menu_keyboard()
    )

@router.message(F.text == "🛠 Настройки")
async def show_settings(message: types.Message):
    contacts_status = "❌ Нет файла"
    if os.path.exists(config.CONTACTS_FILE):
        try:
            df = pd.read_excel(config.CONTACTS_FILE)
            contacts_status = f"✅ {len(df)} контактов"
        except:
            contacts_status = "❌ Ошибка чтения"
    
    await message.answer(
        f"⚙️ Текущие настройки:\n\n"
        f"• Контакты: {contacts_status}\n"
        f"• Доступно админов: {len(config.ADMIN_IDS)}\n"
        f"• Почта: {'✅' if config.EMAIL_FROM else '❌'}\n"
        f"• WhatsApp: {'✅' if config.TELEGRAM_PHONE else '❌'}\n"
        f"• Telegram: {'✅' if config.TELEGRAM_BOT_TOKEN else '❌'}",
        reply_markup=main_menu_keyboard()
    )