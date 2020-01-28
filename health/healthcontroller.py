class InformationDatabase:
    __instance = None
    '''
    Objeler
    Errors ->
    Working Pairs ->
    Signals Count ->
    '''
    @staticmethod
    def getInstance():
        if InformationDatabase.__instance == None:
            InformationDatabase()
        return InformationDatabase.__instance

    def __init__(self):
        if InformationDatabase.__instance != None:
            print("Singletonu iki kere çağırma")
        else:
            self.Database = {}
            self.Database['HealthStatus'] = "Normal"
            self.Database['Errors'] = []
            self.Database['SignalsCount'] = 0
            self.Database['Signals'] = []
            self.Database['PairStatus'] = {}
            InformationDatabase.__instance = self



    def appendError(self,Error):
        self.Database['Errors'].append(Error)
    def appendInfoToPair(self,Pair,Info):
        if self.isKeySet(Pair):
            self.Database[Pair].append(Info)
        else:
            self.Database[Pair] = []
            self.Database[Pair].append(Info)
    def appendSignal(self,Signal):
        self.Database['Signals'].append(Signal)
    def increaseSignalCount(self):
        self.Database['SignalsCount'] += 1
    def addPairStatus(self,Pair,Status):
        self.Database['PairStatus'][Pair] = Status
    def getDatabase(self):
        return self.Database
    def setObject(self,Key,Object):
        if(isinstance(Key,str)):
            self.Database[Key] = Object
        else:
            raise Exception("Key parameter should be an instance of String at setObject function.")
    def getObject(self,Key):
        if(isinstance(Key,str)):
            return self.Database[Key]
        else:
            raise Exception("Key parameter should be an instance of String at setObject function.")
            return False
    def isKeySet(self,Key):
        try:
            test = self.Database[Key]
            return True
        except KeyError as KE:
            return False
    def removeKey(self,Key): ##check
        try:
            del self.Database[Key]
            return True
        except:
            return False