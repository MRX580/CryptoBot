import binance.exceptions
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from binance.client import Client
from telegram_bot.database.sqlite import telegram_database
from telegram_bot.create_tg import bot, dp

class process(StatesGroup):
    getAPI = State()
    getSecretKey = State()

async def start(message: types.Message):
    await dp.bot.set_my_commands([])
    await process.getAPI.set()
    await bot.send_message(message.chat.id, f'''
    Привет {message.from_user.first_name}\nЧто бы работать с этим ботом тебе понадобиться 
API и Secret_Key подробнее на сайте Binance - https://www.binance.com/ru/support/faq/360002502072
''')
    await bot.send_message(message.chat.id, "После того как вы всё сделали введите - API KEY")


async def enterAPI(message: types.Message, state: FSMContext):
    await state.update_data(API=message.text)
    await bot.send_message(message.chat.id, f'Ваш API_KEY - {message.text}\nДалее введите Secret Key')
    await process.next()


async def enterSecretKey(message: types.Message, state: FSMContext):
    await state.update_data(Secret_Key=message.text)
    await bot.send_message(message.chat.id, f'Ваш Secret_KEY - {message.text}')
    async with state.proxy() as data:
        try:
            Client(data['API'], data['Secret_Key']).get_account()
            telegram_database(message.chat.id).addApis(data['API'], data['Secret_Key'], message.from_user.first_name)
            await bot.send_message(message.chat.id, 'Данные заполнены, можешь приступить к работе\n'
                                                    'Все команды описанны тут - /help')
            await dp.bot.set_my_commands([
                types.BotCommand("menu", "General menu"),
                types.BotCommand("help", "All command"),
            ])
            await state.finish()
        except binance.exceptions.BinanceAPIException:
            await bot.send_message(message.chat.id, 'Неправильно введён API или Secret_Key, повторите попытку')
            await bot.send_message(message.chat.id, 'Введите API KEY')
            await process.getAPI.set()



def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(enterAPI, state=process.getAPI)
    dp.register_message_handler(enterSecretKey, state=process.getSecretKey)