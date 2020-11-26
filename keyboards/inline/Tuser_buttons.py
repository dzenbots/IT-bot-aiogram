from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.Tuser_callback_datas import tuser_callback_datas, add_to_group_datas, rm_from_group_datas
from utils.db_api import Group, User, Links


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


def get_groups_list_to_add_keyboard(user_id_to_add: User):
    inline_keyboard = []
    group_list = Group.select()
    for group in group_list:
        if user_id_to_add not in User.select(User).join(Links).join(Group).where(Group.group_name == group.group_name):
            inline_keyboard.append([
                InlineKeyboardButton(text=group.group_name, callback_data=add_to_group_datas.new(
                    group_id=group.id,
                    user_id=user_id_to_add
                ))
            ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_groups_list_to_rm_keyboard(user_to_rm: User):
    inline_keyboard = []
    group_list = Group.select()
    for group in group_list:
        if user_to_rm in User.select(User).join(Links).join(Group).where(Group.group_name == group.group_name):
            inline_keyboard.append(
                InlineKeyboardButton(text=group.group_name, callback_data=rm_from_group_datas.new(
                    group_id=group.id,
                    user_id=user_to_rm.id
                ))
            )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
