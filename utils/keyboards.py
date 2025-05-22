from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📁 Загрузить файл")],
            [KeyboardButton(text="📊 Начать рассылку")],
            [KeyboardButton(text="🛠 Настройки")]
        ],
        resize_keyboard=True
    )

def back_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Назад")]
        ],
        resize_keyboard=True
    )

def mailing_options_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Группа A", callback_data="a")],
            [InlineKeyboardButton(text="Группа Б", callback_data="b")],
            [InlineKeyboardButton(text="Все", callback_data="all")]
        ]
    )

def channels_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Email", callback_data="email")],
            [InlineKeyboardButton(text="WhatsApp", callback_data="whatsapp")],
            [InlineKeyboardButton(text="Telegram", callback_data="telegram")],
            [InlineKeyboardButton(text="Все каналы", callback_data="all")]
        ]
    )