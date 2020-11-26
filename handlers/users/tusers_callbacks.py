from aiogram.types import CallbackQuery

from handlers.users.help_functions import check_valid
from keyboards.inline.Tuser_buttons import get_groups_list_to_add_keyboard
from keyboards.inline.Tuser_callback_datas import tuser_callback_datas, add_to_group_datas, rm_from_group_datas
from loader import dp
from utils.db_api import Links, User, Group


@dp.callback_query_handler(tuser_callback_datas.filter(func='add_Tuser'))
async def choose_group_to_add_user_to(call: CallbackQuery, callback_data: dict):
    if await check_valid(message=call.message, group_name='Admins'):
        await call.answer(cache_time=1)
        user_id_to_add = callback_data.get('user_id')
        await call.message.edit_text('В какую группу добавить пользователя?')
        await call.message.edit_reply_markup(reply_markup=get_groups_list_to_add_keyboard(user_id_to_add=user_id_to_add))


@dp.callback_query_handler(add_to_group_datas.filter())
async def add_tuser_to_group(call: CallbackQuery, callback_data: dict):
    if await check_valid(message=call.message, group_name='Admins'):
        await call.answer(cache_time=1)
        user = User.get(id=callback_data.get('user_id'))
        group = Group.get(id=callback_data.get('group_id'))
        Links.get_or_create(user=user,
                            group=group)
        if user in User.select(User).join(Links).join(Group).where(Group.group_name == 'Unauthorized'):
            Links.get(user=user, group=Group.get(group_name='Unauthorized')).delete_instance()

        await call.message.edit_text(text=f'Пользователь {user.telegram_id} авторизован и добавлен в группу {group.group_name}')
        await dp.bot.send_message(chat_id=user.telegram_id,
                                  text=f'Вы были авторизованы и добавлены в группу {group.group_name}')


@dp.callback_query_handler(rm_from_group_datas.filter())
async def rm_user_from_group(call: CallbackQuery, callback_data: dict):
    if await check_valid(message=call.message, group_name='Admins'):
        await call.answer(cache_time=1)
        user = User.get(id=callback_data.get('user_id'))
        group = Group.get(id=callback_data.get('group_id'))
        Links.get(user=user, group=group).delete_instance()
        if Group.select(Group).join(Links).join(User).where(User.id == user.id).count() < 1:
            Links.get_or_create(user=user, group=Group.get(group_name='Unauthorized'))
