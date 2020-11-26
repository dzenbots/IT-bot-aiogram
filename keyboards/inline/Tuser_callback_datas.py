from aiogram.utils.callback_data import CallbackData

tuser_callback_datas = CallbackData('Tuser', 'func', 'user_id')

add_to_group_datas = CallbackData('TAdd', 'group_id', 'user_id')

rm_from_group_datas = CallbackData('TRm', 'group_id', 'user_id')
