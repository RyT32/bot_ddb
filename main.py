# main.py
import db # мой модуль для БД
import markup # мой модуль для клавиатуры
import telebot # pip install pyTelegramBotAPI
from telebot import types


TOKEN = "5856564999:AAERNXBZIe0PQAJk94FHvoRyf2qRNKAIImY"

bot = telebot.TeleBot(TOKEN)

ADMIN = [1217864060]

database = db.DataBase()



####################################################   команды
# /reg
@bot.message_handler(commands=['reg'])
def register(message):
    print(message)
    id = message.from_user.id
    username = message.from_user.username
    if database.select_id_user(id) is None: # пользователя нет в базе данных
        database.add_user(id,username,0)
        bot.send_message(id, "Успешная регистрация")
    else:
        bot.send_message(id, "Вы уже зарегистрированы")


####################################################   текст
@bot.message_handler(content_types=["text"])
def text_handler(message):
    id = message.from_user.id
    username = message.from_user.username
                            # (1,)   (0,)
    if database.check_ban_user(id)[0] == 1: # проверка бана пользователя
        bot.send_message(id, f"Вы забанены!")
        print("ban")
        return

    if message.text == 'админ' and id in ADMIN:
            bot.send_message(id, f"Приветствую админа!", reply_markup=markup.keyboard_admin )


    # -рассылка Всем привет
    # if message.text.startswith("-рассылка") : # все пользователи

    elif message.text.startswith("-рассылка") and id in ADMIN: # только админы
        text = message.text[10:] # беру текст без '-рассылка'

        users = database.select_users()# [(1, 'pavel', 0), (2, 'oleg', 0), (3, 'olga', 0), (4, 'alex', 0)]

        # user[0] - id
         # user =     (2, 'oleg', 0)
        for user in users:
            bot.send_message(user[0], f"{id} {username} : {text}" )




####################################################   callback
@bot.callback_query_handler(func = lambda call: True) # принимаю все callback
def callback_hander(call):
    id = call.from_user.id
    if call.data == "all_user":
         
        users = database.select_users() # [(1, 'pavel', 0), (2, 'oleg', 0), (3, 'olga', 0), (4, 'alex', 0)]

        # 1  создание клавиатуры
        keyboard_user = types.InlineKeyboardMarkup()


        for user in users:
            # bot.send_message(id,f"{user[0]} - @{user[1]}") # для отображения обычной строкой
            # 2  создание кнопок
            user_btn = types.InlineKeyboardButton(text=f"{user[0]} - {user[1]}", url=f"https://t.me/{user[1]}" )
            # 3  добавление кнопок в клавиатуру
            keyboard_user.add(user_btn)

        bot.send_message(id,"Все пользователи:", reply_markup=keyboard_user)
#############################################################################################################################       ban
    elif call.data == "ban_user":
         
        users = database.select_unban_users() # [(1, 'pavel', 0), (2, 'oleg', 0), (3, 'olga', 0), (4, 'alex', 0)]

        # 1  создание клавиатуры
        keyboard_user = types.InlineKeyboardMarkup()


        for user in users:
            # bot.send_message(id,f"{user[0]} - @{user[1]}") # для отображения обычной строкой
            # 2  создание кнопок
            user_btn = types.InlineKeyboardButton(text=f"{user[0]} - {user[1]}", callback_data=f'ban_{user[0]}' ) # ban_201314
            # 3  добавление кнопок в клавиатуру
            keyboard_user.add(user_btn)

        bot.send_message(id,"Выберите пользователя для бана:", reply_markup=keyboard_user)
    #ban_
    elif call.data.startswith("ban_"):
        id_ban = call.data[4:] #извлекаю id пользователя для бана
        database.add_ban_user(id_ban)
        bot.send_message(id,f"Пользователь {id_ban} забанен!")



#############################################################################################################################       unban

    elif call.data == "unban_user":
         
        users = database.select_ban_users() # [(1, 'pavel', 0), (2, 'oleg', 0), (3, 'olga', 0), (4, 'alex', 0)]

        # 1  создание клавиатуры
        keyboard_user = types.InlineKeyboardMarkup()


        for user in users:
            # bot.send_message(id,f"{user[0]} - @{user[1]}") # для отображения обычной строкой
            # 2  создание кнопок
            user_btn = types.InlineKeyboardButton(text=f"{user[0]} - {user[1]}", callback_data=f'unban_{user[0]}' ) # ban_201314
            # 3  добавление кнопок в клавиатуру
            keyboard_user.add(user_btn)

        bot.send_message(id,"Выберите пользователя для разбана:", reply_markup=keyboard_user)
    #ban_
    elif call.data.startswith("unban_"):
        id_unban = call.data[6:] #извлекаю id пользователя для разбана
        database.unban_user(id_unban)
        bot.send_message(id,f"Пользователь {id_unban} разбанен!")








# цикл бота
bot.polling()
