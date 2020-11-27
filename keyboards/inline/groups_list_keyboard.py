from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
