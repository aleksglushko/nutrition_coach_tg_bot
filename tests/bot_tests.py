import pytest
import src.keyboards as kb
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from src.bot import dp, start, bot
from src.stickers import STICKERS
from src.messages import MESSAGES

@pytest.mark.asyncio
async def test_start_command_handler():
    message = types.Message(chat=types.Chat(id=123), 
                            from_user=types.User(first_name="John"), 
                            text="/start")
    message.from_user = types.User(first_name="John")
    bot_mock = MagicMock()
    send_sticker_mock = bot_mock.send_sticker = AsyncMock()
    send_message_mock = bot_mock.send_message = AsyncMock()

    with patch("src.bot.bot", bot_mock):
        await start(message)
        send_sticker_mock.assert_called_with(message.chat.id, STICKERS['hi'])
        send_message_mock.assert_called_with(
            message.chat.id,
            f"Hello, {message.from_user.first_name if message.from_user else 'Unknown'}! 👋 \n\n" + MESSAGES['start'],
            reply_markup=kb.greet_kb,
            parse_mode='Markdown'
        )
