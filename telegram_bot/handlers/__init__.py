from telegram_bot.handlers.register import register_handlers_register
from telegram_bot.handlers.menu import register_handlers_menu

def register_handlers_client(dp):
    register_handlers_register(dp)
    register_handlers_menu(dp)

