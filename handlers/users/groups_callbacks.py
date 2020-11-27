from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from loguru import logger

from keyboards.inline.groups_list_keyboard import group_list_to_chose_rm, group_callback_datas, group_function_keyboard
from utils.help_functions import check_valid_tuser
from loader import dp
from utils.db_api import Group, User, Links


@dp.callback_query_handler(Text(equals='group_list'))
async def show_all_groups(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        group_list = Group.select()
        ret_list = ''
        for group in group_list:
            ret_list += group.group_name + '\n'
        await call.message.edit_text(text='Список существующих групп:\n\n' + ret_list)


@dp.callback_query_handler(Text(equals='add_group'))
async def add_new_groups(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status="adding new group").where(User.id == user.id).execute()
        await call.message.edit_text(text='Введите имя новой группы')


@dp.callback_query_handler(Text(equals='rm_group'))
async def add_new_groups(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status="removing group").where(User.id == user.id)
        await call.message.edit_text(text='Выберите группу для удаления', reply_markup=group_list_to_chose_rm())


@dp.callback_query_handler(group_callback_datas.filter())
async def remove_group(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        user = User.get(telegram_id=call.message.chat.id)
        group_id_to_remove = callback_data.get('group_id')
        group = Group.get(id=group_id_to_remove)
        for link in Links.select(Links).join(Group).where(Group.id == group.id):
            link.delete_instance()
        group.delete_instance()
        logger.info(f'User {user.id} removed group {group.group_name}')
        await call.message.edit_text(text='Выбите действие',
                                     reply_markup=group_function_keyboard)
