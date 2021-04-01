# Обработка нажатия кнопки "Поиск оборудования"
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from loader import dp
from utils import check_valid_tuser
from utils.db_api import User


@dp.callback_query_handler(Text(equals='main_inventarization'))
async def main_inventarization(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)
