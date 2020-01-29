#Test Algorithm designed by Erim VARIŞ
#Licensed and can't be used without permission.
#Designed for testing live output signals.
#Version : 1.0.0
from algorithms.algorithm import Algorithm
from fonksiyonlar.formats import eightdecimalstring
from algorithms.backtest import BacktestObject,SignalPoint
import pandas as pd
from decimal import Decimal
class TestAlgo(Algorithm):
    def __init__(self): #candles parametresini dataframe olarak değiştir.
        super(TestAlgo,self).__init__([])
        self.TargetMultiplier = 1.02 # %2 kazanç hedefli
    def ApplyLiveData(self,RSI,price):
        ###TODO Yeni gelen verilerde check yapması için fonksiyon.###
        ### sadece rsi vs değerleri parametre gönder fonksiyon true veya false döndürsün ve targeti döndürsün
        return RSI < 10, Decimal(price * self.TargetMultiplier)

    def BackTest(self):
        #Test algoritması için backteste gerek yok.
        return False
def TestAlgoLiveFunc(RSI,ema,sma,price):
    return float(RSI) < 50, [eightdecimalstring(price * (1.015)),eightdecimalstring(price * (1.024)), eightdecimalstring(price * (1.04))]