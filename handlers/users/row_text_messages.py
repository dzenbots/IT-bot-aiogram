from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from handlers.users import check_valid_tuser
from loader import dp
from utils.db_api import User
from keyboards.inline import get_main_inline_keyboard
from utils.help_functions import user_add_new_group


@dp.message_handler(Text(equals=['На главную']))
async def show_main_menu(message: Message):
    if await check_valid_tuser(message=message, group_name='Users'):
        user = User.get(telegram_id=message.chat.id)
        await message.answer(text='Список доступных Вам функций:', reply_markup=get_main_inline_keyboard(user=user))


@dp.message_handler(content_types=['text'])
async def reply_row_text(message: Message):
    if await check_valid_tuser(message=message, group_name='Users'):
        user = User.get(telegram_id=message.chat.id)
        if user.status == '':
            await message.answer(
                text='Воспользуйтесь кнопками для доступа к функциям или используйте вспомогательные команды (/help)')
        else:
            if user.status == 'adding new group':
                await user_add_new_group(message=message, group_name=message.text)
            elif user.status == 'some new status':
                pass
    else:
        await message.answer(text='Дождитесь пока администратор авторизует Вас!')
