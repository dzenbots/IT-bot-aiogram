from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_inventarization_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Инвентарный номер', callback_data='main_invent_search'),
        ],
        [
            InlineKeyboardButton(text='Серийный номер', callback_data='main_serial_search'),
        ]
    ]
)

