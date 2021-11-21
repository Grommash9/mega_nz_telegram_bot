from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import config


def default_reply_keyboard(user_id):
    default_reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    my_list_button = KeyboardButton(text='My list')
    default_reply_keyboard_markup.add(my_list_button)
    if user_id == config.owner_id:
        add_manager = KeyboardButton(text='Add manager')
        remove_manager = KeyboardButton(text='Remove manager')
        manager_list = KeyboardButton(text='Manager list')
        default_reply_keyboard_markup.add(manager_list)
        default_reply_keyboard_markup.add(add_manager)
        default_reply_keyboard_markup.insert(remove_manager)
    return default_reply_keyboard_markup


def delete_button(file_id):
    delete_button_keyboard = InlineKeyboardMarkup()
    delete_button = InlineKeyboardButton(text='delete', callback_data=f'del_{file_id}')
    delete_button_keyboard.add(delete_button)
    return delete_button_keyboard