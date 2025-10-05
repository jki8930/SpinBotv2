import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

def create_bot():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    return bot

def create_dispatcher():
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_command(message: types.Message):
        await message.answer("Привет! Добро пожаловать в TRGSpin!")

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
