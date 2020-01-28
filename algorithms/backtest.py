from classes.candle import AlgoCandle
import pandas as pd
from decimal import Decimal
class BacktestObject:
    def __init__(self):
        self.Points = []

    def addPoint(self,signalpoint):
        if isinstance(signalpoint,SignalPoint):
            self.Points.append(signalpoint)
        else:
            raise Exception("Signal Point parameter should be an instance of Signal Point class")

    def targetCheck(self,candles):
        if isinstance(candles,list):
            if isinstance(candles[0],AlgoCandle):
                i = 1
                signalCount = len(self.Points)
                signalDone = 0
                for signal in self.Points:
                    print("Looking for Signal #{}".format(i))
                    print("============Signal Information============")
                    print("Date : {0}\nBuy Price: {1}\nTarget: {2}".format(signal.Date,signal.BuyPrice,signal.Target))
                    print("==========================================")
                    i +=1
                    for candle in candles:
                        if candle.Timestamp > signal.Timestamp and candle.High >= signal.Target:
                            # stop loss eklenebilir
                            print("Target Has seen at Candle")
                            print("============Candle Information============")
                            print("Date : {0}\nHigh : {1}\nClosePrice : {2}".format(candle.Date,candle.High,candle.ClosePrice))
                            print("==========================================")
                            signal.setTargetReached(candle.Timestamp)
                            signalDone += 1
                            break
                        else:
                            continue
                print("Backtest finished with Total Signals : {0}, Correct Signals : {1}".format(signalCount,signalDone))
            else:
                raise Exception("targetcheck parameter should be an array of algocandles")
        elif isinstance(candles,pd.core.frame.DataFrame):
            i = 1
            signalCount = len(self.Points)
            signalDone = 0
            for signal in self.Points:
                print("Looking for Signal #{}".format(i))
                print("============Signal Information============")
                print("Date : {0}\nBuy Price: {1}\nTarget: {2}".format(signal.Date, signal.BuyPrice, signal.Target))
                print("==========================================")
                i += 1
                for index,row in candles.iterrows():
                    if candles.loc[index,"Timestamp"] > signal.Timestamp and candles.loc[index,"High"] >= signal.Target:
                        # stop loss eklenebilir
                        print("Target Has seen at Candle")
                        print("============Candle Information============")
                        print("Date : {0}\nHigh : {1}\nClosePrice : {2}".format(candles.loc[index,"Date"],candles.loc[index,"High"],candles.loc[index,"Closeprice"]))
                        print("==========================================")
                        signal.setTargetReached(candles.loc[index,"Timestamp"])
                        signalDone += 1
                        break
                    else:
                        continue
            print("Backtest finished with Total Signals : {0}, Correct Signals : {1}".format(signalCount, signalDone))
        else:
            raise Exception("targetcheck parameter should be an array")
class SignalPoint:
    def __init__(self,date,ts,algo,buyprice,target):
        self.Date = date
        self.Timestamp =ts
        self.Algorithm = algo
        self.BuyPrice = buyprice
        self.Target = target
        self.isTargetSeen = False

    def setTargetReached(self,reachtimestamp):
        self.isTargetSeen = True
        self.ReachedAt = reachtimestamp