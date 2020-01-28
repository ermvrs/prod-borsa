class MergedCandlesTechValues:
    def __init__(self,algocandle,close,rsi,sma,ema):
        self.Algo = algocandle
        self.Close = close
        self.RSI =rsi
        self.SMA =sma
        self.EMA = ema
        self.Date = algocandle.Date
        self.Timestamp = algocandle.Timestamp