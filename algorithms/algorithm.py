from classes.candle import AlgoCandle
import pandas as pd
class Algorithm:
    def __init__(self,AlgoCandles):
        if isinstance(AlgoCandles,list):
            if isinstance(AlgoCandles[0],AlgoCandle):
                self.Candles = AlgoCandles
                self.CandleCount = len(AlgoCandles)
                self.isDataFrame = False
            else:
                raise Exception("Parameter of algorithms should be an array of AlgoCandles")
        elif isinstance(AlgoCandles,pd.core.frame.DataFrame):
            self.Candles = AlgoCandles
            self.CandleCount = len(AlgoCandles)
            self.isDataFrame = True
        else:
            raise Exception("Parameter of algorithms should be an array or dataframe.")
    def getAlgorithmInfo(self):
        return self