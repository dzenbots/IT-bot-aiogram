from aiogram.types import Message

from loader import dp
from utils import check_valid_tuser
from utils.db_api import User, Person
from utils.help_functions import send_person_info_to_google_sheet, send_person_info


@dp.message_handler(content_types=['photo'])
async def reply_photo(message: Message):
    if await check_valid_tuser(message=message, group_name='Users'):
        user = User.get(telegram_id=message.chat.id)
        if user.status == '':
            await message.answer(
                text='Воспользуйтесь кнопками для доступа к функциям или используйте вспомогательные команды (/help)')
        else:
            print('here')
            if user.status.split(':')[0] == 'edit_person' and user.status.split(':')[1] == 'photo':
                if await check_valid_tuser(message=message, group_name='PhonesAdmin'):
                    photo_id = message.photo[0].file_id
                    Person.update(photo=photo_id).where(Person.id == int(user.status.split(':')[2])).execute()
                    person = Person.get(id=int(user.status.split(':')[2]))
                    send_person_info_to_google_sheet(person=person)
                    await message.answer(text='Данные успешно обновлены')
                    await send_person_info(message=message, person=person)
