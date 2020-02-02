from decimal import Decimal
import pandas as pd
from fonksiyonlar.timefuncs import timestamptodate,getcurrentdate
from fonksiyonlar.techfuncs import RSI,SMA,EMA
from market.localmarket import Market
from classes.error import Error, Information
from health.healthcontroller import InformationDatabase
def startFunctionsForMarket(StartParams):
    try:
        #print("Starting Local Market - ({})".format(StartParams.Symbol))
        info = Information(StartParams.Symbol, getcurrentdate(), "Starting Local Market")
        InformationDatabase.getInstance().appendInfoToPair(StartParams.Symbol, info)
        InformationDatabase.getInstance().addPairStatus(StartParams.Symbol,"Starting")
        StartParams.Thread.AppendProcess("Starting")
        candlelist = StartParams.Exchange.getKlines(StartParams.Symbol,StartParams.Exchange.Client.KLINE_INTERVAL_3MINUTE,limit=1200)
        StartParams.Thread.AppendProcess("Taking KLINES")
        print("24 VOLUME OF {0} : {1}".format(StartParams.Symbol,StartParams.Exchange.get24HVolume(StartParams.Symbol)[0]))
        StartParams.Thread.AppendProcess("24 Hour Volume is : {0}".format(StartParams.Exchange.get24HVolume(StartParams.Symbol)[0]))
        #candlelist = StartParams.Exchange.getHistoricalCandles(StartParams.Symbol,StartParams.Exchange.Client.KLINE_INTERVAL_3MINUTE,"3 days ago UTC")
        array_of_dicts = []
        for candle in candlelist:
            tempdict = {}
            if float(candle[5]) > 0:
                tempdict['Date'] = timestamptodate(candle[6])
                tempdict['Timestamp'] = int(candle[6])
                tempdict['Closeprice'] = Decimal(candle[4])
                tempdict['Openprice'] = Decimal(candle[1])
                tempdict['High'] = Decimal(candle[2])
                tempdict['Low'] = Decimal(candle[3])
                tempdict['Volume'] = float(candle[5])
                tempdict['Tradescount'] = int(candle[8])
                tempdict['RSI'] = 0
                tempdict['EMA'] = 0
                tempdict['SMA'] = 0
                array_of_dicts.append(tempdict)
            else:
                continue
        df = pd.DataFrame(array_of_dicts)
        StartParams.Thread.AppendProcess("Data Frame Loaded. Length is : {}".format(len(df)))
        info = Information(StartParams.Symbol, getcurrentdate(), "Dict Length : {}".format(len(df)))
        InformationDatabase.getInstance().appendInfoToPair(StartParams.Symbol, info)
        if len(df) > 300:
            rsivalues = RSI(df, 4)  # ilk dört veri kayıyor ileride buna dikkat et
            df.drop(df.index[:4], inplace=True)
            df.reset_index(drop=True, inplace=True)
            sma = SMA(rsivalues, 12)
            ema = EMA(rsivalues, 4)
            # reindexing
            rsivalues.reset_index(drop=True, inplace=True)
            ema.reset_index(drop=True, inplace=True)
            sma.reset_index(drop=True, inplace=True)
            StartParams.Thread.AppendProcess("Tech Calculations Done.")
            for index, row in df.iterrows():
                df.loc[index, "RSI"] = rsivalues[index]
                df.loc[index, "EMA"] = ema[index]
                df.loc[index, "SMA"] = sma[index]
            df.dropna(inplace=True)
            df.reset_index(drop=True, inplace=True)  # Dropped nan values
            ##marketi başlat
            StartParams.Thread.AppendProcess("Starting local market")
            markt = Market(StartParams.Symbol,StartParams.Exchange,StartParams.Thread)
            markt.loadCandles(df[-250:])
            markt.InitializeCandleSockets(StartParams.Exchange.Client.KLINE_INTERVAL_3MINUTE)
            markt.InitializeTradeSockets()
            markt.startSockets() #startsockets çağrılmadımı program kapanıyor.
            info = Information(StartParams.Symbol, getcurrentdate(), "Market Started Succesfully")
            StartParams.Thread.AppendProcess("Market was started")
            InformationDatabase.getInstance().addPairStatus(StartParams.Symbol, "Started & Working")
            InformationDatabase.getInstance().appendInfoToPair(StartParams.Symbol, info)
            #print("({3})Values : RSI:{0} EMA:{1} SMA:{2}".format(list(rsivalues)[-1:],list(ema)[-1:],list(sma)[-1:],StartParams.Symbol))
        else:
            StartParams.Thread.AppendProcess("Pair has not enough candles. Min : 300")
            #print("{} - Market has not enough candles".format(StartParams.Symbol))
            info = Information(StartParams.Symbol, getcurrentdate(), "Market has not enough candles")
            InformationDatabase.getInstance().addPairStatus(StartParams.Symbol, "Stopped. Not enough candles.")
            InformationDatabase.getInstance().appendInfoToPair(StartParams.Symbol, info)
    except Exception as err:
        err_msg = str(err)
        err_cl = Error(StartParams.Symbol,getcurrentdate(),"MarketStarterException",err_msg,2)
        InformationDatabase.getInstance().appendError(err_cl)
        StartParams.Thread.AppendThreadError(err_cl)
        print("Error was added to InfoDB")
class StartParams:
    def __init__(self,sym,exc):
        self.Symbol = sym
        self.Exchange = exc