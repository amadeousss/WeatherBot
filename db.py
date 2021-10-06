import sqlite3

def is_in_table(userid):
        sqlite_connection= sqlite3.connect('database.db', timeout=20)
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT * from users"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        sqlite_connection.close()
        print(records)
        for row in records:
            if str(row[1]) == str(userid):
                return True
        return False

def db_table_val(user_id: int, user_name: str, user_city: str):
    try:
        sqlite_connection= sqlite3.connect('database.db', timeout=20)
        cursor = sqlite_connection.cursor()
        cursor.execute('INSERT INTO users (user_id, user_name, user_city) VALUES (?, ?, ?)', (user_id, user_name, user_city))
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print("1 Ошибка при подключении к sqlite", error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def db_update_value(userid, usercity):
     try:
        sqlite_connection= sqlite3.connect('database.db', timeout=20)
        cursor = sqlite_connection.cursor()
        sql_update_query = f"Update users set user_city = '{usercity}' where user_id = {userid}"
        cursor.execute(sql_update_query)
        sqlite_connection.commit()

     except sqlite3.Error as error:
        print("2 Ошибка при подключении к sqlite", error)

     finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
