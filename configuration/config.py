class Configurations:
    __instance = None
    @staticmethod
    def getInstance():
        if Configurations.__instance == None:
            Configurations()
        return Configurations.__instance
    def __init__(self,Config):
        if Configurations.__instance != None:
            print("Configi iki kere çağırma")
        else:
            self.Config = Config
            Configurations.__instance = self
    def getConfig(self):
        return self.Config
    def getKey(self,Key):
        return self.Config[Key]

import json
class ConfigInterface:
    ConfigurationValues = None
    def __init__(self,ConfigFile):
        with open(ConfigFile , "r") as file:
            data = json.load(file)
            ConfigInterface.ConfigurationValues = data
    def get(self):
        return ConfigInterface.ConfigurationValues
