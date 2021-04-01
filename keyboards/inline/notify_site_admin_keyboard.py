from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_update_siteadmin_keyboard():
    inline_keyboard = list()
    inline_keyboard.append([
        InlineKeyboardButton(text='✅ Обновить',
                             callback_data='update_menu')
    ])
    inline_keyboard.append([
        InlineKeyboardButton(text='❌ Отмена',
                             callback_data='no_update')
    ])
    ret_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    return ret_keyboard


def get_replace_siteadmin_keyboard():
    inline_keyboard = list()
    inline_keyboard.append([
        InlineKeyboardButton(text='✅ Заменить',
                             callback_data='replace_menu')
    ])
    inline_keyboard.append([
        InlineKeyboardButton(text='❌ Отмена',
                             callback_data='no_replace')
    ])
    ret_keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    return ret_keyboard
