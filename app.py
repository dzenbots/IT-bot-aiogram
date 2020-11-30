async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from utils.db_api import initialize_db, Person

    initialize_db()
    # Person.drop_table()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
