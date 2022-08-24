from aiogram.types import ReplyKeyboardMarkup
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegram_bot.database.sqlite import telegram_database
from telegram_bot.create_tg import bot
from aiogram.dispatcher.filters import Text


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
    set_timeframe = State()


cancelMarkup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
cancelMarkup.add('отмена')


async def help(message: types.Message):
    await bot.send_message(message.chat.id, 'Навигатор всего бота - /menu')


async def menu(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    markup.add('settings', 'stats', 'logs', 'start_work')
    await bot.send_message(message.chat.id, 'start_work - начать работу бота(сделать остановку)\n'
                                            'settings - настройки бота\n'
                                            'stats - статистика бота\n'
                                            'logs - все ордера', reply_markup=markup)


async def settingsInterface(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Профит', 'Процент', "Сумму торговли").row("Сумму покупки за сделку", "Таймфрейм").add(
        "Вернуться в меню")
    telegram_client = telegram_database(message.chat.id)
    setting = {'profit': telegram_client.get_profit(),
               'procent': telegram_client.get_procent(),
               'general_money': telegram_client.get_general_money(),
               'piece': telegram_client.get_piece(),
               'timeframe': telegram_client.get_timeframe()
               }
    await bot.send_message(message.chat.id, f'Профит за сделку в процентах(рекомендуемый 1): {setting["profit"]}%\n'
                                            f'Процент который при падении монеты будет докупать монету(рекомендуемый 4+): {setting["procent"]}\n'
                                            f'Сумма на которой бот может торговать: {setting["general_money"]}\n'
                                            f'Сумма на которую бот будет покупать за сделку(миниммум 11$): {setting["piece"]}\n'
                                            f'Выбранный таймфрейм: {setting["timeframe"]}\n\n'
                                            f'Выберите что изменить:', reply_markup=markup)

async def isRegister(message: types.Message):
    await bot.send_message(message.chat.id, 'Сначала нужно зарегистрироваться - /start')

async def settings(message: types.Message):
    await settingsInterface(message)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Вы вернулись обратно в меню', reply_markup=types.ReplyKeyboardRemove())
    await settingsInterface(message)


async def process_invalid(message: types.Message):
    await message.reply("Некорректный ввод")


async def set_profit(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, f'Профит успешно установлен как: {message.text}%')
    telegram_database(message.chat.id).set_profit(message.text)
    await state.finish()
    await settingsInterface(message)


async def profit(message: types.Message):
    await settingsState.set_profit.set()
    await bot.send_message(message.chat.id, 'Введите значение:', reply_markup=cancelMarkup)


async def set_procent(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, f'Процент успешно установлен как: {message.text}%')
    telegram_database(message.chat.id).set_procent(message.text)
    await state.finish()
    await settingsInterface(message)


async def procent(message: types.Message):
    await settingsState.set_procent.set()
    await bot.send_message(message.chat.id, 'Введите значение:', reply_markup=cancelMarkup)


async def set_general_money(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, f'Сумма торговли успешно установлена как: {message.text}$')
    telegram_database(message.chat.id).set_general_money(message.text)
    await state.finish()
    await settingsInterface(message)


async def general_money(message: types.Message):
    await settingsState.set_general_money.set()
    await bot.send_message(message.chat.id, 'Введите значение:', reply_markup=cancelMarkup)


async def set_piece(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, f'Сумма покупки 1 сделки установленна: {message.text}$')
    telegram_database(message.chat.id).set_piece(message.text)
    await state.finish()
    await settingsInterface(message)


async def piece(message: types.Message):
    await settingsState.set_piece.set()
    await bot.send_message(message.chat.id, 'Введите значение:', reply_markup=cancelMarkup)


async def set_timeframe(message: types.Message, state: FSMContext):
    if not message.text.split()[0][0] in '12345':
        await bot.send_message(message.chat.id, 'Неккоректый ввод')
        return
    timeframes = {
        '1': '1m',
        '2': '15m',
        '3': '30m',
        '4': '1h',
        '5': '4h',
    }
    await bot.send_message(message.chat.id, f'Таймфрем установлен как: {timeframes[message.text]}')
    telegram_database(message.chat.id).set_timeframe(timeframes[message.text])
    await state.finish()
    await settingsInterface(message)


async def timeframe(message: types.Message):
    await settingsState.set_timeframe.set()
    await bot.send_message(message.chat.id, '1. 1 минутный таймфрейм\n'
                                            '2. 15 минутный таймфрейм\n'
                                            '3. 30 минутный таймфрейм\n'
                                            '4. 1-часовой таймфрейм\n'
                                            '5. 4-часовой таймфрейм\n\n'
                                            'Введите нужный таймфрейм:', reply_markup=cancelMarkup)


async def stats(message: types.Message):
    await bot.send_message(message.chat.id, 'В разработке')
    pass


async def logs(message: types.Message):
    await bot.send_message(message.chat.id, 'В разработке')
    pass


async def start_work(message: types.Message):
    await bot.send_message(message.chat.id, 'В разработке')
    pass


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.register_message_handler(menu, lambda msg: msg.text.lower() == 'вернуться в меню')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(isRegister, lambda msg: telegram_database(msg.chat.id).isUserInDatabase() == False, state='*')
    dp.register_message_handler(process_invalid, lambda msg: not msg.text.isdigit(),
                                state=[settingsState.set_procent, settingsState.set_profit,
                                       settingsState.set_general_money,
                                       settingsState.set_piece, settingsState.set_timeframe])

    dp.register_message_handler(procent, Text(equals='процент', ignore_case=True))
    dp.register_message_handler(set_procent, state=settingsState.set_procent)

    dp.register_message_handler(profit, Text(equals='профит', ignore_case=True))
    dp.register_message_handler(set_profit, state=settingsState.set_profit)

    dp.register_message_handler(general_money, Text(equals='сумму торговли', ignore_case=True))
    dp.register_message_handler(set_general_money, state=settingsState.set_general_money)

    dp.register_message_handler(piece, Text(equals='сумму покупки за сделку', ignore_case=True))
    dp.register_message_handler(set_piece, state=settingsState.set_piece)

    dp.register_message_handler(timeframe, Text(equals='таймфрейм', ignore_case=True))
    dp.register_message_handler(set_timeframe, state=settingsState.set_timeframe)

    dp.register_message_handler(settings, Text(equals='settings', ignore_case=True))
    dp.register_message_handler(stats, Text(equals='stats', ignore_case=True))
    dp.register_message_handler(logs, Text(equals='logs', ignore_case=True))
    dp.register_message_handler(start_work, Text(equals='start_work', ignore_case=True))
