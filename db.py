import sqlite3

# 1 - подключение к БД (connect)
# 2 - создание курсора  (cursor) для запросов к БД
# 3 - запросы( execute)
# 4 - закрытие или сохранение бд


###################################################    создаем таблицу
# CREATE TABLE *название_таблицы*(
#   *название поля* *тип поля* *доп параметры(первичный ключ, уникальное значение и тд)*,
#   *название поля* *тип поля* *доп параметры(первичный ключ, уникальное значение и тд)*,
# 
# )

class DataBase:
    def __init__(self) -> None:
        self.con = sqlite3.connect("user.sqlite", check_same_thread=False)# подключение
        # con = sqlite3.connect(r"C:\Users\User\Desktop\bot_ddb\user.sqlite")
        self.cur = self.con.cursor()#  создание курсора  (cursor) для запросов к БД


        # CREATE TABLE IF NOT EXISTS  - создание таблицы если она еще не создана

        self.cur.execute("""CREATE TABLE IF NOT EXISTS user(
                    id INT PRIMARY KEY,
                    name TEXT,
                    is_ban INT
        )
        """)  # # запрос к БД

            #is_ban = 0 - ЭТО НЕ БАН
            #is_ban = 1 - ЭТО БАН

        self.con.commit()  # сохранение
        print("Таблица была создана")


    ###################################################    добавляем пользователя
    #INSERT INTO *название таблицы* VALUES (*то что добавляем*)

    def add_user(self, id, name, is_ban):
        #   ? - потом подставлю значение под этот знак
        self.cur.execute("INSERT INTO user VALUES (?, ?, ?)", (id, name, is_ban))
        self.con.commit()  # сохранение



    ###################################################    проверяю пользователя на бан 
    # SELECT *то что хотим извлечь* FROM *название таблицы*

    def check_ban_user(self,id):
        #   ? - потом подставлю значение под этот знак
        self.cur.execute("SELECT is_ban FROM user WHERE id=?", (id,))

        data = self.cur.fetchone()# извлекаю все записи из БД

        return data # возвращаю данные из функции (1,) (0,) 

    ###################################################    извлекаем  всех пользователей 
    # SELECT *то что хотим извлечь* FROM *название таблицы*

    def select_users(self):
        #   ? - потом подставлю значение под этот знак
        self.cur.execute("SELECT * FROM user ")

        data = self.cur.fetchall()# извлекаю все записи из БД

        return data # возвращаю данные из функции [(1, 'pavel', 0), (2, 'oleg', 0), (3, 'olga', 0), (4, 'alex', 0)]

    ###################################################    извлекаем  всех забаненых пользователей 
    # SELECT *то что хотим извлечь* FROM *название таблицы*

    def select_ban_users(self):
        #   ? - потом подставлю значение под этот знак
        self.cur.execute("SELECT * FROM user WHERE is_ban=1")

        data = self.cur.fetchall()# извлекаю все записи из БД

        return data # возвращаю данные из функции [(1, 'pavel', 0), (2, 'oleg', 0), (3, 'olga', 0), (4, 'alex', 0)]

 ###################################################    извлекаем  всех не забаненых пользователей 
    # SELECT *то что хотим извлечь* FROM *название таблицы*

    def select_unban_users(self):
        #   ? - потом подставлю значение под этот знак
        self.cur.execute("SELECT * FROM user WHERE is_ban=0")

        data = self.cur.fetchall()# извлекаю все записи из БД

        return data # возвращаю данные из функции [(1, 'pavel', 0), (2, 'oleg', 0), (3, 'olga', 0), (4, 'alex', 0)]



    ###################################################   ищу пользователя
    # SELECT *то что хотим извлечь* FROM *название таблицы*

    def select_id_user(self, id):
        #   ? - потом подставлю значение под этот знак
        self.cur.execute("SELECT * FROM user WHERE id=? ", (id,))

        data = self.cur.fetchone()# извлекаю все записи из БД

        return data # возвращаю данные из функции (1, 'pavel', 0) or None



    ###################################################    удалить пользователя
    # DELETE FROM *название таблицы* WHERE *условие*
    def delete_user(self, id):
        self.cur.execute("DELETE FROM user WHERE id = ? ", (id,))
        self.con.commit()  # сохранение


    ###################################################    обновить пользователя
    # UPDATE *название таблицы*  SET   *стобец=новое значение*       WHERE *условие*
    def update_name_user(self, id, name):
        self.cur.execute("UPDATE user SET name=?  WHERE id = ? ", (name, id))
        self.con.commit()  # сохранение


    ###################################################    добавляю  пользователя в бан
    # UPDATE *название таблицы*  SET   *стобец=новое значение*       WHERE *условие*
    def add_ban_user(self, id):
        self.cur.execute("UPDATE user SET is_ban=1 WHERE id = ? ", (id,))
        self.con.commit()  # сохранение

    ###################################################    разбан
    # UPDATE *название таблицы*  SET   *стобец=новое значение*       WHERE *условие*
    def unban_user(self, id):
        self.cur.execute("UPDATE user SET is_ban=0 WHERE id = ? ", (id,))
        self.con.commit()  # сохранение

