import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from src.bot.keyboards import get_main_menu_keyboard
from src.db.session import async_session
from src.db.queries import get_user_by_telegram_id, create_user, get_user_by_referral_code, count_referrals
from src.bot.middlewares.antiflood import AntiFloodMiddleware

def create_bot():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    return bot

def create_dispatcher():
    dp = Dispatcher()
    dp.message.middleware(AntiFloodMiddleware())

    @dp.message(CommandStart())
    async def start_command(message: types.Message):
        args = message.text.split()
        referred_by_id = None

        if len(args) > 1:
            referral_code = args[1]
            async with async_session() as session:
                referrer = await get_user_by_referral_code(session, referral_code)
                if referrer:
                    referred_by_id = referrer.id

        async with async_session() as session:
            user = await get_user_by_telegram_id(session, message.from_user.id)
            if not user:
                await create_user(session, message.from_user.id, message.from_user.username, referred_by=referred_by_id)
                await message.answer("Привет! Добро пожаловать в TRGSpin!", reply_markup=get_main_menu_keyboard())
            else:
                await message.answer("С возвращением!", reply_markup=get_main_menu_keyboard())

    @dp.callback_query(F.data == "referral_system")
    async def referral_system_callback(callback_query: types.CallbackQuery):
        async with async_session() as session:
            user = await get_user_by_telegram_id(session, callback_query.from_user.id)
            if user:
                num_referrals = await count_referrals(session, user.id)
                bot_info = await callback_query.bot.get_me()
                bot_username = bot_info.username
                referral_link = f"https://t.me/{bot_username}?start={user.referral_code}"
                text = (
                    f"👥 Реферальная система 👥\n\n"
                    f"Приглашайте друзей и получайте бонусы!\n\n"
                    f"🔗 Ваша реферальная ссылка: {referral_link}\n"
                    f"\n"
                    f"Вы пригласили: {num_referrals} человек"
                )
                await callback_query.message.answer(text)
            await callback_query.answer()

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
