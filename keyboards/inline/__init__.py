# from .equipment_keyboards import get_equipment_reply_markup, edit_equipment_callback, move_equipment_callback, \
#     parameter_to_edit_equipment_keyboard, get_movement_keyboard
from .groups_list_keyboard import group_function_keyboard, group_callback_datas, group_list_to_chose_rm
from .inventrization_keyboards import main_inventarization_keyboard, main_inventarization_callback, \
    get_equipment_reply_markup, edit_equipment_callback, move_equipment_callback, \
    parameter_to_edit_equipment_keyboard, get_movement_keyboard
from .main_inline_keyboard import get_main_inline_keyboard
from .phones_searcher_keyboards import main_phone_searcher_keyboard, phone_searcher_callback, \
    klass_ruk_seracher_keyboard, klass_ruk_searcher_callback
from .tuser_keyboard import get_add_tuser_keyboard, get_tuser_keyboard, get_groups_list_to_add_keyboard, \
    get_groups_list_to_rm_keyboard, tuser_callback_datas, add_to_group_datas, rm_from_group_datas, edit_tuser_datas, \
    get_edit_tuser_keyboard
from .notify_site_admin_keyboard import get_update_siteadmin_keyboard, get_replace_siteadmin_keyboard
