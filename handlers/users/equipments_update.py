from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from utils import check_valid_tuser
from utils.GoogleSheetsAPI import GoogleSync
from utils.db_api import Equipment, Movement
from utils.misc import rate_limit


@rate_limit(5, 'equipments_update')
@dp.message_handler(Command('equipments_update'))
async def bot_help(message: Message):
    if await check_valid_tuser(message=message, group_name='Inventarization') or \
            await check_valid_tuser(message=message, group_name='Inventarization'):
        cur_equipments = Equipment.select()
        cur_movement = Movement.select()
        gs = GoogleSync()
        equipments_from_google = gs.read_range(list_name='Список оборудования',
                                               range_in_list=f'A{cur_equipments.count() + 2}:G')
        movements_from_google = gs.read_range(list_name='Перемещение оборудования',
                                              range_in_list=f'A{cur_movement.count() + 2}:C')
        if equipments_from_google is not None:
            if len(equipments_from_google) > 0:
                for item in equipments_from_google:
                    if len(item) < 7:
                        for j in range(len(item), 7):
                            item.append('')
                    Equipment.create(it_id=item[0],
                                     pos_in_buh=item[1],
                                     invent_num=item[2],
                                     type=item[3],
                                     mark=item[4],
                                     model=item[5],
                                     serial_num=item[6])
        if movements_from_google is not None:
            if len(movements_from_google) > 0:
                for item in movements_from_google:
                    if len(item) < 7:
                        for j in range(len(item), 7):
                            item.append('')
                    if item[0] == '':
                        continue
                    Movement.create(equipment=Equipment.get(it_id=item[0]),
                                    campus=item[1],
                                    room=item[2])
        await message.answer(text='Данные получены')
