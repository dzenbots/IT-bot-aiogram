from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from handlers.users.help_functions import check_valid_tuser
from keyboards.inline import group_list_keyboard
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(Command("groups"))
async def groups_func(message: types.Message):
    if await check_valid_tuser(message=message, group_name='Admins'):
        await message.answer(text='Выбите действие',
                             reply_markup=group_list_keyboard)


