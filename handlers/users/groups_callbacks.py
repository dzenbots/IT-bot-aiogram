from aiogram.types import CallbackQuery
from loguru import logger

from handlers.users.help_functions import check_valid_tuser
from loader import dp
from utils.db_api import Group, User


@dp.callback_query_handler(text_contains='group_list')
async def show_all_groups(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        group_list = Group.select()
        ret_list = ''
        for group in group_list:
            ret_list += group.group_name + '\n'
        await call.message.edit_text(text='Список существующих групп:\n\n' + ret_list)


@dp.callback_query_handler(text_contains='add_group')
async def add_new_groups(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        user = User.get(telegram_id=call.message.chat.id)
        User.update(status="adding new group").where(User.id == user.id)
        await call.message.edit_text(text='Введите имя новой группы')
