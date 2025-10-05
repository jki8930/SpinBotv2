import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from src.bot.keyboards import get_main_menu_keyboard

def create_bot():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    return bot

def create_dispatcher():
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_command(message: types.Message):
        await message.answer("Привет! Добро пожаловать в TRGSpin!", reply_markup=get_main_menu_keyboard())

    @dp.callback_query(F.data == "referral_system")
    async def referral_system_callback(callback_query: types.CallbackQuery):
        await callback_query.answer("Вы выбрали реферальную систему.", show_alert=True)

    @dp.callback_query(F.data == "leaderboard")
    async def leaderboard_callback(callback_query: types.CallbackQuery):
        await callback_query.answer("Вы выбрали таблицу лидеров.", show_alert=True)

    @dp.errors()
    async def error_handler(update: types.Update, exception: Exception):
        logging.error(f"Ошибка при обработке апдейта {update}: {exception}")
        return True

    return dp

async def run_bot(bot: Bot, dp: Dispatcher):
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
