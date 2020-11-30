from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from loguru import logger

from data.config import INVENTARIZATION_SPREADSHEET_ID
from keyboards.inline import get_main_inline_keyboard, group_function_keyboard, get_equipment_reply_markup
from loader import dp
from utils import check_valid_tuser, get_equipment_info
from utils.GoogleSheetsAPI import GoogleSync
from utils.db_api import User, Group, Equipment


# Добавляет пользователя бота в группу
async def user_add_new_group(message: Message, group_name: str):
    if await check_valid_tuser(message=message, group_name='Admins'):
        user = User.get(telegram_id=message.chat.id)
        new_group, created = Group.get_or_create(group_name=group_name)
        if not created:
            logger.info(f'User {user.id} tried to add an existing group {new_group.group_name} one more time')
            await message.answer(text='Группа с таким именем уже существует')
            await message.answer(text='Выбите действие',
                                 reply_markup=group_function_keyboard)
        else:
            logger.info(f'User {user.id} added new group {new_group.group_name}')
            await message.answer(text='Группа создана')
            await message.answer(text='Выбите действие',
                                 reply_markup=group_function_keyboard)


# Поиск оборудования по инвентарному номеру
async def make_invent_num_search(message: Message):
    if await check_valid_tuser(message=message, group_name='Inventarization') or \
            await check_valid_tuser(message=message, group_name='Zavhoz'):
        user = User.get(telegram_id=message.chat.id)
        looking_invent_num = message.text
        found_equipments = Equipment.select().where(Equipment.invent_num == looking_invent_num)
        if found_equipments.count() < 1:
            await message.answer(text=f'Оборудование с инвентарным номером {looking_invent_num} не стоит на балансе')
            logger.info(
                f'User {user.id} looking for unexisting equipment with {looking_invent_num} invent number')
        else:
            for item in found_equipments:
                await message.answer(text=get_equipment_info(equipment=item),
                                     reply_markup=get_equipment_reply_markup(equipment=item) if await check_valid_tuser(
                                         message=message, group_name='Inventarization') else None)

# Поиск оборудования по серийному номеру
async def make_serial_num_search(message: Message):
    if await check_valid_tuser(message=message, group_name='Inventarization') or \
            await check_valid_tuser(message=message, group_name='Zavhoz'):
        user = User.get(telegram_id=message.chat.id)
        looking_serial_num = message.text
        found_equipments = Equipment.select().where(Equipment.serial_num == looking_serial_num)
        if found_equipments.count() < 1:
            await message.answer(text=f'Оборудование с серийным номером {looking_serial_num} не стоит на балансе')
            logger.info(
                f'User {user.id} looking for unexisting equipment with {looking_serial_num} invent number')
        else:
            for item in found_equipments:
                await message.answer(text=get_equipment_info(equipment=item),
                                     reply_markup=get_equipment_reply_markup(equipment=item) if await check_valid_tuser(
                                         message=message, group_name='Inventarization') else None)


# Отправка иинформации об оборудовании в Google-таблицу
def send_equipment_info_to_google_sheet(equipment: Equipment):
    GoogleSync(spreadsheet_id=INVENTARIZATION_SPREADSHEET_ID).write_data_to_range(list_name='Список оборудования',
                                                                                  range_in_list=f'A{equipment.id + 1}:G{equipment.id + 1}',
                                                                                  data=[[
                                                                                      str(equipment.it_id),
                                                                                      str(equipment.pos_in_buh),
                                                                                      str(equipment.invent_num),
                                                                                      str(equipment.type),
                                                                                      str(equipment.mark),
                                                                                      str(equipment.model),
                                                                                      str(equipment.serial_num)
                                                                                  ]])


# Изменение типа в оборудовании
async def edit_equipment_type(message: Message, equipment_id: str):
    if await check_valid_tuser(message=message, group_name='Inventarization'):
        Equipment.update(type=message.text).where(Equipment.id == int(equipment_id)).execute()
        equipment = Equipment.get(id=int(equipment_id))
        send_equipment_info_to_google_sheet(equipment)
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


# Изменение марки в оборудовании
async def edit_equipment_mark(message: Message, equipment_id: str):
    if await check_valid_tuser(message=message, group_name='Inventarization'):
        Equipment.update(mark=message.text).where(Equipment.id == int(equipment_id)).execute()
        equipment = Equipment.get(id=int(equipment_id))
        send_equipment_info_to_google_sheet(equipment)
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


# Изменение модели в оборудовании
async def edit_equipment_model(message: Message, equipment_id: str):
    if await check_valid_tuser(message=message, group_name='Inventarization'):
        Equipment.update(model=message.text).where(Equipment.id == int(equipment_id)).execute()
        equipment = Equipment.get(id=int(equipment_id))
        send_equipment_info_to_google_sheet(equipment)
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


# Изменение серийного номера в оборудовании
async def edit_equipment_serial(message: Message, equipment_id: str):
    if await check_valid_tuser(message=message, group_name='Inventarization'):
        Equipment.update(serial_num=message.text).where(Equipment.id == int(equipment_id)).execute()
        equipment = Equipment.get(id=int(equipment_id))
        send_equipment_info_to_google_sheet(equipment)
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


# Показывает пользователю список доступных ему фукнций в зависимости от групп, в которых пользователь состоит
@dp.message_handler(Text(equals=['На главную']))
async def show_main_menu(message: Message):
    if await check_valid_tuser(message=message, group_name='Users'):
        user = User.get(telegram_id=message.chat.id)
        User.update(status='').where(User.id == user.id).execute()
        await message.answer(text='Список доступных Вам функций:', reply_markup=get_main_inline_keyboard(user=user))


# Хендлер всех текстовых сообщений, распределение функций зависит от статуса пользователя
@dp.message_handler(content_types=['text'])
async def reply_row_text(message: Message):
    if await check_valid_tuser(message=message, group_name='Users'):
        user = User.get(telegram_id=message.chat.id)
        if user.status == '':
            await message.answer(
                text='Воспользуйтесь кнопками для доступа к функциям или используйте вспомогательные команды (/help)')
        else:
            if user.status == 'adding new group':
                await user_add_new_group(message=message, group_name=message.text)
            elif user.status == 'invent_search':
                await make_invent_num_search(message=message)
            elif user.status == 'serial_search':
                await make_serial_num_search(message=message)
            elif user.status.split(':')[0] == 'edit_type':
                equipment_id = user.status.split(':')[1]
                await edit_equipment_type(message=message, equipment_id=equipment_id)
            elif user.status.split(':')[0] == 'edit_mark':
                equipment_id = user.status.split(':')[1]
                await edit_equipment_mark(message=message, equipment_id=equipment_id)
            elif user.status.split(':')[0] == 'edit_model':
                equipment_id = user.status.split(':')[1]
                await edit_equipment_model(message=message, equipment_id=equipment_id)
            elif user.status.split(':')[0] == 'edit_serial':
                equipment_id = user.status.split(':')[1]
                await edit_equipment_serial(message=message, equipment_id=equipment_id)
            User.update(status='').where(User.id == user.id).execute()
    else:
        await message.answer(text='Дождитесь пока администратор авторизует Вас!')
