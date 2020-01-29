#Black Algorithm designed by Erim VARIŞ
#Licensed and can't be used without permission.
#Version : 1.0.0
from algorithms.algorithm import Algorithm
from algorithms.backtest import BacktestObject,SignalPoint
from fonksiyonlar.formats import eightdecimalstring
from decimal import Decimal
import pandas as pd
class BlackAlgo(Algorithm):
    def __init__(self,Candles): #candles parametresini dataframe olarak değiştir.
        super(BlackAlgo,self).__init__(Candles)
        self.TargetMultiplier = 1.02 # %2 kazanç hedefli
    def ApplyLiveData(self,rsi,ema,sma,price): #foınksiyonu kullan
        diff = sma - ema
        if rsi < 15 and ema < 20 and sma > 25 and ema > diff and diff > 15:
            return True,Decimal(price * self.TargetMultiplier)
        else:
            return False,0

    def BackTest(self):
        #Initialize backtest object.
        BackTestObj = BacktestObject()
        print("############ BACKTEST STARTED FOR BLACKALGO ############")
        if isinstance(self.Candles,pd.core.frame.DataFrame):
            for index,row in self.Candles.iterrows():
                rsi = self.Candles.loc[index,"RSI"]
                ema = self.Candles.loc[index,"EMA"]
                sma = self.Candles.loc[index,"SMA"]
                diff = sma - ema
                if rsi < 15 and ema < 20 and sma > 25 and ema > diff and diff > 15:
                    target = self.Candles.loc[index,"Closeprice"] * self.TargetMultiplier
                    newSignal = SignalPoint(self.Candles.loc[index,"Date"],self.Candles.loc[index,"Timestamp"],"Blackalgo",self.Candles.loc[index,"Closeprice"],target)
                    BackTestObj.addPoint(newSignal)
                    print("Found Signal Point")
            print("Checing for targets")
            BackTestObj.targetCheck(self.Candles)
        else:
            for candle in self.Candles:
                diff = candle.SMA - candle.EMA
                if candle.RSI < 15 and candle.EMA < 20 and candle.SMA > 25 and candle.EMA > diff and diff > 15:
                    #Signal point
                    target = candle.ClosePrice * self.TargetMultiplier
                    newSignal = SignalPoint(candle.Date,candle.Timestamp,"BlackAlgo",candle.ClosePrice,target)
                    BackTestObj.addPoint(newSignal)
                    print("Found Signal Point")
            print("Checking for targets")
            BackTestObj.targetCheck(self.Candles)

def BlackAlgoLiveFunc(rsi,ema,sma, price):
    diff = sma - ema
    if rsi < 15 and ema < 20 and sma > 25 and ema > diff and diff > 15:
        return True, [eightdecimalstring(price * (1.015)),eightdecimalstring(price * (1.024)), eightdecimalstring(price * (1.04))]
    else:
        return False, 0

def BlackAlgoLiveFuncNoDiff(rsi,ema,sma,price): # riskli ama daha fazla signal
    diff = sma - ema
    if ema < 20 and diff > 15 and sma > 25 and rsi < 15:
        return True, [eightdecimalstring(price * (1.015)),eightdecimalstring(price * (1.024)), eightdecimalstring(price * (1.04))]
    else:
        return False, 0