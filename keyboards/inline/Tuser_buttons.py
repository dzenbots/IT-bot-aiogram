from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.Tuser_callback_datas import tuser_callback_datas


def get_add_tuser_keyboard(telegram_user):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить в группу', callback_data=tuser_callback_datas.new(
                    func='add_Tuser',
                    user_id=str(telegram_user.id)
                ))
            ]
        ]
    )


def get_Tuser_keyboard(telegram_user):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить в группу', callback_data=Tuser_callback_datas.new(
                    func='add_Tuser',
                    user_id=str(telegram_user.id)
                )),
                InlineKeyboardButton(text='Удалить из группы', callback_data=Tuser_callback_datas.new(
                    func='rm_Tuser',
                    user_id=str(telegram_user.id)
                ))
            ]
        ]
    )
