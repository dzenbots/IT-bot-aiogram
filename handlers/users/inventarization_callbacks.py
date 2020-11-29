from aiogram.types import CallbackQuery

from keyboards.inline import main_inventarization_callback
from loader import dp
from utils import check_valid_tuser
from utils.db_api import User


# Обработка нажатия кнопки "Инвентарный номер" в блоке "Посик оборудования"
@dp.callback_query_handler(main_inventarization_callback.filter(parameter='invent_num'))
async def ask_for_invent_number(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Inventarization') or \
            await check_valid_tuser(message=call.message, group_name='Zavhoz'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='invent_search').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите искомый инвентарный номер')


# Обработка нажатия кнопки "Серийный номер" в блоке "Посик оборудования"
@dp.callback_query_handler(main_inventarization_callback.filter(parameter='serial_num'))
async def ask_for_invent_number(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Inventarization') or \
            await check_valid_tuser(message=call.message, group_name='Zavhoz'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='serial_search').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите серийный инвентарный номер')
