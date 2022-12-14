import math
import sqlite3
from datetime import datetime


class database:
    _con = sqlite3.connect('data.db')
    _cur = _con.cursor()
    _procent = 3

    def __init__(self, telegram_id):
        self.telegram_id = str(telegram_id)
        try:
            self._cur.execute('''CREATE TABLE users (telegram_id text, API_key text, Secret_Key text, first_name 
            TEXT, isWork TEXT, profit TEXT, date text)''')
        except sqlite3.OperationalError:
            pass
        try:
            self._cur.execute('''CREATE TABLE general_info (telegram_id text, profit TEXT, procent TEXT, 
            general_money TEXT, piece TEXT, timeframe TEXT, coin TEXT)''')
        except sqlite3.OperationalError:
            pass
        try:
            self._cur.execute('''CREATE TABLE orders (telegram_id text, quantity text, coin text, price_coin text, 
            side text, count text, date text)''')
        except sqlite3.OperationalError:
            pass
        data = self._cur.execute('SELECT * FROM users')
        for i in data.fetchall():
            if self.telegram_id == i[0]:
                self.api = i[1]
                self.secret_key = i[2]
                self.work = i[4]
                self.userProfit = i[5]

        data = self._cur.execute('SELECT * FROM general_info')
        for i in data.fetchall():
            if self.telegram_id == i[0]:
                self.__profit = i[1]
                self.__procent = i[2]
                self.__general_money = i[3]
                self.__piece = i[4]
                self.__timeframe = i[5]
                self.__coin = i[6]

    def isUserInDatabase(self):
        data = self._cur.execute('SELECT * FROM users')
        for i in data.fetchall():
            if self.telegram_id == i[0]:
                return True
        return False

    def addProfit(self, profit):
        data = self._cur.execute('SELECT * FROM users')
        profitdb = 0
        for i in data.fetchall():
            if self.telegram_id == i[0]:
                profitdb = float(i[5])
        profitdb += float(profit)
        self._cur.execute(f"UPDATE users SET profit = '{profitdb}' WHERE telegram_id = {self.telegram_id}")

    def deleteOrder(self, price):
        self._cur.execute(f'DELETE FROM orders WHERE price_coin = "{price}";')
        self._con.commit()

    def get_profit(self):
        return self.__profit

    def get_procent(self):
        return self.__procent

    def get_general_money(self):
        return self.__general_money

    def get_piece(self):
        return self.__piece

    def get_timeframe(self):
        return self.__timeframe

    def get_api(self):
        return self.api

    def get_secret_key(self):
        return self.secret_key

    def get_coin(self):
        return self.__coin

    def get_work(self):
        return self.work

    def get_userProfit(self):
        return self.userProfit


class spot_database(database):
    def __init__(self, telegram_id):
        super().__init__(telegram_id)

    def take_price_coin(self):
        mass = []
        data = self._cur.execute('SELECT * FROM orders')
        for i in data.fetchall():
            if self.telegram_id == i[0]:
                mass.append([i[3], i[1]])
        mass.sort()
        return mass[0]

    def createNewOrder(self, quantity, coin, price_coin, side):
        isCreate = self.checkCountPercent(price_coin)
        if isCreate:
            print((self.telegram_id, quantity, coin, price_coin, side, isCreate, datetime.now()))
            self._cur.execute(f"INSERT INTO orders VALUES (?,?,?,?,?,?,?)",
                              (self.telegram_id, quantity, coin, price_coin, side, isCreate, datetime.now()))
            self._con.commit()
        else:
            print('order not created')

    def checkCountPercent(self, price_coin):
        mass = []
        max = math.floor(30/float(self.get_procent()))+1
        data = self._cur.execute('SELECT * FROM orders')
        for i in data.fetchall():
            if self.telegram_id == i[0]:
                mass.append([float(i[3]), int(i[5])])
        mass.sort()
        if mass[0][1] == max:
            return False
        if not mass:
            return 1
        if mass[0][0] < (price_coin - (price_coin * self._procent / 100)) * (mass[0][1]):
            return mass[0][1] + 1


class telegram_database(database):
    def __init__(self, telegram_id):
        super().__init__(telegram_id)


    def addApis(self, API_key, Secret_Key, first_name):
        if not self.isUserInDatabase():
            self._cur.execute(f"INSERT INTO users VALUES ('{self.telegram_id}','{API_key}','{Secret_Key}',"
                              f"'{first_name}','off', '0', '{datetime.now()}')")
            self._cur.execute(f"INSERT INTO general_info VALUES (?,?,?,?,?,?,?)",
                              (self.telegram_id, '', '', '', '', '', ''))
            self._con.commit()
        else:
            return "?????????? ???????????????????????? ?????? ????????"

    def switch_work(self):
        if self.get_work() == 'on':
            self._cur.execute(f"UPDATE users SET isWork = 'off' WHERE telegram_id = {self.telegram_id}")
        else:
            self._cur.execute(f"UPDATE users SET isWork = 'on' WHERE telegram_id = {self.telegram_id}")
        self._con.commit()

    def set_profit(self, profit):
        self._cur.execute(f"UPDATE general_info SET profit = '{profit}' WHERE telegram_id = {self.telegram_id}")
        self._con.commit()

    def set_procent(self, procent):
        self._cur.execute(f"UPDATE general_info SET procent = '{procent}' WHERE telegram_id = {self.telegram_id}")
        self._con.commit()

    def set_general_money(self, general_money):
        self._cur.execute(
            f"UPDATE general_info SET general_money = '{general_money}' WHERE telegram_id = {self.telegram_id}")
        self._con.commit()

    def set_piece(self, piece):
        self._cur.execute(f"UPDATE general_info SET piece = '{piece}' WHERE telegram_id = {self.telegram_id}")
        self._con.commit()

    def set_timeframe(self, arefm):
        self._cur.execute(f"UPDATE general_info SET timeframe = '{arefm}' WHERE telegram_id = {self.telegram_id}")
        self._con.commit()

    def set_coin(self, coin):
        self._cur.execute(f"UPDATE general_info SET coin = '{coin.upper()}' WHERE telegram_id = {self.telegram_id}")
        self._con.commit()
