import pandas as pd
from fonksiyonlar.timefuncs import timestamptodate,getcurrentdate, getcurrentts
from datetime import datetime
from fonksiyonlar.formats import eightdecimalstring
from fonksiyonlar.techfuncs import RSI,SMA,EMA
from decimal import Decimal
from algorithms.testalgo import TestAlgoLiveFunc
from algorithms.blackalgo import BlackAlgoLiveFunc,BlackAlgoLiveFuncNoDiff
from fonksiyonlar.outputs import TelegramOutput
from fonksiyonlar.outputs import OutputManager
from health.healthcontroller import InformationDatabase
from classes.error import Error, Information
from classes.signal import Signal
from classes.techdata import TechnicalAnalysisData
class Market:
    def __init__(self,symbol,exchange):
        self.AlgorithmFunc = TestAlgoLiveFunc
        self.Telegram = TelegramOutput()
        self.Symbol = symbol
        self.VolumeRequirement = 50 #Sinyal çıktısı için 24 saatlik volume şartı (btc bazlı)
        self.Exchange = exchange
        response = self.Exchange.getFirstDepth(symbol,50)
        self.Bids = response["bids"]
        self.Asks = response["asks"]
        self.LastUpdateId = int(response["lastUpdateId"])
    def InitializeTradeSockets(self):
        start,err = self.Exchange.startListenMarket(_sym=self.Symbol,_cb=self.HandleResponse)
        if not start:
            print("Error at starting socket. Symbol : {0}, Error : {1}".format(self.Symbol,err))
            errorclass = Error(self.Symbol,getcurrentdate(),"localmarket.py LN25",str(err),1)
            info = Information(self.Symbol,getcurrentdate(),"Error At starting socket")
            InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
            InformationDatabase.getInstance().appendError(errorclass)
        else:
            print("Started to listen {} trades.".format(self.Symbol))
    def startSockets(self):
        start,err = self.Exchange.startSockets()
        if not start:
            #start sockets, initializetradesockets ve initialize candle sockets 3 ü aynanda çağırılırsa hataveriyor olabilir. Hata kaynağı
            #bu bunu fixle.
            print("Error at starting sockets. Symbol : {0}, Error : {1}".format(self.Symbol,err))
            errorclass = Error(self.Symbol,getcurrentdate(),"localmarket.py LN35",str(err),1)
            InformationDatabase.getInstance().appendError(errorclass)
        else:
            print("{} Sockets started.".format(self.Symbol))
    def HandleResponse(self,msg):
        self.LastUpdateId = int(msg['lastUpdateId'])
        self.Bids = msg['bids']
        if(msg['asks'][0][0] != self.Asks[0][0]):
            #print("Best buy offer changed. Recalculation will began.")
            self.recalculatewithbestprice()
        self.Asks = msg['asks']

    def bestPricetoBuy(self):
        return Decimal(self.Asks[0][0]),Decimal(self.Asks[0][1])#price,qty
    def getAsks(self):
        return self.Asks
    def getBids(self):
        return self.Bids
    def loadCandles(self,Candles):
        if isinstance(Candles,pd.core.frame.DataFrame):
            self.Candles = Candles
            self.CandleCount = len(Candles)
            self.lastCandleTimestamp = int(Candles.iloc[-1:]['Timestamp'])
            #print(self.Candles.iloc[-1:])
            print("{} Candles Loaded.".format(self.CandleCount))
            info = Information(self.Symbol, getcurrentdate(), "{} Candles Loaded.".format(self.CandleCount))
            InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
        else:
            raise Exception("Candles parameter at loadCandles should be an instance of pandas.Dataframe")
    def updateLastCandle(self,newCandle):
        self.Candles.drop(self.Candles.index[:1],inplace=True)
        self.Candles = self.Candles.append(newCandle,ignore_index=True) # row eklemiyor.
        self.Candles.reset_index(drop=True, inplace=True)
        print("Candles Updated")
        info = Information(self.Symbol, getcurrentdate(), "Candles Updated.")
        InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
    def InitializeCandleSockets(self,interval):
        start,err = self.Exchange.startCandleListening(_sym=self.Symbol,_interval=interval,_cb=self.candleSocketHandler)
        if not start:
            print("Error at starting candle socket.\nSymbol : {0},\nError : {1}".format(self.Symbol,err))
            errorclass = Error(self.Symbol,getcurrentdate(),"localmarket.py LN71",err.msg,1)
            InformationDatabase.appendError(errorclass)
        else:
            print("Started to listen {}".format(self.Symbol))
            info = Information(self.Symbol, getcurrentdate(), "Started to listen {}".format(self.Symbol))
            InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
    def candleSocketHandler(self,msg):
        newCandle = {}
        newCandle['Date'] = str(timestamptodate(msg['k']['T']))
        newCandle['Timestamp'] = int(msg['k']['T'])
        newCandle['Closeprice'] =Decimal(msg['k']['c'])
        newCandle['Openprice'] =Decimal(msg['k']['o'])
        newCandle['High'] =Decimal(msg['k']['h'])
        newCandle['Low'] =Decimal(msg['k']['l'])
        newCandle['Volume'] =float(msg['k']['v'])
        newCandle['Tradescount'] =int(msg['k']['n'])
        newCandle['RSI'] = 0
        newCandle['EMA'] = 0
        newCandle['SMA'] = 0
        if int(msg['k']['T']) > (self.lastCandleTimestamp + 180) and int(msg['k']['n'] > 0): #socket data yeni bir candle
            self.updateLastCandle(newCandle)
            self.lastCandleTimestamp = int(msg['k']['T'])
            self.recalculatewithlasttradeprice(newCandle['Closeprice'],True)
        elif int(msg['k']['n'] > 0):
            self.recalculatewithlasttradeprice(newCandle['Closeprice'],False)

    def recalculatewithbestprice(self):
        price,qty = self.bestPricetoBuy()
        copy = self.Candles
        copy.loc[copy.index[-1], 'Closeprice'] = Decimal(price)
        rsival = RSI(copy,4)
        ema = list(EMA(rsival, 4))[-1:][0]
        sma = list(SMA(rsival, 12))[-1:][0]
        rsi = list(rsival)[-1:][0]
        #print("({0})Best Buy Price Results => RSI : {1}, EMA : {2}, SMA : {3}".format(self.Symbol,rsi,ema,sma,Decimal(price)))
        self.checkForAlgorithm(self.AlgorithmFunc, rsi,ema,sma, Decimal(price))

    def recalculatewithlasttradeprice(self,price,isUpdated):
        if isUpdated:
            rsival = RSI(self.Candles, 4)
            ema = list(EMA(rsival, 4))[-1:][0]
            sma = list(SMA(rsival, 12))[-1:][0]
            rsi = list(rsival)[-1:][0]
            #print("({0})Last Trade Price Results(UPDATED) => RSI : {1}, EMA : {2}, SMA : {3}".format(self.Symbol,rsi, ema,sma,Decimal(price)))
            self.checkForAlgorithm(self.AlgorithmFunc,rsi,ema,sma,Decimal(price))
        else:
            fakecandle = {}
            fakecandle['Date'] = datetime.now()
            #sonuncuyu değiştiriyor. bi öncekiler kayıyor problem olabilir
            fakecandle['Timestamp'] = 0  # emindeğilim
            fakecandle['Closeprice'] = Decimal(price)
            fakecandle['Volume'] = float(46)
            copy = self.Candles
            copy.loc[copy.index[-1], 'Closeprice'] = Decimal(price)
            rsival = RSI(copy, 4)
            ema = list(EMA(rsival, 4))[-1:][0]
            sma = list(SMA(rsival, 12))[-1:][0]
            rsi = list(rsival)[-1:][0]
            #print("({0} - , {4})Last Trade Price Results(NOUPDT) => RSI : {1}, EMA : {2}, SMA : {3}".format(self.Symbol,rsi,ema,sma,Decimal(price)))
            self.checkForAlgorithm(self.AlgorithmFunc,rsi,ema,sma,Decimal(price))

    def checkForAlgorithm(self,AlgorithmLiveFunc,rsi,ema,sma,currPrice):
        algo,target = AlgorithmLiveFunc(rsi,ema,sma,float(currPrice))
        if algo:
            #output target
            volume = float(self.Exchange.get24HVolume(self.Symbol)[0])
            if volume > self.VolumeRequirement:
                td = TechnicalAnalysisData(rsi, ema, sma, getcurrentdate(),volume)
                signal = Signal(self.Symbol,str(currPrice),str(target),getcurrentdate(),td.__dict__,getcurrentts(),AlgorithmLiveFunc.__name__)

                InformationDatabase.getInstance().appendSignal(signal)
                print("==========Live signal given ==========")
                print("Pair : {2}\nBuy Price : {0}\nTarget Price : {1}".format(currPrice,target,self.Symbol))
                #self.Telegram.sendMessage("Pair : {0}\nBuy Price : {1}\nTarget Price : {2}".format(self.Symbol,currPrice,target))
                OutputManager.getInstance().PublishSignal(self.Symbol,currPrice,target)
            else:
                print("Volume is not enough. Symbol : {} - Volume : {}".format(self.Symbol,volume))

