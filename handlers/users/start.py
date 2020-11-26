from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from .help_functions import isValidUser, is_private


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if not is_private(chat=message.chat):
        return
    telegram_user = message.from_user
    if not await isValidUser(telegram_user):
        await message.answer(
            text=f'Вы не авторизованный пользователь! Сообщите администратору код {telegram_user.id} для получения доступа к функциям этого бота.')
    else:
        await message.answer(f'Привет, {message.from_user.full_name}!')
