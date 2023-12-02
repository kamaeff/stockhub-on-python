import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from src.config import TOKEN
from src.py_func.profile import ProfileManager
from src.py_func.db import connection_check
from src.keyboards import main_keyboard

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        chat_id = update.message.chat_id
        username = update.message.chat.first_name
        message_id = update.message.message_id
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id
        username = update.callback_query.message.chat.first_name
        message_id = update.callback_query.message.message_id
    
    await context.bot.delete_message(chat_id, message_id)
    with open("./src/img/Logo.png", "rb") as f:
        await context.bot.send_photo(
            chat_id,
            f,
            caption=f"<b>✌🏻 Yo {username}! Я бот группы <i><b><a href='https://t.me/stockhub12'>StockHub!</a></b></i></b>\n\n"
            + "⚙️ <b>Кнопки основного меню:</b>\n\n"
            + "➖ <b>Поиск пары</b> - <i>Фильтр поиска пары</i>\n"
            + "➖ <b>ShowRoom</b> - <i>Коллекция магазина</i>\n"
            + "➖ <b>Мой профиль</b> - <i>Инфа о твоем профиле</i>\n"
            + "➖ <b>Обратная связь</b> - <i>help@stockhub12.ru</i>\n\n"
            + "<b><i>💬 Полезное:</i></b> \n"
            + "<i><b><a href='https://telegra.ph/Dogovor-oferty-na-okazanie-uslugi-11-27'>➖ Договор оферты</a></b></i>\n"
            + "➖ /commands <i>(Дополнительные команды)</i>\n\n"
            + "<i><b>Created by: </b><b><a href='https://t.me/YoKrossbot_log'>Anton Kamaev</a></b>.\n<b>Alfa-version.v3</b></i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(main_keyboard),
        )
        
async def update_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
  if update.message:
        chat_id = update.message.chat_id
        username = update.message.chat.first_name
        message_id = update.message.message_id
  elif update.callback_query:
      chat_id = update.callback_query.message.chat_id
      username = update.callback_query.message.chat.first_name
      message_id = update.callback_query.message.message_id
      
  await context.bot.edit_message_caption(
        chat_id=chat_id,
        message_id=message_id,
        caption=f"<b>✌🏻 Yo {username}! Я бот группы <i><b><a href='https://t.me/stockhub12'>StockHub!</a></b></i></b>\n\n"
                + "⚙️ <b>Кнопки основного меню:</b>\n\n"
                + "➖ <b>Поиск пары</b> - <i>Фильтр поиска пары</i>\n"
                + "➖ <b>ShowRoom</b> - <i>Коллекция магазина</i>\n"
                + "➖ <b>Мой профиль</b> - <i>Инфа о твоем профиле</i>\n"
                + "➖ <b>Обратная связь</b> - <i>help@stockhub12.ru</i>\n\n"
                + "<b><i>💬 Полезное:</i></b> \n"
                + "<i><b><a href='https://telegra.ph/Dogovor-oferty-na-okazanie-uslugi-11-27'>➖ Договор оферты</a></b></i>\n"
                + "➖ /commands <i>(Дополнительные команды)</i>\n\n"
                + "<i><b>Created by: </b><b><a href='https://t.me/YoKrossbot_log'>Anton Kamaev</a></b>.\n<b>Alfa-version.v3</b></i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(main_keyboard),
  )


async def main_menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "profile":
        profile_manager = ProfileManager(query)
        await profile_manager.edit_profile_caption()
        
    if query.data == "exit": 
      await update_main_menu(update, context)

def main() -> None:
    connection_check()
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(main_menu_button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
