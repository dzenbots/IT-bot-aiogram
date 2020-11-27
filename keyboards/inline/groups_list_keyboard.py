from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import Group

group_function_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Список существующих групп', callback_data='group_list')
        ],
        [
            InlineKeyboardButton(text='Добавить группу', callback_data='add_group')
        ],
        [
            InlineKeyboardButton(text='Удалить группу', callback_data='rm_group')
        ],
    ]
)

group_callback_datas = CallbackData('group_remove', 'group_id')


def group_list_to_chose_rm():
    group_list = Group.select()
    inline_keyboard = []
    for group in group_list:
        inline_keyboard.append([
            InlineKeyboardButton(text=group.group_name, callback_data=group_callback_datas.new(
                group_id=group.id
            ))
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
