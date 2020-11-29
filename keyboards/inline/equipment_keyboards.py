from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import Equipment

edit_equipment_callback = CallbackData('edit_equipment', 'equipment_id', 'parameter')


def get_equipment_reply_markup(equipment: Equipment):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Изменить данные', callback_data=edit_equipment_callback.new(
                    equipment_id=equipment.id,
                    parameter='_'
                ))
            ],
            [
                InlineKeyboardButton(text='Переместить', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='_'
                ))
            ]
        ]
    )


move_equipment_callback = CallbackData('edit_equipment', 'equipment_id', 'campus')


def parameter_to_edit_equipment_keyboard(equipment: Equipment):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Тип', callback_data=edit_equipment_callback.new(
                    equipment_id=equipment.id,
                    parameter='type'
                ))
            ],
            [
                InlineKeyboardButton(text='Марка', callback_data=edit_equipment_callback.new(
                    equipment_id=equipment.id,
                    parameter='mark'
                ))
            ],
            [
                InlineKeyboardButton(text='Модель', callback_data=edit_equipment_callback.new(
                    equipment_id=equipment.id,
                    parameter='model'
                ))
            ],
            [
                InlineKeyboardButton(text='Серийный номер', callback_data=edit_equipment_callback.new(
                    equipment_id=equipment.id,
                    parameter='serial_num'
                ))
            ]
        ]
    )
