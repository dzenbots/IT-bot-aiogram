import time

from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from loguru import logger

from data.config import INVENTARIZATION_SPREADSHEET_ID
from keyboards.inline import get_main_inline_keyboard, group_function_keyboard, get_equipment_reply_markup
from loader import dp
from utils import check_valid_tuser, get_equipment_info
from utils.GoogleSheetsAPI import GoogleSync
from utils.db_api import User, Group, Equipment, Movement, Person
from utils.help_functions import send_person_info, send_person_info_to_google_sheet


# Добавляет пользователя бота в группу
async def adding_new_group(message: Message, group_name: str):
    if await check_valid_tuser(message=message, group_name='Admins'):
        user = User.get(telegram_id=message.chat.id)
        new_group, created = Group.get_or_create(group_name=group_name)
        if not created:
            logger.info(f'User {user.telegram_id} tried to add an existing group {new_group.group_name} one more time')
            await message.answer(text='Группа с таким именем уже существует')
            await message.answer(text='Выбите действие',
                                 reply_markup=group_function_keyboard)
        else:
            logger.info(f'User {user.telegram_id} added new group {new_group.group_name}')
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
                f'User {user.telegram_id} looking for unexisting equipment with {looking_invent_num} invent number')
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
                f'User {user.telegram_id} looking for unexisting equipment with {looking_serial_num} invent number')
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
        user = User.get(telegram_id=message.chat.id)
        send_equipment_info_to_google_sheet(equipment)
        logger.info(f'User {user.telegram_id} changed type of equipment {equipment.it_id}')
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


# Изменение марки в оборудовании
async def edit_equipment_mark(message: Message, equipment_id: str):
    if await check_valid_tuser(message=message, group_name='Inventarization'):
        Equipment.update(mark=message.text).where(Equipment.id == int(equipment_id)).execute()
        equipment = Equipment.get(id=int(equipment_id))
        user = User.get(telegram_id=message.chat.id)
        send_equipment_info_to_google_sheet(equipment)
        logger.info(f'User {user.telegram_id} changed mark of equipment {equipment.it_id}')
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


# Изменение модели в оборудовании
async def edit_equipment_model(message: Message, equipment_id: str):
    if await check_valid_tuser(message=message, group_name='Inventarization'):
        Equipment.update(model=message.text).where(Equipment.id == int(equipment_id)).execute()
        equipment = Equipment.get(id=int(equipment_id))
        user = User.get(telegram_id=message.chat.id)
        send_equipment_info_to_google_sheet(equipment)
        logger.info(f'User {user.telegram_id} changed model of equipment {equipment.it_id}')
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


# Изменение серийного номера в оборудовании
async def edit_equipment_serial(message: Message, equipment_id: str):
    if await check_valid_tuser(message=message, group_name='Inventarization'):
        Equipment.update(serial_num=message.text).where(Equipment.id == int(equipment_id)).execute()
        equipment = Equipment.get(id=int(equipment_id))
        user = User.get(telegram_id=message.chat.id)
        send_equipment_info_to_google_sheet(equipment)
        logger.info(f'User {user.telegram_id} changed serial number of equipment {equipment.it_id}')
        await message.answer(text=get_equipment_info(equipment),
                             reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                                 message=message, group_name='Inventarization') else None)


def send_movement_to_google_sheet(equipment: Equipment, movement: Movement):
    GoogleSync(spreadsheet_id=INVENTARIZATION_SPREADSHEET_ID).write_data_to_range(list_name='Перемещение оборудования',
                                                                                  range_in_list=f'A{movement.id + 1}:C{movement.id + 1}',
                                                                                  data=[
                                                                                      [
                                                                                          str(equipment.it_id),
                                                                                          str(movement.campus),
                                                                                          str(movement.room)
                                                                                      ]
                                                                                  ])


# def send_person_info_to_google_sheet(person: Person):
#     GoogleSync(spreadsheet_id=PHONE_SPREADSHEET_ID).write_data_to_range(list_name='База контактов',
#                                                                         range_in_list=f'A{person.id + 1}:H{person.id + 1}',
#                                                                         data=[
#                                                                             [
#                                                                                 str(person.surname),
#                                                                                 str(person.name),
#                                                                                 str(person.patronymic),
#                                                                                 str(person.position),
#                                                                                 str(person.photo),
#                                                                                 str(person.phone),
#                                                                                 str(person.email),
#                                                                                 str(person.actual)
#                                                                             ]
#                                                                         ])
#

