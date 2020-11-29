from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message

from keyboards.inline import group_function_keyboard
from loader import dp
from utils.help_functions import check_valid_tuser
from utils.misc import rate_limit


@rate_limit(5, 'groups')
@dp.message_handler(Command("groups"))
async def groups_func(message: Message):
    if await check_valid_tuser(message=message, group_name='Admins'):
        await message.answer(text='Выбите действие',
                             reply_markup=group_function_keyboard)
