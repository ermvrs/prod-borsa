from binanceapi.connector import Binance
from binance.client import Client
import pandas as pd
from decimal import Decimal
from market.marketstarter import startFunctionsForMarket, StartParams
from classes.threadings import ThreadHandler
import json
from fonksiyonlar.outputs import OutputManager
from health.healthcontroller import InformationDatabase
from health.statusoutput import app
Exchange = Binance("LUB6dWFM5MfQFLWAyKmAbYviRmdAyLMhpxBTqKZ6dV9MxTn3dzA0xVWLTeb21caj","c5tuBiHSX2FeThXBfKf1VnlLTFxj1LJdbbxcFyBc8v5ZXSfcbL3ukvu31qNDMASM")
InformationDatabase() # initiliaze db

OutputManager() #silinebilir

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

app.run(host="0.0.0.0",port=5714)