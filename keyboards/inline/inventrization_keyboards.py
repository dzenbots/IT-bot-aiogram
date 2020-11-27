from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

main_inventarization_callback = CallbackData('inventarization', 'parameter')

main_inventarization_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Инвентарный номер', callback_data=main_inventarization_callback.new(
                parameter='invent_num',
            )),
        ],
        [
            InlineKeyboardButton(text='Серийный номер', callback_data=main_inventarization_callback.new(
                parameter='serial_num'
            )),
        ]
    ]
)
