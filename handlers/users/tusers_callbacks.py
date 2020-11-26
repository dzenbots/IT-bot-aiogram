from aiogram.types import CallbackQuery

from handlers.users.help_functions import is_private, isValidUser
from keyboards.inline.Tuser_buttons import get_groups_list_to_add_keyboard
from keyboards.inline.Tuser_callback_datas import tuser_callback_datas
from loader import dp


@dp.callback_query_handler(tuser_callback_datas.filter(func='add_Tuser'))
async def add_tuser_to_group(call: CallbackQuery, callback_data: dict):
    if not is_private(call.message.chat):
        await call.answer(cache_time=1)
        return
    telegram_user = call.message.from_user
    if not await isValidUser(telegram_user=telegram_user, group_name='Admins'):
        await call.answer(text='У Вас нет доступа к этой функции!')
        return
    await call.answer(cache_time=1)
    user_id_to_add = callback_data.get('user_id')
    await call.message.edit_text('В какую группу добавить пользователя?')
    await call.message.edit_reply_markup(reply_markup=get_groups_list_to_add_keyboard(user_id_to_add=user_id_to_add))
