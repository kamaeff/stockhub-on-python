import mysql.connector
from mysql.connector import errors
from src.config import HOST, USER, PASSWORD, DATABASE
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class ProfileManager:
    def __init__(self, query):
        self.query = query

        self.db_config = {
            'host': HOST,
            'user': USER,
            'password': PASSWORD,
            'database': DATABASE,
            'port': 3306
        }

    def create_connection(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection:
                print(
                    f"Успешное подключение к MySQL серверу (версия {connection.get_server_info()})")
                return connection
            else:
                print(f"Ошибка подключения к MySQL серверу")
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def return_profile_data(self):
        try:
            connection = self.create_connection()
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM users WHERE chat_id = %s',
                           (str(self.query.from_user.id),))
            columns = [col[0] for col in cursor.description]
            result = cursor.fetchall()
        # Создаем список словарей, где каждый словарь представляет одну строку данных
            data = [dict(zip(columns, row)) for row in result]
            return data
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    async def edit_profile_caption(self):
        print(self.db_config)
        print(self.query.from_user.id)

        user_data = self.return_profile_data()
        print(user_data)

        await self.query.edit_message_caption(
            caption=f"📈 <b>Вот твоя стата {self.query.message.chat.first_name}:</b>\n\n"+
            f"● <b>ФИО:</b> <i>{user_data[0]['FIO']}</i>\n"+
            f"● <b>Всего заказов сделано:</b> <i>{user_data[0]['orders_count']}</i>\n"+
            f"● <b>Бонусы:</b> <i>{user_data[0]['bonus_count']}</i>\n"+
            f"● <b>Способ доставки:</b> <i>{user_data[0]['locale']}</i>\n"+
            f"● <b>Email:</b> <i>{user_data[0]['email']}</i>\n",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("⏳ История заказов", callback_data="data_orders"),],
                    [InlineKeyboardButton("📦 Обновить адрес", callback_data="locale"),],
                    [InlineKeyboardButton('🏠 Выход в главное меню', callback_data="exit")]
                ]),
        )
