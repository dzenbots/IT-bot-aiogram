from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from handlers.users.help_functions import check_valid_tuser, get_tuser_info
from keyboards.inline import get_tuser_keyboard
from loader import dp
from utils.db_api import User
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(Command("all_users"))
async def groups_func(message: Message):
    if await check_valid_tuser(message=message, group_name='Admins'):
        for user in User.select():
            await message.answer(text=get_tuser_info(user=user),
                                 reply_markup=get_tuser_keyboard(user=user))
