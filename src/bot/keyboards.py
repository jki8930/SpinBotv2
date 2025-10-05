from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎰 Колесо фортуны", web_app={"url": "http://localhost:8000/static/index.html"}) # Placeholder URL
    )
    builder.row(
        InlineKeyboardButton(text="👥 Реферальная система", callback_data="referral_system")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Таблица лидеров", callback_data="leaderboard")
    )
    return builder.as_markup()
