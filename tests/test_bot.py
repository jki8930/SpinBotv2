import pytest
from unittest.mock import AsyncMock
from aiogram import Bot
from aiogram.methods import SendMessage
from aiogram.types import Update, Message, User, Chat
from src.bot.main import create_dispatcher

@pytest.mark.asyncio
async def test_start_command(mocker):
    mocker.patch("src.db.queries.get_user_by_telegram_id", new_callable=AsyncMock, return_value=None)
    mocker.patch("src.db.queries.create_user", new_callable=AsyncMock)
    dp = create_dispatcher()
    bot = Bot(token="123456789:AABBCCDDEEFFaabbccddeeff-123456789")
    chat = Chat(id=123, type="private")
    user = User(id=123, is_bot=False, first_name="Test")
    message = Message(message_id=1, date=123, chat=chat, from_user=user, text="/start")
    update = Update(update_id=1, message=message)

    async def mock_send_message(*args, **kwargs):
        return True

    mocker.patch.object(bot, 'send_message', new=mock_send_message)

    result = await dp.feed_update(bot, update)
    assert result is not None
