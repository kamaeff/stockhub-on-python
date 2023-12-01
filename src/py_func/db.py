import mysql.connector
from mysql.connector import errors
from src.config import HOST, USER, PASSWORD, DATABASE


def connection_check():
    connection = None  # Предварительное определение переменной

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=3306
        )

        if connection.is_connected():
            print(
                f"Успешное подключение к MySQL серверу (версия {connection.get_server_info()})")

            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_info = cursor.fetchone()
            print(f"Текущая база данных: {db_info[0]}")

    except errors.Error as e:
        print(f"Ошибка подключения: {e}")
