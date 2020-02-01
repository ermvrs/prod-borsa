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
with open("marketlist-r.txt" , "r") as file:
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