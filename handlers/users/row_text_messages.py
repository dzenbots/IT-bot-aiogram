from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from handlers.users import check_valid_tuser
from loader import dp
from utils.db_api import User
from keyboards.inline import get_main_inline_keyboard


@dp.message_handler(Text(equals=['На главную']))
async def show_main_menu(message: Message):
    if await check_valid_tuser(message=message, group_name='Users'):
        user = User.get(telegram_id=message.chat.id)
        await message.answer(text='Список доступных Вам функций:', reply_markup=get_main_inline_keyboard(user=user))
