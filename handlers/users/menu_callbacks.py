import os

from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from prettytable import PrettyTable

from loader import dp
from utils import check_valid_tuser
from utils.Menu_worker.mail_worker import MailWorker, IMAP_SERVER, DIRECTORY_TO_SAVE_FILES, MENU_FOLDER_NAME, LOGIN, \
    PASSWORD
from utils.db_api import User


@dp.callback_query_handler(Text(equals='update_menu'))
async def main_inventarization(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)
        mw = MailWorker(server=IMAP_SERVER,
                        save_dir=DIRECTORY_TO_SAVE_FILES,
                        menu_folder_name=MENU_FOLDER_NAME)
        if not mw.authorize(login=LOGIN,
                            password=PASSWORD):
            return
        folder_list = mw.get_folder_list()
        if folder_list is None:
            print("Ошибка при получении списка папок")
            return
        if MENU_FOLDER_NAME not in folder_list:
            print('Папка с меню не найдена. Завешение работы')
            return
        if not mw.select_folder(MENU_FOLDER_NAME):
            print('Проблема с открытием папки ' + MENU_FOLDER_NAME)
            return
        messages = mw.get_messages_from_folder()
        if not messages:
            print('Нет сообщений с файлами меню')
            return
        table = PrettyTable(['ID', 'Тема письма', 'Дата получения письма', 'Отправитель'])
        for message in mw.get_messages_from_folder():
            with open(os.path.join(DIRECTORY_TO_SAVE_FILES, str(message.subject.uk) + '.pdf'), "wb") as fp:
                fp.write(message.file.content)
                fp.close()
            table.add_row(
                [str(message.id), message.subject.uk + ' ' + str(message.subject.date), message.date,
                 message.from_user])
        print(table)
        # mw.disconnect()


@dp.callback_query_handler(Text(equals='no_update_menu'))
async def main_inventarization(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)


@dp.callback_query_handler(Text(equals='replace_menu'))
async def main_inventarization(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)


@dp.callback_query_handler(Text(equals='no_replace_menu'))
async def main_inventarization(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)
