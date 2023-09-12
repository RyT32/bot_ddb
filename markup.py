#markup.py
from telebot import types

# 1  создание клавиатуры
keyboard_admin = types.InlineKeyboardMarkup()

# 2  создание кнопок
adm_btn1 = types.InlineKeyboardButton(text="all user", callback_data='all_user' )
adm_btn2 = types.InlineKeyboardButton(text="ban user", callback_data='ban_user' )
adm_btn3 = types.InlineKeyboardButton(text="unban user", callback_data='unban_user' )


# 3  добавление кнопок в клавиатуру

keyboard_admin.add(
    adm_btn1,
    adm_btn2,
    adm_btn3
)