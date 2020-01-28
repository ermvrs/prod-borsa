class Error:
    def __init__(self,Thread,Date,File,ErrorDesc,Level):
        self.Thread = Thread
        self.Date = Date
        self.File = File
        self.ErrorDesc = ErrorDesc
        self.Level = Level
class Information:
    def __init__(self,Pair,Date,Desc):
        self.Pair = Pair
        self.Date = Date
        self.Desc = Desc
