from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

group_list_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Список групп', callback_data='')
        ]
    ]
)