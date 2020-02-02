# Outputmgr ile connection sağlayan fonksiyonlar

from configuration.config import Configurations
from health.healthcontroller import InformationDatabase
from fonksiyonlar.timefuncs import getcurrentdate,getcurrentts
from classes.error import Error
import socket
import json
def sendSignal(x):
    pass #todo
def sendSignalTODO(Signal):
    try:
        print("SendSignalTCP WORK")
        connip = Configurations.getInstance().getKey('OutputManagerIP')
        connport = int(Configurations.getInstance().getKey('OutputManagerPort'))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((connip, connport))
        s.sendall(json.dumps(Signal.__dict__))
        data = s.recv(1024)
        s.close()
    except Exception as err:
        err_msg = str(err)
        err_cl = Error(Signal.Pair,getcurrentdate(),"SocketException - output.py",err_msg,2)
        InformationDatabase.getInstance().appendError(err_cl)
        print(err)