from aiogram.types import Message
from loguru import logger

from data.config import admins
from keyboards.inline.phones_searcher_keyboards import get_person_keyboard
from keyboards.inline.tuser_keyboard import get_add_tuser_keyboard
from loader import dp
from utils.db_api import User, Links, Group, Equipment, Movement
# Получить информацию о пользователе, подключавшимся когда-либо к боту
from utils.db_api.models import Person


def get_tuser_info(user: User):
    groups_list = ""
    for group in Group.select(Group).join(Links).join(User).where(User.id == user.id):
        groups_list += group.group_name + ', '
    return f"""Информация о пользователе:
ID: {user.id}
Фамилия: {user.last_name}
Имя: {user.first_name}
Username: {user.username}
Groups: {groups_list}
"""


# Получить информацию по команде /help для пользователя
def get_help_message(user: User):
    text = ''
    if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'Admins'):
        text += '/all_users - Информация о подключавшихся пользователях\n\n'
        text += '/groups - действия с группами пользователей\n\n'

    if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'Inventarization'):
        text += '/equipments_update - подгрузить новое оборудование из таблицы Инвентаризация\n\n'

    if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'PhonesAdmin'):
        text += '/phones_update - подгрузить новых сотрудников в телефонный справочник'

    if text == '':
        text = '<b>У Вас пока нет никаких вспомогательных функций</b>'
    else:
        text = '<b>Список доступных вспомогательных функций</b>\n\n' + text
    return text


# Проверить чат, написал боту аккаунт человека или сообщение полученно из группы/канала
def is_private(chat):
    if chat.type == 'private':
        return True
    return False


# Проверить валидность пользователя. Находится ли он в группе, которой доступен требуемый функционал
async def is_valid_user(telegram_chat, group_name='Users'):
    try:
        user = User.get(telegram_id=str(telegram_chat.id))
    except Exception:
        # Если пользователь новый, то администраторам будет отправлено сообщение о новом подключении,
        # а пользователь останется ожидать авторизации от администратора
        logger.info('New unauthorized user connection!')
        user, created = User.get_or_create(telegram_id=telegram_chat.id,
                                           first_name=telegram_chat.first_name,
                                           last_name=telegram_chat.last_name,
                                           username=telegram_chat.username,
                                           status='')
        Links.get_or_create(user=user,
                            group=Group.get(group_name='Unauthorized'))
        for admin in admins:
            await dp.bot.send_message(chat_id=admin,
                                      text=f'Новый пользователь!')
            await dp.bot.send_message(chat_id=admin,
                                      text=get_tuser_info(user=user),
                                      reply_markup=get_add_tuser_keyboard(user=user))
        return False
    if user not in User.select(User).join(Links).join(Group).where(Group.group_name == group_name):
        # Если пользователь не находится в группе, указанной в аргументах
        logger.info(
            f'User id: {user.telegram_id} name: {user.first_name} {user.last_name} try to use unallowed function!')
        return False
    return True


async def check_valid_tuser(message: Message, group_name='Admins'):
    if not is_private(message.chat):
        return False
    if not await is_valid_user(telegram_chat=message.chat, group_name=group_name):
        await message.answer(text='У Вас нет доступа к этой функции!')
        return False
    return True


def get_equipment_info(equipment: Equipment):
    ret_str = 'Информация об оборудовании\n'
    ret_str += f'ID: {equipment.it_id}\n'
    ret_str += f'Инвентарный номер: {equipment.invent_num}\n'
    ret_str += f'Тип: {equipment.type}\n'
    ret_str += f'Марка: {equipment.mark}\n'
    ret_str += f'Модель: {equipment.model}\n'
    ret_str += f'Серийный номер: {equipment.serial_num}\n\n'
    try:
        movements = Movement.select().where(Movement.equipment == equipment)
        movement = None
        for item in movements:
            movement = item
        ret_str += f'Корпус: {movement.campus}\n'
        ret_str += f'Кабинет: {movement.room}\n'
    except:
        ret_str += 'Корпус: N/A\n'
        ret_str += 'Кабинет: N/A\n'
    return ret_str


def get_person_info(person: Person):
    ret_str = f'ФИО: {person.surname} {person.name} {person.patronymic}\n'
    ret_str += f'Должность: {person.position}\n'
    if not person.email == '':
        ret_str += f'E-mail: {person.email}'
    return ret_str


def get_person_vcard(person: Person):
    vcf = 'BEGIN:VCARD\nVERSION:3.0\n'
    vcf += 'N:' + f'{person.surname};{person.name};{person.patronymic}' + "\n"
    vcf += 'ORG:' + 'ГБОУ Школа \" Дмитровский\"' + "\n"
    vcf += 'TEL;CELL:' + person.phone + "\n"
    if not person.email == '':
        vcf += 'EMAIL:' + person.email + "\n"
    vcf += 'END:VCARD' + "\n\n"
    return vcf


async def send_person_info(person: Person, message: Message):
    if not person.photo == '':
        await dp.bot.send_photo(chat_id=message.chat.id,
                                photo=person.photo,
                                caption=get_person_info(person=person))
    await dp.bot.send_message(chat_id=message.chat.id,
                              text=get_person_info(person=person),
                              reply_markup=get_person_keyboard(person=person) if check_valid_tuser(message=message,
                                                                                                   group_name='PhonesAdmin') else None)
    if not person.phone == '':
        await dp.bot.send_contact(chat_id=message.chat.id,
                                  phone_number=f'+{person.phone}',
                                  first_name=f'{person.surname} {person.name}',
                                  last_name=f'{person.patronymic}',
                                  vcard=get_person_vcard(person=person))
