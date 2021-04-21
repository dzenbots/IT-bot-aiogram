import asyncio

import aioschedule

from keyboards.inline import get_update_siteadmin_keyboard, get_replace_siteadmin_keyboard
from utils.db_api import User, Links, Group


async def send_update_menu_notification(dp, message='test'):
    for user in User.select(User).join(Links).join(Group).where(Group.group_name == 'SiteAdmin'):
        await dp.bot.send_message(chat_id=user.telegram_id,
                                  text=message,
                                  reply_markup=get_update_siteadmin_keyboard())


async def send_replace_menu_notification(dp, message='test'):
    for user in User.select(User).join(Links).join(Group).where(Group.group_name == 'SiteAdmin'):
        await dp.bot.send_message(chat_id=user.telegram_id,
                                  text=message,
                                  reply_markup=get_replace_siteadmin_keyboard())


async def scheduler(dp):
    aioschedule.every().day.at('17:45').do(send_update_menu_notification,
                                           dp=dp,
                                           message='Обновить меню на завтра?')
    aioschedule.every().day.at('08:55').do(send_replace_menu_notification,
                                           dp=dp,
                                           message='Заменить сегодняшнее меню на завтрашнее?')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
