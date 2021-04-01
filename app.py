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


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    asyncio.create_task(scheduler(dp))


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from utils.db_api import initialize_db, Person, User

    initialize_db()
    # Person.drop_table()
    # User.drop_table()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
