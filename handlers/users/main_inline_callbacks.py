from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.inline import main_inventarization_keyboard
from keyboards.inline import main_phone_searcher_keyboard
from loader import dp
from utils import check_valid_tuser
from utils.db_api import User


# Обработка нажатия кнопки "Поиск оборудования"
@dp.callback_query_handler(Text(equals='main_inventarization'))
async def main_inventarization(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Inventarization') or \
            await check_valid_tuser(message=call.message, group_name='Zavhoz'):
        user = User.get(telegram_id=call.message.chat.id)
        await call.message.edit_text(text='Выберите параметр поиска', reply_markup=main_inventarization_keyboard)


# Обработка нажатия кнопки "Телефонный справочник"
@dp.callback_query_handler(Text(equals='main_phones_searcher'))
async def main_phone_searcher(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Users'):
        await call.message.edit_text(text='Выберите параметр поиска', reply_markup=main_phone_searcher_keyboard)
