from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime

class Binance:
    def __init__(self,api_key,api_secret):
        if isinstance(api_key,str) and isinstance(api_secret,str):
            self.Client = Client(api_key,api_secret)
            self.SocketManager = BinanceSocketManager(self.Client, user_timeout=60)
        else:
            raise Exception("Binance parameters should be an instance of string.")
    def getServerTime(self):
        stamp = self.Client.get_server_time()['serverTime']
        return datetime.fromtimestamp(stamp/1e3)
    def getHistoricalCandles(self,_sym,klinetime,fromwhere):
        return self.Client.get_historical_klines(symbol=_sym,interval=klinetime,start_str=fromwhere)
    def getOrderBook(self,_symbol):
        if isinstance(_symbol,str):
            return self.Client.get_order_book(symbol=_symbol)
        else:
            raise Exception("getOrderBook parameter should be an instance of string.")
    def getKlines(self,_symbol,klinetime):
        if isinstance(_symbol,str) and isinstance(klinetime,str):
            return self.Client.get_klines(symbol=_symbol,interval=klinetime)
        else:
            raise Exception("Symbol parameter should be a string and klinetime should be an instance of Client.kline")
    def getFirstDepth(self,_sym,lmt):
        if isinstance(_sym,str) and isinstance(lmt,int):
            return self.Client.get_order_book(symbol=_sym,limit=lmt)
        else:
            raise Exception("Symbol should be string and limit should be integer.")
    def startListenMarket(self,_sym,_cb):
        try:
            self.TradeSocketKey = self.SocketManager.start_depth_socket(symbol=_sym,depth=BinanceSocketManager.WEBSOCKET_DEPTH_10,callback=_cb)
            print("Trade socket initialized.")
            return True,None
        except Exception as err:
            return False,err
    def startCandleListening(self,_sym,_cb,_interval):
        try:
            self.KlineSocketKey = self.SocketManager.start_kline_socket(symbol=_sym,callback=_cb,interval=_interval)
            print("Candle socket initialized.")
            return True,None
        except Exception as err:
            return False,err
    def startSockets(self):
        try:
            self.SocketManager.start()
            return True,None
        except Exception as err:
            return False,err