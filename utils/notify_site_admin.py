import asyncio

import aioschedule

from data.config import admins


async def send_test_message(dp, message='test'):
    for admin in admins:
        await dp.bot.send_message(admin, message)


async def scheduler(dp):
    aioschedule.every().day.at('18:05').do(send_test_message, dp=dp, message='test message')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)