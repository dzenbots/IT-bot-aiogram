from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

phone_searcher_callback = CallbackData('phone_searcher', 'search_parameter', 'value')

main_phone_searcher_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Фамилия', callback_data=phone_searcher_callback.new(
                search_parameter='surname',
                value='_'
            )),
        ],
        [
            InlineKeyboardButton(text='Имя Отчество', callback_data=phone_searcher_callback.new(
                search_parameter='name',
                value='_'
            )),
        ],
        [
            InlineKeyboardButton(text='Классный руководитель', callback_data=phone_searcher_callback.new(
                search_parameter='klass_ruk',
                value='_'
            )),
        ],
    ]
)