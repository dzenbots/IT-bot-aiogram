from aiogram.types import Message
from loguru import logger

from data.config import admins
from keyboards.inline import get_add_tuser_keyboard, group_function_keyboard
from loader import dp
from utils.db_api import User, Links, Group


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


def get_help_message(user: User):
    text = ''
    if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'Admins'):
        text += '/all_users - Информация о подключавшихся пользователях\n\n'
        text += '/groups - действия с группами пользователей\n\n'
        text += '/google_update - подгрузить новое оборудование из таблицы Инвентаризация\n\n'
        text += '/phones_update - подгрузить новых сотрудников в телефонный справочник'

    if text == '':
        text = '<b>У Вас пока нет никаких вспомогательных функций</b>'
    else:
        text = '<b>Список доступных вспомогательных функций</b>\n\n' + text
    return text


def is_private(chat):
    if chat.type == 'private':
        return True
    return False


async def is_valid_user(telegram_chat, group_name='Users'):
    try:
        user = User.get(telegram_id=str(telegram_chat.id))
    except Exception:
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
        logger.info(
            f'User id: {user.telegram_id} name: {user.first_name} {user.last_name} try to use unallowed function!')
        return False
    return True


async def check_valid_tuser(message: Message, group_name='Admins'):
    if not is_private(message.chat):
        return False
    telegram_chat = message.chat
    if not await is_valid_user(telegram_chat=telegram_chat, group_name=group_name):
        await message.answer(text='У Вас нет доступа к этой функции!')
        return False
    return True
