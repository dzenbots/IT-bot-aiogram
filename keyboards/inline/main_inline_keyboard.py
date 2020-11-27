from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import IT_SUPPORT_FORM, IT_SUPPORT_TABLE
from utils.db_api import User, Group, Links


def get_main_inline_keyboard(user: User):
    inline_keyboard = []
    if user in User.select(User).join(Links).join(Group).where(
            Group.group_name == 'Inventarization' or Group.group_name == 'Zavhoz'):
        inline_keyboard.append([
            InlineKeyboardButton(text=' 🔍 Поиск оборудования',
                                 callback_data='main_inventarization')
        ])
    if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'Users'):
        inline_keyboard.append([
            InlineKeyboardButton(text=' ☎️ Телефонный справочник',
                                 callback_data='main_phones_searcher')
        ])
    if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'SysAdmins'):
        inline_keyboard.append([
            InlineKeyboardButton(text=' 📋 Таблица заявок',
                                 url=IT_SUPPORT_TABLE)
        ])
    if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'Users'):
        inline_keyboard.append([
            InlineKeyboardButton(text=' 🆘 Форма обращений в IT-службу',
                                 url=IT_SUPPORT_FORM)
        ])
    ret_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    return ret_keyboard
