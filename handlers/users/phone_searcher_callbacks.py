from aiogram.types import CallbackQuery

from keyboards.inline import phone_searcher_callback, klass_ruk_seracher_keyboard, klass_ruk_seracher_callback
from loader import dp
# Обработка нажатия кнопки "Фамилия" в блоке "Телефонный справочник"
from utils import check_valid_tuser
from utils.db_api import User
from utils.db_api.models import Person
from utils.help_functions import send_person_info


@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='surname'))
async def main_surname_search(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='phone_search:surname').where(User.id == user.id).execute()
        await call.answer(text='Введите фамилию искомого человека')


# Обработка нажатия кнопки "Имя отчество" в блоке "Телефонный справочник"
@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='name'))
async def main_name_search(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='phone_search:name').where(User.id == user.id).execute()
        await call.answer(text='Введите имя и отчество искомого человека')


# Обработка нажатия кнопки "Номер телефона" в блоке "Телефонный справочник"
@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='name'))
async def main_name_search(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='phone_search:phone').where(User.id == user.id).execute()
        await call.answer(text='Введите искомыйномер телефона')


# Обработка нажатия кнопки "Классный руководитель" в блоке "Телефонный справочник"
@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='klass_ruk'))
async def main_klass_ruk_search(call: CallbackQuery):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        await call.message.edit_text(text='Выберите класс, классного руководителя которого Вы ищите:',
                                     reply_markup=klass_ruk_seracher_keyboard)


# Обработка нажатия кнопки выбора класса в блоке "Телефонный справочник" -> "Классный руководитель"
@dp.callback_query_handler(klass_ruk_seracher_callback.filter())
async def main_klass_ruk_search(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Users'):
        user = User.get(telegram_id=call.message.chat.id)
        klass_name = callback_data.get('klass_name')
        position = f'Классный руководитель {klass_name}'
        await call.message.edit_text(text='Выберите класс, классного руководителя которого Вы ищите:',
                                     reply_markup=klass_ruk_seracher_keyboard)
        founded_persons = Person.select().where(position in Person.position)
        if founded_persons.count() > 0:
            for person in founded_persons:
                await send_person_info(person=person, call=call, dp=dp)
        else:
            await call.answer(text='Я не нашел искомого Вами контакта')