# Создание нового списания
async def make_spisanie(message: Message, equipment_id: str):
    equipment = Equipment.get(id=int(equipment_id))
    movement = Movement.create(equipment=equipment,
                               campus='Списание',
                               room=message.text)
    send_movement_to_google_sheet(equipment=equipment, movement=movement)
    user = User.get(telegram_id=message.chat.id)
    logger.info(f'User {user.telegram_id} move equipment {equipment.it_id} to spisanie')
    await message.answer(text=get_equipment_info(equipment),
                         reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                             message=message, group_name='Inventarization') else None)


# Создание нового перемещения
async def make_movement(message: Message, equipment_id: str, campus: str):
    equipment = Equipment.get(id=int(equipment_id))
    movement = Movement.create(equipment=equipment,
                               campus=campus,
                               room=message.text)
    send_movement_to_google_sheet(equipment=equipment, movement=movement)
    user = User.get(telegram_id=message.chat.id)
    logger.info(f'User {user.telegram_id} move equipment {equipment.it_id} to campus {campus} room message.text')
    await message.answer(text=get_equipment_info(equipment),
                         reply_markup=get_equipment_reply_markup(equipment) if await check_valid_tuser(
                             message=message, group_name='Inventarization') else None)


# Поиск человека в телефонном справочнике по ФИО
async def phone_search(message: Message, search_parameter: str):
    if search_parameter == 'phone':
        found_person = None
        try:
            found_person = Person.get(phone=message.text)
        except:
            await message.answer(text='Я никого не нашел по указанным параметрам поиска')
            return
        await send_person_info(message=message, person=found_person)
    elif search_parameter == 'fio':
        found_persons = []
        search_depth = len(message.text.split(' '))
        found_person = Person.select().where(Person.surname == message.text.split(' ')[0].title())
        surname_found_persons = []
        if found_person.count() > 0:
            for person in found_person:
                surname_found_persons.append(person)
        if search_depth == 1:
            found_persons = surname_found_persons
        else:
            name_found_persons = []
            for person in surname_found_persons:
                if person.name == message.text.split(' ')[1].title():
                    name_found_persons.append(person)
            if search_depth == 2:
                found_persons = name_found_persons
            else:
                patronymic_found_persons = []
                search_patronymic = message.text.replace(f"{message.text.split(' ')[0]} {message.text.split(' ')[1]}",
                                                         '').title()
                for person in name_found_persons:
                    if person.patronymic == search_patronymic:
                        patronymic_found_persons.append(person)
                found_persons = patronymic_found_persons
        if not found_persons:
            await message.answer(text='Я никого не нашел по указанным параметрам поиска')
        else:
            for person in found_persons:
                await send_person_info(message=message, person=person)
                time.sleep(1)


async def edit_person_info(message, edit_parameter, person_id):
    if await check_valid_tuser(message=message, group_name='PhonesAdmin'):
        if edit_parameter == 'photo':
            await message.answer(
                text='Для изменения фото контакта необходимо прислать фотографию а не текстовое сообщение')
            return
        if edit_parameter == 'surname':
            Person.update(surname=message.text).where(Person.id == int(person_id)).execute()
        elif edit_parameter == 'name':
            Person.update(name=message.text).where(Person.id == int(person_id)).execute()
        elif edit_parameter == 'patronymic':
            Person.update(patronymic=message.text).where(Person.id == int(person_id)).execute()
        elif edit_parameter == 'phone':
            Person.update(phone=message.text).where(Person.id == int(person_id)).execute()
        elif edit_parameter == 'position':
            Person.update(position=message.text).where(Person.id == int(person_id)).execute()
        elif edit_parameter == 'email':
            Person.update(email=message.text).where(Person.id == int(person_id)).execute()
        await message.answer(text='Данные успешно обновлены')
        person = Person.get(id=int(person_id))
        send_person_info_to_google_sheet(person=person)
        await send_person_info(message=message, person=person)


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
                await adding_new_group(message=message, group_name=message.text)
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
            elif user.status.split(':')[0] == 'spisanie':
                equipment_id = user.status.split(':')[1]
                await make_spisanie(message=message, equipment_id=equipment_id)
            elif user.status.split(':')[0] == 'move_equipment':
                equipment_id = user.status.split('/')[0].split(':')[1]
                campus = user.status.split(':')[2]
                await make_movement(message=message, equipment_id=equipment_id, campus=campus)
            elif user.status.split(':')[0] == 'phone_search':
                parameter = user.status.split(':')[1]
                await phone_search(message=message, search_parameter=parameter)
            elif user.status.split(':')[0] == 'phone_search':
                parameter = user.status.split(':')[1]
                person_id = user.status.split(':')[2]
                await edit_person_info(message=message, edit_parameter=parameter, person_id=person_id)
            User.update(status='').where(User.id == user.id).execute()
    else:
        await message.answer(text='Дождитесь пока администратор авторизует Вас!')
