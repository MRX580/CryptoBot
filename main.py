from binance.client import Client
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
client = Client(os.getenv('API_KEY'), os.getenv('Secret_key'))

def info():
    for i in client.get_all_orders(symbol='XRPUSDT'):
        print(i)
    print(client.get_account())
    print(client.get_asset_balance('XRPUSDT'))
    print(client.get_asset_balance('USDT'))

info()

