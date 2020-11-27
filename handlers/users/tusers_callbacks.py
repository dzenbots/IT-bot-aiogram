from aiogram.types import CallbackQuery

from utils.help_functions import check_valid_tuser, get_tuser_info
from keyboards.default import main_keyboard
from keyboards.inline import get_groups_list_to_add_keyboard, get_main_inline_keyboard, get_groups_list_to_rm_keyboard, \
    get_tuser_keyboard
from keyboards.inline import tuser_callback_datas, add_to_group_datas, rm_from_group_datas
from loader import dp
from utils.db_api import Links, User, Group


@dp.callback_query_handler(tuser_callback_datas.filter(func='add_Tuser'))
async def choose_group_to_add_user_to(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        await call.answer(cache_time=1)
        user_id_to_add = callback_data.get('user_id')
        user = User.get(id=user_id_to_add)
        await call.message.edit_text(text='В какую группу добавить пользователя?',
                                     reply_markup=get_groups_list_to_add_keyboard(user=user))


@dp.callback_query_handler(tuser_callback_datas.filter(func='rm_Tuser'))
async def choose_group_to_add_user_to(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        await call.answer(cache_time=1)
        user_id_to_add = callback_data.get('user_id')
        user = User.get(id=user_id_to_add)
        await call.message.edit_text(text='Из какой группы удалить пользователя?',
                                     reply_markup=get_groups_list_to_rm_keyboard(user=user))


@dp.callback_query_handler(add_to_group_datas.filter())
async def add_tuser_to_group(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        await call.answer(cache_time=1)
        user = User.get(id=callback_data.get('user_id'))
        group = Group.get(id=callback_data.get('group_id'))
        Links.get_or_create(user=user,
                            group=group)
        if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'Unauthorized'):
            Links.get(user=user, group=Group.get(group_name='Unauthorized')).delete_instance()
        user = User.get(id=callback_data.get('user_id'))
        await call.message.edit_text(text=get_tuser_info(user=user),
                                     reply_markup=get_tuser_keyboard(user=user))
        await dp.bot.send_message(chat_id=user.telegram_id,
                                  text=f'Вы были авторизованы и добавлены в группу {group.group_name}',
                                  reply_markup=main_keyboard)
        await dp.bot.send_message(chat_id=user.telegram_id,
                                  text='Список доступных Вам функций:',
                                  reply_markup=get_main_inline_keyboard(user=user))


@dp.callback_query_handler(rm_from_group_datas.filter())
async def rm_user_from_group(call: CallbackQuery, callback_data: dict):
    if await check_valid_tuser(message=call.message, group_name='Admins'):
        await call.answer(cache_time=1)
        user = User.get(id=callback_data.get('user_id'))
        group = Group.get(id=callback_data.get('group_id'))
        Links.get(user=user, group=group).delete_instance()
        if Group.select(Group).join(Links).join(User).where(User.id == user.id).count() < 1:
            Links.get_or_create(user=user, group=Group.get(group_name='Unauthorized'))
        user = User.get(id=callback_data.get('user_id'))
        await call.message.edit_text(text=get_tuser_info(user=user),
                                     reply_markup=get_tuser_keyboard(user=user))
        await dp.bot.send_message(chat_id=user.telegram_id,
                                  text=f'Вы были удалены из группы {group.group_name}',
                                  reply_markup=main_keyboard)
        await dp.bot.send_message(chat_id=user.telegram_id,
                                  text='Список доступных Вам функций:',
                                  reply_markup=get_main_inline_keyboard(user=user))