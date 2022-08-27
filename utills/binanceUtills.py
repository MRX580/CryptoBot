import os

import binance.exceptions
from datetime import datetime
from telegram_bot.database.sqlite import spot_database
import math
from binance.client import Client
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class BinanceClient:
    def __init__(self, telegram_id):
        data = spot_database(telegram_id)
        api, secret_key = data.get_api(), data.get_secret_key()
        self.telegram_id = telegram_id
        self.__client = Client(api, secret_key)
        self.coin = data.get_coin()
        try:
            self.priceCoin = float(self.__client.get_symbol_ticker(symbol=self.coin)['price'])
        except binance.exceptions.BinanceAPIException:
            pass
        self.profit = data.get_profit()
        self.tf = data.get_timeframe()
        self.usdt = data.get_piece()  # сделать формулу на ограничение с общей валютой
        self.procent = data.get_procent()
        self.general_money = data.get_general_money()

    def isCoin(self, coin):
        try:
            self.__client.get_symbol_ticker(symbol=coin.upper())
            return True
        except binance.exceptions.BinanceAPIException:
            return False

    def get_coin_average(self, tf):
        timeFrame = {
            '1m': '1 hours ago UTC',
            '15m': '15 hours ago UTC',
            '30m': '30 hours ago UTC',
            '1h': '60 hours ago UTC',
            '4h': '240 hours ago UTC',
        }
        temp = []
        klines = self.__client.get_historical_klines_generator(self.coin, Client.KLINE_INTERVAL_1MINUTE,
                                                               timeFrame[f'{tf}'])
        for i in klines:
            temp.append((float(i[2]) + float(i[3])) / 2)
        return round(sum((float(temp[i]) for i in range(0, int(len(temp))))) / int(len(temp)), 4)

    def __formula(self, price_coin):
        return round(price_coin * (self.profit + 0.25) / 100 + price_coin, 4)

    def takeAllOders(self):
        return [
            'Symbol - %s. Price - %s. Count - %s. Side %s. Time %s' % (
            i["symbol"], i["price"], i["origQty"], i["side"],
            datetime.fromtimestamp(i['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S'))
            for i in self.__client.get_all_orders(symbol='XRPUSDT')
        ]

    def check_orders(self):
        self.__client.get_all_orders()

    def isReadyToWork(self):
        if self.coin and self.profit and self.usdt and self.tf and self.procent and self.general_money:
            return True
        return False

    def cycleBuyAndSell(self):
        buyCoin = math.floor(self.usdt / self.get_coin_average(self.tf))
        spot_database(self.telegram_id).createNewOrder(buyCoin, self.coin, self.priceCoin, 'BUY')
        self.__client.order_market_buy(
            symbol=self.coin,
            quantity=buyCoin,
            requests_params={'timeout': 20})
        print('Ордер на покупку создан для - ', self.telegram_id)
        self.create_order_sell()

    def create_order_sell(self):
        price_coin = spot_database(self.telegram_id).take_price_coin()[0]
        coin_sell = int(spot_database(self.telegram_id).take_price_coin()[1])
        print(self.__formula(price_coin), coin_sell)
        self.__client.create_order(
            symbol=self.coin,
            side='SELL',
            type='LIMIT',
            quantity=coin_sell,
            timeInForce='GTC',
            price=round(self.__formula(price_coin), 4)
        )
        print('Ордер на продажу создан для - ', self.telegram_id)
