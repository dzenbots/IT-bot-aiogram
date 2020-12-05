from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import Person

phone_searcher_callback = CallbackData('phone_searcher', 'search_parameter')

main_phone_searcher_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Фамилия', callback_data=phone_searcher_callback.new(
                search_parameter='surname'
            )),
        ],
        [
            InlineKeyboardButton(text='Имя Отчество', callback_data=phone_searcher_callback.new(
                search_parameter='name'
            )),
        ],
        [
            InlineKeyboardButton(text='Номер телефона', callback_data=phone_searcher_callback.new(
                search_parameter='phone'
            )),
        ],
        [
            InlineKeyboardButton(text='Классный руководитель', callback_data=phone_searcher_callback.new(
                search_parameter='klass_ruk'
            )),
        ],
    ]
)

klass_ruk_searcher_callback = CallbackData('klass_ruk_search', 'klass_name')

klass_ruk_seracher_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        # 1 классы
        [
            InlineKeyboardButton(text='1А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='1А'
            )),
            InlineKeyboardButton(text='1Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='1Б'
            )),
            InlineKeyboardButton(text='1В', callback_data=klass_ruk_searcher_callback.new(
                klass_name='1В'
            )),
            InlineKeyboardButton(text='1Г', callback_data=klass_ruk_searcher_callback.new(
                klass_name='1Г'
            )),
            InlineKeyboardButton(text='1Д', callback_data=klass_ruk_searcher_callback.new(
                klass_name='1Д'
            )),
            InlineKeyboardButton(text='1М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='1М'
            )),
            InlineKeyboardButton(text='1Н', callback_data=klass_ruk_searcher_callback.new(
                klass_name='1Н'
            )),
        ],
        # 2 классы
        [
            InlineKeyboardButton(text='2А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='2А'
            )),
            InlineKeyboardButton(text='2Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='2Б'
            )),
            InlineKeyboardButton(text='2В', callback_data=klass_ruk_searcher_callback.new(
                klass_name='2В'
            )),
            InlineKeyboardButton(text='2Г', callback_data=klass_ruk_searcher_callback.new(
                klass_name='2Г'
            )),
            InlineKeyboardButton(text='2Д', callback_data=klass_ruk_searcher_callback.new(
                klass_name='2Д'
            )),
            InlineKeyboardButton(text='2Л', callback_data=klass_ruk_searcher_callback.new(
                klass_name='2Л'
            )),
            InlineKeyboardButton(text='2М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='2М'
            )),
        ],
        # 3 классы
        [
            InlineKeyboardButton(text='3А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='3А'
            )),
            InlineKeyboardButton(text='3Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='3Б'
            )),
            InlineKeyboardButton(text='3В', callback_data=klass_ruk_searcher_callback.new(
                klass_name='3В'
            )),
            InlineKeyboardButton(text='3Л', callback_data=klass_ruk_searcher_callback.new(
                klass_name='3Л'
            )),
            InlineKeyboardButton(text='3М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='3М'
            )),
            InlineKeyboardButton(text='3У', callback_data=klass_ruk_searcher_callback.new(
                klass_name='3У'
            )),
        ],
        # 4 классы
        [
            InlineKeyboardButton(text='4А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='4А'
            )),
            InlineKeyboardButton(text='4Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='4Б'
            )),
            InlineKeyboardButton(text='4В', callback_data=klass_ruk_searcher_callback.new(
                klass_name='4В'
            )),
            InlineKeyboardButton(text='4Г', callback_data=klass_ruk_searcher_callback.new(
                klass_name='4Г'
            )),
            InlineKeyboardButton(text='4Л', callback_data=klass_ruk_searcher_callback.new(
                klass_name='4Л'
            )),
            InlineKeyboardButton(text='4М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='4М'
            )),
            InlineKeyboardButton(text='4У', callback_data=klass_ruk_searcher_callback.new(
                klass_name='4У'
            )),
        ],
        # 5 классы
        [
            InlineKeyboardButton(text='5А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='5А'
            )),
            InlineKeyboardButton(text='5Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='5Б'
            )),
            InlineKeyboardButton(text='5В', callback_data=klass_ruk_searcher_callback.new(
                klass_name='5В'
            )),
            InlineKeyboardButton(text='5Д', callback_data=klass_ruk_searcher_callback.new(
                klass_name='5Д'
            )),
            InlineKeyboardButton(text='5Л', callback_data=klass_ruk_searcher_callback.new(
                klass_name='5Л'
            )),
            InlineKeyboardButton(text='5М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='5М'
            )),
            InlineKeyboardButton(text='5Н', callback_data=klass_ruk_searcher_callback.new(
                klass_name='5Н'
            )),
        ],
        # 6 классы
        [
            InlineKeyboardButton(text='6А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='6А'
            )),
            InlineKeyboardButton(text='6Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='6Б'
            )),
            InlineKeyboardButton(text='6В', callback_data=klass_ruk_searcher_callback.new(
                klass_name='6В'
            )),
            InlineKeyboardButton(text='6Г', callback_data=klass_ruk_searcher_callback.new(
                klass_name='6Г'
            )),
            InlineKeyboardButton(text='6Д', callback_data=klass_ruk_searcher_callback.new(
                klass_name='6Д'
            )),
            InlineKeyboardButton(text='6Л', callback_data=klass_ruk_searcher_callback.new(
                klass_name='6Л'
            )),
            InlineKeyboardButton(text='6М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='6М'
            )),
        ],
        # 7 классы
        [
            InlineKeyboardButton(text='7А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='7А'
            )),
            InlineKeyboardButton(text='7Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='7Б'
            )),
            InlineKeyboardButton(text='7Г', callback_data=klass_ruk_searcher_callback.new(
                klass_name='7Г'
            )),
            InlineKeyboardButton(text='7К', callback_data=klass_ruk_searcher_callback.new(
                klass_name='7К'
            )),
            InlineKeyboardButton(text='7М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='7М'
            )),
            InlineKeyboardButton(text='7Н', callback_data=klass_ruk_searcher_callback.new(
                klass_name='7Н'
            )),
        ],
        # 8 классы
        [
            InlineKeyboardButton(text='8И', callback_data=klass_ruk_searcher_callback.new(
                klass_name='8И'
            )),
            InlineKeyboardButton(text='8К', callback_data=klass_ruk_searcher_callback.new(
                klass_name='8К'
            )),
            InlineKeyboardButton(text='8М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='8М'
            )),
            InlineKeyboardButton(text='8С', callback_data=klass_ruk_searcher_callback.new(
                klass_name='8С'
            )),
            InlineKeyboardButton(text='8Э', callback_data=klass_ruk_searcher_callback.new(
                klass_name='8Э'
            )),
            InlineKeyboardButton(text='8Я', callback_data=klass_ruk_searcher_callback.new(
                klass_name='8Я'
            )),
        ],
        # 9 классы
        [
            InlineKeyboardButton(text='9А', callback_data=klass_ruk_searcher_callback.new(
                klass_name='9А'
            )),
            InlineKeyboardButton(text='9Б', callback_data=klass_ruk_searcher_callback.new(
                klass_name='9Б'
            )),
            InlineKeyboardButton(text='9В', callback_data=klass_ruk_searcher_callback.new(
                klass_name='9В'
            )),
            InlineKeyboardButton(text='9Г', callback_data=klass_ruk_searcher_callback.new(
                klass_name='9Г'
            )),
            InlineKeyboardButton(text='9К', callback_data=klass_ruk_searcher_callback.new(
                klass_name='9К'
            )),
            InlineKeyboardButton(text='9Л', callback_data=klass_ruk_searcher_callback.new(
                klass_name='9Л'
            )),
            InlineKeyboardButton(text='9М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='9М'
            )),
        ],
        # 10 классы
        [
            InlineKeyboardButton(text='10И', callback_data=klass_ruk_searcher_callback.new(
                klass_name='10И'
            )),
            InlineKeyboardButton(text='10К', callback_data=klass_ruk_searcher_callback.new(
                klass_name='10К'
            )),
            InlineKeyboardButton(text='10М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='10М'
            )),
        ],
        # 11 классы
        [
            InlineKeyboardButton(text='11И', callback_data=klass_ruk_searcher_callback.new(
                klass_name='11И'
            )),
            InlineKeyboardButton(text='11К', callback_data=klass_ruk_searcher_callback.new(
                klass_name='11К'
            )),
            InlineKeyboardButton(text='11М', callback_data=klass_ruk_searcher_callback.new(
                klass_name='11М'
            )),
        ],
    ]
)

person_activation_callback = CallbackData('person_visible', 'person_id', 'is_visible')
person_edit_callback = CallbackData('person_edit', 'person_id', 'parameter')


def get_person_keyboard(person: Person):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Изменить', callback_data=person_edit_callback.new(
                    person_id=person.id,
                    parameter='_'
                )),
                InlineKeyboardButton(text='Видимый ✅' if person.actual == 'True' else 'Невидимый ❌',
                                     callback_data=person_activation_callback.new(
                                         person_id=person.id,
                                         is_visible='True'
                                     ))
            ]
        ]
    )
