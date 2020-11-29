from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.db_api import User
from utils.help_functions import check_valid_tuser, get_help_message
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    if await check_valid_tuser(message=message, group_name='Users'):
        user = User.get(telegram_id=message.chat.id)
        await message.answer(text=get_help_message(user=user))
