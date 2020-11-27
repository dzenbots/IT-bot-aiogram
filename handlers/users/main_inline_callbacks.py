from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from loader import dp
from utils.help_functions import check_valid_tuser


@dp.callback_query_handler(Text(equals='main_inventarization'))
async def main_inventarization(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Inventarization'):
        pass


@dp.callback_query_handler(Text(equals='main_phones_searcher'))
async def main_phone_searcher(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='Users'):
        pass
