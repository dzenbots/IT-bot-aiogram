from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import Group, User, Links

tuser_callback_datas = CallbackData('Tuser', 'func', 'user_id')

add_to_group_datas = CallbackData('TAdd', 'group_id', 'user_id')

rm_from_group_datas = CallbackData('TRm', 'group_id', 'user_id')


def get_add_tuser_keyboard(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить в группу', callback_data=tuser_callback_datas.new(
                    func='add_Tuser',
                    user_id=str(user.id)
                ))
            ]
        ]
    )


def get_tuser_keyboard(user: User):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить в группу', callback_data=tuser_callback_datas.new(
                    func='add_Tuser',
                    user_id=str(user.id)
                )),
                InlineKeyboardButton(text='Удалить из группы', callback_data=tuser_callback_datas.new(
                    func='rm_Tuser',
                    user_id=str(user.id)
                ))
            ]
        ]
    )


def get_groups_list_to_add_keyboard(user: User):
    inline_keyboard = []
    group_list = Group.select()
    for group in group_list:
        if user not in User.select(User).join(Links).join(Group).where(Group.group_name == group.group_name):
            inline_keyboard.append([
                InlineKeyboardButton(text=group.group_name, callback_data=add_to_group_datas.new(
                    group_id=group.id,
                    user_id=user.id
                ))
            ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_groups_list_to_rm_keyboard(user: User):
    inline_keyboard = []
    group_list = Group.select()
    for group in group_list:
        if user in User.select(User).join(Links).join(Group).where(Group.group_name == group.group_name):
            inline_keyboard.append([
                InlineKeyboardButton(text=group.group_name, callback_data=rm_from_group_datas.new(
                    group_id=group.id,
                    user_id=user.id
                ))
            ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
