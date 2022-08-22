from handlers import register_handlers_client
import logging
from aiogram import executor
from create_tg import dp

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)