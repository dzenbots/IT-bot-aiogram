from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import main_keyboard
from keyboards.inline import get_main_inline_keyboard
from loader import dp
from utils.help_functions import is_valid_user, is_private
from utils.db_api import User


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if not is_private(chat=message.chat):
        return
    telegram_user = message.chat
    if not await is_valid_user(telegram_user):
        await message.answer(
            text=f'Вы не авторизованный пользователь! Сообщите администратору код {telegram_user.id} для получения доступа к функциям этого бота.')
    else:
        await message.answer(text=f'С возвращением {telegram_user.full_name}!', reply_markup=main_keyboard)
        user = User.get(telegram_id=telegram_user.id)
        await message.answer(text='Список доступных Вам функций:', reply_markup=get_main_inline_keyboard(user=user))
