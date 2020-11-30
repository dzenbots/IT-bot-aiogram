from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import Equipment

main_inventarization_callback = CallbackData('inventarization', 'parameter')

main_inventarization_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Инвентарный номер', callback_data=main_inventarization_callback.new(
                parameter='invent_num',
            )),
        ],
        [
            InlineKeyboardButton(text='Серийный номер', callback_data=main_inventarization_callback.new(
                parameter='serial_num'
            )),
        ]
    ]
)

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


move_equipment_callback = CallbackData('move_equipment', 'equipment_id', 'campus')


def get_movement_keyboard(equipment: Equipment):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='УК 1', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='1'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 2', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='2'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 3', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='3'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 4', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='4'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 5', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='5'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 6', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='6'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 7', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='7'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 8', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='8'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 9', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='9'
                ))
            ],
            [
                InlineKeyboardButton(text='УК 10', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='10'
                ))
            ],
            [
                InlineKeyboardButton(text='Списание', callback_data=move_equipment_callback.new(
                    equipment_id=equipment.id,
                    campus='spisanie'
                ))
            ],
        ]
    )
