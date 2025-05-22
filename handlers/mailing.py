from aiogram import Router, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import config
from utils.keyboards import (
    mailing_options_keyboard, 
    channels_keyboard, 
    back_keyboard,
    main_menu_keyboard
)
from services.email import send_email
from services.telegram import send_telegram_message
from services.whatsapp import send_whatsapp
import pandas as pd
import logging
import os

router = Router()
logger = logging.getLogger(__name__)

class MailingStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_email_subject = State()
    waiting_for_group = State()
    waiting_for_channel = State()

def check_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS

@router.message(F.text == "📊 Начать рассылку")
async def start_mailing(message: types.Message, state: FSMContext):
    if not check_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещен")
        return
    
    if not os.path.exists(config.CONTACTS_FILE):
        await message.answer("❌ Файл с контактами не загружен")
        return
    
    await message.answer(
        "✍️ Введите текст для рассылки:",
        reply_markup=back_keyboard()
    )
    await state.set_state(MailingStates.waiting_for_text)

@router.message(MailingStates.waiting_for_text)
async def process_mailing_text(message: types.Message, state: FSMContext):
    await state.update_data(mailing_text=message.text)
    await message.answer(
        "📝 Введите тему для email (или нажмите 'Пропустить'):",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Пропустить")],
                [KeyboardButton(text="❌ Назад")]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(MailingStates.waiting_for_email_subject)

@router.message(MailingStates.waiting_for_email_subject, F.text == "Пропустить")
async def skip_email_subject(message: types.Message, state: FSMContext):
    await state.update_data(email_subject="Сообщение от бота")
    await ask_for_group(message, state)

@router.message(MailingStates.waiting_for_email_subject, F.text == "❌ Назад")
async def back_to_text(message: types.Message, state: FSMContext):
    await message.answer(
        "✍️ Введите текст для рассылки:",
        reply_markup=back_keyboard()
    )
    await state.set_state(MailingStates.waiting_for_text)

@router.message(MailingStates.waiting_for_email_subject)
async def process_email_subject(message: types.Message, state: FSMContext):
    await state.update_data(email_subject=message.text)
    await ask_for_group(message, state)

async def ask_for_group(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите группу для рассылки:",
        reply_markup=mailing_options_keyboard()
    )
    await state.set_state(MailingStates.waiting_for_group)

@router.callback_query(MailingStates.waiting_for_group, F.data.in_(["a", "b", "all"]))
async def select_group(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(group=callback.data)
    await callback.message.edit_text(
        "Теперь выберите каналы для рассылки:",
        reply_markup=channels_keyboard()
    )
    await state.set_state(MailingStates.waiting_for_channel)
    await callback.answer()

@router.callback_query(MailingStates.waiting_for_channel, F.data.in_(["email", "whatsapp", "telegram", "all"]))
async def start_sending(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mailing_text = data.get('mailing_text', '')
    email_subject = data.get('email_subject', 'Сообщение от бота')
    group = data.get('group', 'all')
    channels = callback.data
    
    await callback.message.edit_text("⏳ Начинаю рассылку...")
    
    try:
        contacts = pd.read_excel(config.CONTACTS_FILE)
        
        if group != "all":
            group_name = 'Группа A' if group == 'a' else 'Группа Б'
            contacts = contacts[contacts['Группа'] == group_name]
        
        success = 0
        errors = 0
        whatsapp_links = []
        
        for _, row in contacts.iterrows():            
            if channels in ["email", "all"] and pd.notna(row.get('Email')):
                status = await send_email(
                    to_email=row['Email'],
                    subject=email_subject,
                    body=mailing_text
                )
                if status: success += 1
                else: errors += 1
            
            if channels in ["telegram", "all"] and pd.notna(row.get('Telegram')):
                status, _ = await send_telegram_message(
                    user_id=row['Telegram'],
                    message=mailing_text
                )
                if status: success += 1
                else: errors += 1
            
            if channels in ["whatsapp", "all"] and pd.notna(row.get('WhatsApp')):
                status, link = await send_whatsapp(
                    phone=row['WhatsApp'],
                    message=mailing_text
                )
                if status: 
                    success += 1
                    whatsapp_links.append(link)
                else: errors += 1
        
        result_message = (
            f"✅ Рассылка завершена\n\n"
            f"Успешно отправлено: {success}\n"
            f"Ошибок: {errors}"
        )
        
        if whatsapp_links:
            result_message += "\n\n🔗 Ссылки WhatsApp (первые 10):\n" + "\n".join(whatsapp_links[:10])
        
        await callback.message.edit_text(result_message)
        
    except Exception as e:
        logger.error(f"Ошибка рассылки: {e}", exc_info=True)
        await callback.message.edit_text(f"❌ Ошибка рассылки: {str(e)}")
    
    await state.clear()
    await callback.answer()

@router.message(F.text == "❌ Назад")
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Главное меню",
        reply_markup=main_menu_keyboard()
    )