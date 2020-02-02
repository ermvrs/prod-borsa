import pandas as pd
from fonksiyonlar.timefuncs import timestamptodate,getcurrentdate, getcurrentts
from datetime import datetime
from fonksiyonlar.formats import eightdecimalstring
from fonksiyonlar.techfuncs import RSI,SMA,EMA
from decimal import Decimal
from algorithms.testalgo import TestAlgoLiveFunc
from algorithms.blackalgo import BlackAlgoLiveFunc,BlackAlgoLiveFuncNoDiff
#from fonksiyonlar.outputs import TelegramOutput
#from fonksiyonlar.outputs import OutputManager
from health.healthcontroller import InformationDatabase
from classes.error import Error, Information
from classes.signal import Signal
from classes.techdata import TechnicalAnalysisData
from fonksiyonlar.output import sendSignal
class Market:
    def __init__(self,symbol,exchange,thread):
        self.AlgorithmFunc = BlackAlgoLiveFunc
        #self.Telegram = TelegramOutput()
        self.Symbol = symbol
        self.Thread = thread
        self.VolumeRequirement = 35 #Sinyal çıktısı için 24 saatlik volume şartı (btc bazlı)
        self.Exchange = exchange
        response = self.Exchange.getFirstDepth(symbol,50)
        self.Bids = response["bids"]
        self.Asks = response["asks"]
        self.LastUpdateId = int(response["lastUpdateId"])
    def InitializeTradeSockets(self):
        self.Thread.AppendProcess("Trade socket is starting.")
        start,err = self.Exchange.startListenMarket(_sym=self.Symbol,_cb=self.HandleResponse)
        if not start:
            self.Thread.AppendThreadError(Error(self.Symbol, getcurrentdate(), "localmarket.py - InitializeTradeSockets", str(err), 2))
            print("Error at starting socket. Symbol : {0}, Error : {1}".format(self.Symbol,err))
            info = Information(self.Symbol,getcurrentdate(),"Error At starting socket")
            InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
        else:
            print("Started to listen {} trades.".format(self.Symbol))
            self.Thread.AppendProcess("Trade socket was started.")
    def startSockets(self):
        self.Thread.AppendProcess("Sockets Starting.")
        start,err = self.Exchange.startSockets()
        if not start:
            self.Thread.AppendThreadError(Error(self.Symbol, getcurrentdate(), "localmarket.py - startSockets", str(err), 1))
            print("Error at starting sockets. Symbol : {0}, Error : {1}".format(self.Symbol,err))
        else:
            self.Thread.AppendProcess("Sockets were started.")
            print("{} Sockets started.".format(self.Symbol))
    def HandleResponse(self,msg):
        #Tradesockets Handler
        self.Thread.AppendProcess("Tradesocket response will be handled.")
        self.LastUpdateId = int(msg['lastUpdateId'])
        self.Bids = msg['bids']
        if(msg['asks'][0][0] != self.Asks[0][0]):
            self.recalculatewithbestprice()
        self.Asks = msg['asks']
        self.Thread.AppendProcess("Tradesocket response was handled.")

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
            self.Thread.AppendProcess("Candles were loaded to market instance.")
            info = Information(self.Symbol, getcurrentdate(), "{} Candles Loaded.".format(self.CandleCount))
            InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
        else:
            raise Exception("Candles parameter at loadCandles should be an instance of pandas.Dataframe")
    def updateLastCandle(self,newCandle):
        self.Candles.drop(self.Candles.index[:1],inplace=True)
        self.Candles = self.Candles.append(newCandle,ignore_index=True) # row eklemiyor.
        self.Candles.reset_index(drop=True, inplace=True)
        print("[{}] Candles Updated".format(getcurrentdate()))
        self.Thread.AppendProcess("Candle list was updated")
        info = Information(self.Symbol, getcurrentdate(), "Candles Updated.")
        InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
    def InitializeCandleSockets(self,interval):
        self.Thread.AppendProcess("Candle socket is initializing.")
        start,err = self.Exchange.startCandleListening(_sym=self.Symbol,_interval=interval,_cb=self.candleSocketHandler)
        if not start:
            self.Thread.AppendThreadError(Error(self.Symbol,getcurrentdate(),"localmarket.py - InitializeCandleSockets",str(err),2))
            print("Error at starting candle socket.\nSymbol : {0},\nError : {1}".format(self.Symbol,err))
        else:
            print("[{0}] Started to listen {1}".format(getcurrentdate(),self.Symbol))
            self.Thread.AppendProcess("Candle socket was started. And now listening.")
            info = Information(self.Symbol, getcurrentdate(), "Started to listen {}".format(self.Symbol))
            InformationDatabase.getInstance().appendInfoToPair(self.Symbol, info)
    def candleSocketHandler(self,msg):
        self.Thread.AppendProcess("Candle will be handled.")
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
            self.Thread.AppendProcess("Candle is handled")
        elif int(msg['k']['n'] > 0):
            self.recalculatewithlasttradeprice(newCandle['Closeprice'],False)
            self.Thread.AppendProcess("Candle is handled.")

    def recalculatewithbestprice(self):
        self.Thread.AppendProcess("Recalculation with bestprice will be done.")
        price,qty = self.bestPricetoBuy()
        copy = self.Candles
        copy.loc[copy.index[-1], 'Closeprice'] = Decimal(price)
        rsival = RSI(copy,4)
        ema = list(EMA(rsival, 4))[-1:][0]
        sma = list(SMA(rsival, 12))[-1:][0]
        rsi = list(rsival)[-1:][0]
        self.checkForAlgorithm(self.AlgorithmFunc, rsi,ema,sma, Decimal(price))
        self.Thread.AppendProcess("Recalculation with bestprice is done.")

    def recalculatewithlasttradeprice(self,price,isUpdated):
        self.Thread.AppendProcess("Recalculation with last trade price will be done.")
        if isUpdated:
            rsival = RSI(self.Candles, 4)
            ema = list(EMA(rsival, 4))[-1:][0]
            sma = list(SMA(rsival, 12))[-1:][0]
            rsi = list(rsival)[-1:][0]
            self.Thread.AppendProcess("Checking Algorithm")
            self.checkForAlgorithm(self.AlgorithmFunc,rsi,ema,sma,Decimal(price))
            self.Thread.AppendProcess("Recalculation with last trade is done.")
        else:
            fakecandle = {}
            fakecandle['Date'] = datetime.now()
            fakecandle['Timestamp'] = 0  # emindeğilim
            fakecandle['Closeprice'] = Decimal(price)
            fakecandle['Volume'] = float(46)
            copy = self.Candles
            copy.loc[copy.index[-1], 'Closeprice'] = Decimal(price)
            rsival = RSI(copy, 4)
            ema = list(EMA(rsival, 4))[-1:][0]
            sma = list(SMA(rsival, 12))[-1:][0]
            rsi = list(rsival)[-1:][0]
            self.Thread.AppendProcess("Checking Algorithm")
            self.checkForAlgorithm(self.AlgorithmFunc,rsi,ema,sma,Decimal(price))
            self.Thread.AppendProcess("Recalculation with last trade is done.")

    def checkForAlgorithm(self,AlgorithmLiveFunc,rsi,ema,sma,currPrice):
        algo,target = AlgorithmLiveFunc(rsi,ema,sma,float(currPrice))
        if algo:
            #output target
            volume = float(self.Exchange.get24HVolume(self.Symbol)[0])
            if volume > self.VolumeRequirement:
                td = TechnicalAnalysisData(rsi, ema, sma, getcurrentdate(),volume)
                signal = Signal(self.Symbol,str(currPrice),target,getcurrentdate(),td.__dict__,getcurrentts(),AlgorithmLiveFunc.__name__)
                sendSignal(signal)
                InformationDatabase.getInstance().appendSignal(signal)
                self.Thread.AppendProcess("Algorithm prerequirements is okey. Signal will be given.")
                print("==========Live signal given ==========")
                print("Pair : {2}\nBuy Price : {0}\nTarget Price : {1}".format(currPrice,target,self.Symbol))
                #OutputManager.getInstance().PublishSignal(self.Symbol,currPrice,target)
            else:
                print("Volume is not enough. Symbol : {} - Volume : {}".format(self.Symbol,volume))

