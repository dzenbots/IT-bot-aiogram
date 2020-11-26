from loguru import logger

from data.config import admins
from keyboards.inline.Tuser_buttons import get_add_tuser_keyboard
from loader import dp
from utils.db_api import User, Links, Group


def is_private(chat):
    if chat.type == 'private':
        return True
    return False


def get_user_info(telegram_user):
    return f"""Информация о пользователе:
ID: {telegram_user.id}
Имя: {telegram_user.full_name}
"""


async def isValidUser(telegram_user, group_name='Users'):
    user = None
    try:
        user = User.get(telegram_id=str(telegram_user.id))
    except Exception as err:
        logger.info('New unauthorized user connection!')
        for admin in admins:
            await dp.bot.send_message(chat_id=admin,
                                      text=f'Новый пользователь!')
            await dp.bot.send_message(chat_id=admin,
                                      text=get_user_info(telegram_user=telegram_user),
                                      reply_markup=get_add_tuser_keyboard(telegram_user=telegram_user))
        return False
    if user not in User.select(User).join(Links).join(Group).where(Group.group_name == group_name):
        logger.info(f'User id: {user.telegram_id} name: {user.first_name} {user.last_name} try to use unallowed function!')
        return False
    return True
