import datetime
import os

from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from loguru import logger
from prettytable import PrettyTable

from loader import dp
from utils import check_valid_tuser
from utils.Menu_worker.mail_worker import MailWorker, IMAP_SERVER, DIRECTORY_TO_SAVE_FILES, MENU_FOLDER_NAME, LOGIN, \
    PASSWORD, PdfCompressor
from utils.Menu_worker.mail_worker.mail_worker import get_public_key
from utils.Menu_worker.site_worker import SiteWorker, BASE_SCHOOL_SITE_ADDR, SITE_LOGIN, SITE_PASSWORD, \
    TOMORROW_MENU_FOLDER_PATH_IN_SITE_STORAGE, ROOT_FOLDER
from utils.db_api import User


@dp.callback_query_handler(Text(equals='update_menu'))
async def update_menu_callback(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)
        mw = MailWorker(server=IMAP_SERVER,
                        save_dir=DIRECTORY_TO_SAVE_FILES,
                        menu_folder_name=MENU_FOLDER_NAME)
        if not mw.authorize(login=LOGIN,
                            password=PASSWORD):
            await dp.bot.edit_message_text(text='Ошибка авторизации на почтовом сервере',
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id,
                                           reply_markup=None)
            return
        folder_list = mw.get_folder_list()
        if folder_list is None:
            await dp.bot.edit_message_text(text='Ошибка получения списка папок на почтовом сервере',
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
            return
        if MENU_FOLDER_NAME not in folder_list:
            await dp.bot.edit_message_text(text='Папка с меню не найдена на почтовом сервере',
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
            return
        if not mw.select_folder(MENU_FOLDER_NAME):
            await dp.bot.edit_message_text(text=f'Проблема с открытием папки {MENU_FOLDER_NAME}',
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
            return
        messages = mw.get_messages_from_folder()
        if not messages:
            await dp.bot.edit_message_text(text='Новых писем с меню нет',
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
            return
        table = PrettyTable(['ID', 'Тема письма', 'Дата получения письма', 'Отправитель'])
        for message in mw.get_messages_from_folder():
            with open(os.path.join(DIRECTORY_TO_SAVE_FILES, str(message.subject.uk) + '.pdf'), "wb") as fp:
                fp.write(message.file.content)
                fp.close()
            table.add_row(
                [str(message.id), message.subject.uk + ' ' + str(message.subject.date), message.date,
                 message.from_user])
        logger.info(table)
        sw = SiteWorker(base_url=BASE_SCHOOL_SITE_ADDR,
                        login=SITE_LOGIN,
                        password=SITE_PASSWORD)
        sw.delete_all_in_folder(folder_path=TOMORROW_MENU_FOLDER_PATH_IN_SITE_STORAGE)
        for filename in os.listdir('./Menus'):
            pdf_compressor = PdfCompressor(public_api_key=get_public_key(datetime.date.today()))
            pdf_compressor.compress_file(filepath=os.path.join('./Menus/', filename),
                                         output_directory_path='./Menus_small')
        if sw.authorized:
            sw.upload_file(folder_path=TOMORROW_MENU_FOLDER_PATH_IN_SITE_STORAGE,
                           files=[os.path.join('./Menus_small', file) for file in os.listdir('./Menus_small')],
                           root_folder_id=ROOT_FOLDER)
        await dp.bot.edit_message_text(text='Меню размещены',
                                       chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       reply_markup=None)

        # mw.disconnect()

@dp.callback_query_handler(Text(equals='no_update_menu'))
async def cancel_update_menu_callback(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)


@dp.callback_query_handler(Text(equals='replace_menu'))
async def replace_menu_callback(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)


@dp.callback_query_handler(Text(equals='no_replace_menu'))
async def cancel_replace_menu_callback(call: CallbackQuery):
    await call.answer(cache_time=1)
    if await check_valid_tuser(message=call.message, group_name='SiteAdmin'):
        user = User.get(telegram_id=call.message.chat.id)
