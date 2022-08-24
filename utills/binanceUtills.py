from telegram_bot.database.sqlite import spot_database
import math
from binance.client import Client
from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())
class BinanceClient:
    __client = Client(os.getenv('API_KEY'), os.getenv('Secret_key'))

    def __init__(self, coin, profit, tf, usdt):
        self.coin = coin.upper()
        self.priceCoin = float(self.__client.get_symbol_ticker(symbol=self.coin)['price'])
        self.profit = profit
        self.tf = tf
        self.usdt = usdt

    def get_coin_average(self, tf):
        timeFrame = {
            '1m': '1 hours ago UTC',
            '15m': '15 hours ago UTC',
            '30m': '30 hours ago UTC',
            '1h': '60 hours ago UTC',
            '4h': '240 hours ago UTC',
        }
        temp = []
        klines = self.__client.get_historical_klines_generator(self.coin.upper(), Client.KLINE_INTERVAL_1MINUTE,
                                                                 timeFrame[f'{tf}'])
        for i in klines:
            temp.append((float(i[2]) + float(i[3])) / 2)
        return round(sum((float(temp[i]) for i in range(0, int(len(temp))))) / int(len(temp)),4)

    def __formula(self, price_coin):
        price_coin = float(price_coin)
        return price_coin*(self.profit + 0.25)/100+price_coin

    def check_orders(self):
        self.__client.get_all_orders()

    def create_order_buy(self, telegram_id):
        price = self.get_coin_average('1m')
        buy_coin = math.floor(self.usdt/price)
        price_str = '{:0.0{}f}'.format(price, 4)
        spot_database(telegram_id).createNewOrder(buy_coin, self.coin, self.priceCoin, 'BUY')
        self.__client.create_order(
            symbol=self.coin,
            side='BUY',
            type='LIMIT',
            quantity=buy_coin,
            timeInForce='GTC',
            price=price_str
        )
        print('Ордер на покупку создан для - ', telegram_id)

    def create_order_sell(self, telegram_id):
        price_coin = spot_database(telegram_id).take_price_coin()[0]
        coin_sell = int(spot_database(telegram_id).take_price_coin()[1])
        print(self.__formula(price_coin), coin_sell)
        self.__client.create_order(
            symbol=self.coin,
            side='SELL',
            type='LIMIT',
            quantity=coin_sell,
            timeInForce='GTC',
            price=round(self.__formula(price_coin),4)
        )
        print('Ордер на продажу создан для - ', telegram_id)

