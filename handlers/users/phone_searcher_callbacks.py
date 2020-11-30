from aiogram.types import CallbackQuery

from keyboards.inline import phone_searcher_callback
from loader import dp


# Обработка нажатия кнопки "Фамилия" в блоке "Телефонный справочник"
from utils import check_valid_tuser


@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='surname'))
async def main_surname_search(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        pass


# Обработка нажатия кнопки "Имя отчество" в блоке "Телефонный справочник"
@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='name'))
async def main_name_search(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        pass


# Обработка нажатия кнопки "Классный руководитель" в блоке "Телефонный справочник"
@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='klass_ruk'))
async def main_klass_ruk_search(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        pass
