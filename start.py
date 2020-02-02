'''
from binanceapi.connector import Binance
from market.marketstarter import startFunctionsForMarket, StartParams
from classes.threadings import ThreadHandler
import json
from health.healthcontroller import InformationDatabase
from configuration import config
from health.statusoutput import app
config.Configurations(config.ConfigInterface("config.json").get())

Exchange = Binance(config.Configurations.getInstance().getKey('BinanceAPIKEY'),config.Configurations.getInstance().getKey('BinanceAPIPass'))
InformationDatabase() # initiliaze db



btcmarkets = []
with open("marketlist.txt" , "r") as file:
    data = file.read()
    btcmarkets = json.loads(data)

Threads = []
for item in btcmarkets:
    param = StartParams(item,Exchange)
    thread = ThreadHandler(startFunctionsForMarket,param)
    Threads.append(thread)

for th in Threads:
    th.StartThread()

app.run(host="0.0.0.0",port=int(config.Configurations.getInstance().getKey('HealthPort')))
'''
from binanceapi.connector import Binance
from multithreading.ThreadClass import Threads,ThreadInterface,StartParams
from market.marketstarter import startFunctionsForMarket
from health.healthcontroller import InformationDatabase
from configuration import config
from health.statusoutput import app
import json
InformationDatabase()
config.Configurations(config.ConfigInterface("config.json").get())
Exchange = Binance(config.Configurations.getInstance().getKey('BinanceAPIKEY'),config.Configurations.getInstance().getKey('BinanceAPIPass'))
Threads() # Threads listesini oluştur.
btcmarkets = []
with open("marketlist.txt" , "r") as file:
    data = file.read()
    btcmarkets = json.loads(data)

for item in btcmarkets:
    th = ThreadInterface(item,Exchange,startFunctionsForMarket)
    Threads.getInstance().AppendThread(item,th)

Threads.getInstance().StartAllThreads()
app.run(host="0.0.0.0",port=int(config.Configurations.getInstance().getKey('HealthPort')))