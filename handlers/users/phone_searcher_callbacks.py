from aiogram.types import CallbackQuery

from keyboards.inline import phone_searcher_callback, klass_ruk_seracher_keyboard, klass_ruk_searcher_callback
from keyboards.inline.phones_searcher_keyboards import person_activation_callback, get_person_keyboard, \
    person_edit_callback, get_edit_person_keyboard
from loader import dp
# Обработка нажатия кнопки "Фамилия" в блоке "Телефонный справочник"
from utils import check_valid_tuser
from utils.db_api import User
from utils.db_api.models import Person
from utils.help_functions import send_person_info


@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='fio'))
async def main_surname_search(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Users'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='phone_search:fio').where(User.id == user.id).execute()
        await call.message.edit_text(
            text='Введите фамилию/фамилию и имя/фамилию, имя и отчетво (что известно) искомого человека')


# Обработка нажатия кнопки "Номер телефона" в блоке "Телефонный справочник"
@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='phone'))
async def main_name_search(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Users'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status='phone_search:phone').where(User.id == user.id).execute()
        await call.message.edit_text(
            text='Введите искомыйномер телефона в международном формате, начиная с +7. Например, +79161234567')


# Обработка нажатия кнопки "Классный руководитель" в блоке "Телефонный справочник"
@dp.callback_query_handler(phone_searcher_callback.filter(search_parameter='klass_ruk'))
async def main_klass_ruk_search(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Users'):
        await call.message.edit_text(text='Выберите класс, классного руководителя которого Вы ищите:',
                                     reply_markup=klass_ruk_seracher_keyboard)


# Обработка нажатия кнопки выбора класса в блоке "Телефонный справочник" -> "Классный руководитель"
@dp.callback_query_handler(klass_ruk_searcher_callback.filter())
async def klass_ruk_search(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Users'):
        user = User.get(telegram_id=call.message.chat.id)
        klass_name = callback_data.get('klass_name')
        position = f'Классный руководитель {klass_name}'
        person_is_found = False
        for person in Person.select():
            if position in person.position:
                await send_person_info(person=person, message=call.message)
                person_is_found = True
                break
        if not person_is_found:
            await call.bot.send_message(chat_id=user.telegram_id, text='Я не нашел искомого Вами контакта')


# Изменить отображение контакта при поиске
@dp.callback_query_handler(person_activation_callback.filter())
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        Person.update(actual=callback_data.get('is_visible')).where(
            Person.id == int(callback_data.get('person_id'))).execute()
        person = Person.get(id=int(callback_data.get('person_id')))
        await call.message.edit_reply_markup(get_person_keyboard(person=person))


# Обработка нажатия кнопки "Изменить" у найденного контактаконтакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='_'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await dp.bot.send_message(chat_id=call.message.chat.id,
                                  text='Выберите параметр для редактирования:',
                                  reply_markup=get_edit_person_keyboard(person=person))


# Обработка нажатия кнопки "Фамилия" в блоке Изменить у найденного контакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='surname'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await call.message.edit_text(text='Введите новую фамилию')
        User.update(status=f'edit_person:surname:{person.id}').where(User.telegram_id == call.message.chat.id).execute()


# Обработка нажатия кнопки "Имя" в блоке Изменить у найденного контакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='name'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await call.message.edit_text(text='Введите новое имя')
        User.update(status=f'edit_person:name:{person.id}').where(User.telegram_id == call.message.chat.id).execute()


# Обработка нажатия кнопки "Отчество" в блоке Изменить у найденного контакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='patronymic'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await call.message.edit_text(text='Введите новое отчество')
        User.update(status=f'edit_person:patronymic:{person.id}').where(
            User.telegram_id == call.message.chat.id).execute()


# Обработка нажатия кнопки "Телефон" в блоке Изменить у найденного контакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='phone'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await call.message.edit_text(text='Введите новый номер телефона в международном формате без +. Например 79161234567')
        User.update(status=f'edit_person:phone:{person.id}').where(
            User.telegram_id == call.message.chat.id).execute()


# Обработка нажатия кнопки "Фото" в блоке Изменить у найденного контакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='photo'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await call.message.edit_text(text='Пришлите новое фото')
        User.update(status=f'edit_person:photo:{person.id}').where(
            User.telegram_id == call.message.chat.id).execute()


# Обработка нажатия кнопки "Должность" в блоке Изменить у найденного контакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='position'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await call.message.edit_text(text='Введите новую должность')
        User.update(status=f'edit_person:position:{person.id}').where(
            User.telegram_id == call.message.chat.id).execute()


# Обработка нажатия кнопки "E-mail" в блоке Изменить у найденного контакта
@dp.callback_query_handler(person_edit_callback.filter(parameter='email'))
async def change_person_activity(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='PhonesAdmin'):
        person = Person.get(id=callback_data.get('person_id'))
        await call.message.edit_text(text='Введите новый e-mail')
        User.update(status=f'edit_person:email:{person.id}').where(
            User.telegram_id == call.message.chat.id).execute()
