from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data.config import PHONE_SPREADSHEET_ID
from loader import dp
from utils import check_valid_tuser
from utils.GoogleSheetsAPI import GoogleSync
from utils.db_api.models import Person
from utils.misc import rate_limit


@rate_limit(5, 'phones_update')
@dp.message_handler(Command('phones_update'))
async def phones_update(message: Message):
    if await check_valid_tuser(message=message, group_name='PhonesAdmin'):
        cur_persons_count = Person.select().count()
        persons_from_google = GoogleSync(spreadsheet_id=PHONE_SPREADSHEET_ID). \
            read_range(list_name='База контактов',
                       range_in_list=f'A{cur_persons_count + 2}:F')

        if persons_from_google is not None:
            for person in persons_from_google:
                if len(person) < 7:
                    for j in range(len(person), 7):
                        person.append('')
                Person.get_or_create(
                    phone=f'+{person[4].strip()}',
                    defaults={
                        'name': person[1].strip(),
                        'surname': person[0].strip(),
                        'patronymic': person[2].strip(),
                        'position': person[3].strip(),
                        'email': person[5].strip(),
                        'photo': '',
                        'actual': person[6].strip()
                    })
        await message.answer(text='Данные получены')
