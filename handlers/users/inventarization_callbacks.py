from aiogram.types import CallbackQuery

from keyboards.inline import main_inventarization_callback, edit_equipment_callback, \
    parameter_to_edit_equipment_keyboard
from loader import dp
from utils import check_valid_tuser
from utils.db_api import User, Equipment


# Обработка нажатия кнопки "Инвентарный номер" в блоке "Поиск оборудования"
@dp.callback_query_handler(main_inventarization_callback.filter(parameter='invent_num'))
async def ask_for_invent_number(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Inventarization') or \
            await check_valid_tuser(message=call.message, group_name='Zavhoz'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='invent_search').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите искомый инвентарный номер')


# Обработка нажатия кнопки "Серийный номер" в блоке "Поиск оборудования"
@dp.callback_query_handler(main_inventarization_callback.filter(parameter='serial_num'))
async def ask_for_serial_number(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Inventarization') or \
            await check_valid_tuser(message=call.message, group_name='Zavhoz'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='serial_search').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите серийный инвентарный номер')


# Обработка нажатия кнопки "Изменить данные" у оборудования
@dp.callback_query_handler(edit_equipment_callback.filter(parameter='_'))
async def choose_parameter_to_edit(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Inventarization'):
        equipment = Equipment.get(id=int(callback_data.get('equipment_id')))
        await call.bot.send_message(chat_id=call.message.chat.id,
                                    text='Выберите параметр оборудования для редактирования',
                                    reply_markup=parameter_to_edit_equipment_keyboard(equipment=equipment))


# Обработка нажатия кнопки "Тип" в блоке "Изменить оборудования"
@dp.callback_query_handler(edit_equipment_callback.filter(parameter='type'))
async def choose_parameter_to_edit(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Inventarization'):
        equipment = Equipment.get(id=int(callback_data.get('equipment_id')))
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status=f'edit_type:{equipment.id}').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите новое название типа оборудования')


# Обработка нажатия кнопки "Марка" в блоке "Изменить оборудования"
@dp.callback_query_handler(edit_equipment_callback.filter(parameter='mark'))
async def choose_parameter_to_edit(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Inventarization'):
        equipment = Equipment.get(id=int(callback_data.get('equipment_id')))
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status=f'edit_mark:{equipment.id}').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите новое название марки оборудования')


# Обработка нажатия кнопки "Модель" в блоке "Изменить оборудования"
@dp.callback_query_handler(edit_equipment_callback.filter(parameter='model'))
async def choose_parameter_to_edit(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Inventarization'):
        equipment = Equipment.get(id=int(callback_data.get('equipment_id')))
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status=f'edit_model:{equipment.id}').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите новое название модели оборудование')


# Обработка нажатия кнопки "Серийный номер" в блоке "Изменить оборудования"
@dp.callback_query_handler(edit_equipment_callback.filter(parameter='serial_num'))
async def choose_parameter_to_edit(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Inventarization'):
        equipment = Equipment.get(id=int(callback_data.get('equipment_id')))
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status=f'edit_serial:{equipment.id}').where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите корректный серийный номер оборудования')

