from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from handlers.users.help_functions import check_valid
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(Command("groups"))
async def groups_func(message: types.Message):
    if await check_valid(message=message, group_name='Admins'):
        await message.answer('123')


