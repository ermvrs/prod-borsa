from classes.error import Error,Information
from fonksiyonlar.timefuncs import getcurrentdate
from health.healthcontroller import InformationDatabase
from threading import Thread
class ThreadInterface:
    def __init__(self,Pair,Exchange,Func):
        self.Name = Pair
        self.Errors = []
        self.Outputs = []
        self.LastProcess = None
        self.LastProcessList = []
        param = StartParams(Pair, Exchange, self)
        self.Instance = Thread(name=Pair, target=Func, args=(param,))

    def isThreadAlive(self):
        return self.Instance.is_alive() #FALSE DÖNÜYOR
    def StartThread(self):
        self.Instance.start()
    def GetThreadName(self):
        return self.Instance.getName()
    def AppendThreadError(self,err):
        self.Errors.append(err.__dict__)
    def AppendThreadOutputs(self,out):
        self.Outputs.append(out)
    def GetLastProcess(self):
        return self.LastProcess
    def AppendProcess(self,proc):
        self.LastProcessList.append({'Date': getcurrentdate(), 'Process': proc})
        self.LastProcess = proc
    def GetProcessList(self):
        return self.LastProcessList

class Threads:
    __instance = None
    @staticmethod
    def getInstance():
        if Threads.__instance == None:
            Threads()
        return Threads.__instance
    def __init__(self):
        if Threads.__instance != None:
            print("Singletonu iki kere çağırma")
        else:
            self.ThreadList = {}
            Threads.__instance = self
    def AppendThread(self,Pair,IThread):
        if isinstance(IThread,ThreadInterface):
            self.ThreadList[Pair] = IThread
        else:
            err = Error(Pair,getcurrentdate(),"ThreadClass.py - appendThread","IThread instance is not ThreadInterface",2)
            InformationDatabase.getInstance().appendError(err)
    def GetThreadByName(self,Name):
        try:
            return self.ThreadList[Name]
        except KeyError as KE:
            err = Error(Name,getcurrentdate(),"ThreadClass.py - Threads - GetThreadByName","Key Error at function. Thread is not found.",2)
            InformationDatabase.getInstance().appendError(err)
            return False
    def RemoveThreadByName(self,Name):
        try:
            del self.ThreadList[Name]
            return True
        except KeyError as KE:
            err = Error(Name,getcurrentdate(),"ThreadClass.py - Threads - RemoveThreadByName","Key Error at function. Thread is not found.",2)
            InformationDatabase.getInstance().appendError(err)
            return False
    def StartAllThreads(self):
        for th in self.ThreadList.values():
            print("{} - Started",th.Name)
            th.Instance.start()

class StartParams:
    def __init__(self,sym,exc,th):
        self.Symbol = sym
        self.Exchange = exc
        self.Thread = th