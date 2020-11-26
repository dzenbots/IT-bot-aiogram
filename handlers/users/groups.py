from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(Command("groups"))
async def groups_func(message: types.Message):
    pass
