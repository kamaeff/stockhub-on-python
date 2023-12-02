from telegram import InlineKeyboardButton

main_keyboard = [
            [
                InlineKeyboardButton(
                    "🔎 Поиск пары", callback_data="choose"),
                InlineKeyboardButton("⚡️ Show Room", callback_data="show"),
            ],
            [InlineKeyboardButton("📝 Поиск по артиклу",
                                  callback_data="srrticul")],

            [InlineKeyboardButton(
                "✌🏼 Мой профиль", callback_data="profile")],
        ]

