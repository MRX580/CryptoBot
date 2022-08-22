from binance.client import Client
from config import API_KEY, SECRET_KEY
from telegram_bot.database.sqlite import spot_database
import math
client = Client(API_KEY, SECRET_KEY)
def info():
    for i in client.get_all_orders(symbol='XRPUSDT'):
        print(i)
    print(client.get_account())
    print(client.get_asset_balance('XRPUSDT'))
    print(client.get_asset_balance('USDT'))




info()
#BinanceClient('XRPUSDT', 1, '1m', 10.2).create_order_buy(951679992)
#BinanceClient('XRPUSDT', 1, '1m', 10.2).create_order_sell(951679992)

