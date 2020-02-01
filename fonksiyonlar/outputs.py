import json
import requests
from datetime import datetime
from classes.error import Error
#from health.healthcontroller import InformationDatabase
from fonksiyonlar.formats import eightdecimalstring
from decimal import Decimal
'''
class TelegramOutput:
    def __init__(self):
        self.BotApi =("1045834942:AAHAS-5JoTN9SwpVA_sXQwl4Cb3JwEdGWfw")

    def sendMessage(self,Msg):
        bot_chatID = '962179053'
        send_text = 'https://api.telegram.org/bot' + self.BotApi + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + Msg

        response = requests.get(send_text).json()
        return response
'''
def TelegramMessage(x,y):
    pass
def TelegramMessagex(signal,infodb): # bunu kullan
    try:  #burada hata oluyor sanırsam
        BotApi = ("1089469288:AAEGNf310x82FrmRMxEZyzxfUcgqDbqIwa0")
        bot_chatID = str('-382269432')
        print(signal.Sells[1])
        Msg = "Pair : {0}%0ABuy Price : {1}%0ASell Price Levels %0A{2}%0A{3}%0A{4}".format(signal.Pair,signal.Buy,signal.Sells[0],signal.Sells[1],signal.Sells[2])
        send_text = 'https://api.telegram.org/bot' + BotApi + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + Msg
        resp = requests.get(send_text).json()
        print("Message sent" + json.dumps(resp))
    except Exception as err:
        errmsg = str(err)
        errcl = Error(signal.Pair,signal.Date,"outputs.py",errmsg,2)
        infodb.appendError(errcl) #sunucuda böyle dene
        print("Error message added. Msg : {}".format(errmsg))
'''
class OutputManager:
    __instance = None
    @staticmethod
    def getInstance():
        if OutputManager.__instance == None:
            OutputManager()
        return OutputManager.__instance
    def __init__(self):
        if OutputManager.__instance != None:
            raise Exception("You can't create more instances of Outputmgr!")
        else:
            OutputManager.__instance = self
            self.Signals = [{
                "signalid" : 0,
                "buyprice" : 0,
                "sellprices" : [0,0,0],
                "pair" : "SAMPLE"
            }]
    def PublishSignalx(self,_pair,_buyprice,_sellprices):
        signalid = len(self.Signals) + 1
        now = datetime.now()
        currentdate = now.strftime("%d/%m/%Y %H:%M:%S")
        SignalObj = {
            "signalid" : signalid,
            "pair" : _pair,
            "buyprice" : _buyprice,
            "sellprices" : _sellprices,
            "creationdate" : now,
            "status" : 0,
            "updatedate" : None
        }
        BotApi = ("1045834942:AAHAS-5JoTN9SwpVA_sXQwl4Cb3JwEdGWfw")
        bot_chatID = '-382269432'
        #sp1, sp2, sp3 = str("{0:.8f}".format(_sellprices[0])),str("{0:.8f}".format(_sellprices[1])),str("{0:.8f}".format(_sellprices[2]))
        sp1, sp2, sp3 = eightdecimalstring(_sellprices[0]), eightdecimalstring(_sellprices[1]), eightdecimalstring(_sellprices[2])
        Msg = "Pair : {0}\nBuy Price : {1}\nSell Price Levels \n{2}\n{3}\n{4}".format(_pair,Decimal(_buyprice),Decimal(sp1),Decimal(sp2),Decimal(sp3))
        send_text = 'https://api.telegram.org/bot' + BotApi + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + Msg
        response = requests.get(send_text).json()
        self.Signals.append(SignalObj)
        return True

    def PublishSignal(self,pair,buy,sells):
        #sp1, sp2, sp3 = str("{0:.8f}".format(sells[0])), str("{0:.8f}".format(sells[1])), str("{0:.8f}".format(sells[2]))
        sp1,sp2,sp3 = eightdecimalstring(sells[0]), eightdecimalstring(sells[1]), eightdecimalstring(sells[2])
        endpoint = "http://185.50.69.97:8080/signal/add"
        data = {
            'key' : "erimsapp34",
            'buyprice' : buy,
            'sellprices' : [sp1,sp2,sp3],
            'pair' : pair
        }
        r = requests.post(url = endpoint, data = data)
'''