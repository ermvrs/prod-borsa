class AlgoCandle:
    def __init__(self,date,ts,closeprice,openprice,high,low,volume,numtrades):
        try:
            self.Date = date
            self.Timestamp = int(ts)
            self.ClosePrice = float(closeprice)
            self.OpenPrice = float(openprice)
            self.High = float(high)
            self.Low = float(low)
            self.Volume = float(volume)
            self.TradesCount = int(numtrades)
        except Exception as err:
            raise Exception("Error at AlgoCandle init : {}".format(err))
    def setRSI(self,rsi):
        self.RSI = rsi
        return self
    def setEMAofRSI(self,ema):
        self.EMA= ema
        return self
    def setSMAofRSI(self,sma):
        self.SMA = sma
        return self

