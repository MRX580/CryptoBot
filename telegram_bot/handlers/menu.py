from aiogram.types import ReplyKeyboardMarkup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegram_bot.database.sqlite import telegram_database
from telegram_bot.create_tg import bot

class menuState(StatesGroup):
    settings = State()
    stats = State()
    logs = State()
    start = State()

class settingsState(StatesGroup):
    set_profit = State()
    set_procent = State()
    set_general_money = State()
    set_piece = State()

async def help(message: types.Message):
    await bot.send_message(message.chat.id, 'Навигатор всего бота - /menu')


async def menu(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    markup.add('settings', 'stats', 'logs', 'start_work')
    bot.send_message(message.chat.id, 'start_work - начать работу бота(сделать остановку)\n'
                                      'settings - настройки бота\n'
                                      'stats - статистика бота\n'
                                      'logs - все ордера', markup=markup)


async def settings(message: types.Message):
    pass


async def stats(message: types.Message):
    bot.send_message(message.chat.id, 'В разработке')
    pass


async def logs(message: types.Message):
    bot.send_message(message.chat.id, 'В разработке')
    pass


async def start_work(message: types.Message):
    bot.send_message(message.chat.id, 'В разработке')
    pass


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.register_message_handler(settings, lambda msg: msg.text.lower() == 'settings')
    dp.register_message_handler(stats, lambda msg: msg.text.lower() == 'stats')
    dp.register_message_handler(logs, lambda msg: msg.text.lower() == 'logs')
    dp.register_message_handler(start_work, lambda msg: msg.text.lower() == 'start_work')