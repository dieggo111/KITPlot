#!/usb/bin/python
import os,sys
from ConfigParser import ConfigParser

class ConfigHandler(ConfigParser):

    def __init__(self, parDict = None):
        ConfigParser.__init__(self)
        self.__dir = "cfg/"
        self.__prmtr = None     
        if parDict is not None:
            self.init(parDict)
            
    def __cfgExists(self):
        return os.path.exists(self.__cfg)
    
    def __load(self, cfg='default.cfg'):

        if os.path.exists(self.__dir + cfg):

            fullDict = {}
            
            self.read(self.__dir + cfg)
            for sec in self.sections():
                tmpDict = {}
                for (key,val) in self.items(sec):
                    tmpDict[key] = val
                fullDict[sec] = tmpDict                     
        else:
            sys.exit("No cfg found!")

        return fullDict

    def get(self, sec, par):
        if self.__prmtr is not None:
            return self.__prmtr[sec][par]
            
    def getDict(self, sec):
        if self.__prmtr is not None:
        # TODO Try-Except
            return self.__prmtr[sec]
        # sys.exit("Section: %s not defined" %sec)
        
    def getParameters(self):
        return self.__prmtr

    def init(self, fullDict):                    
        if isinstance(fullDict,dict):
        #TODO: Check if val of key is dict
            self.__prmtr = fullDict

    def load(self,cfg='default.cfg'):
        self.__prmtr = self.__load(cfg)

    def setDir(self, dirName="cfg/"):
        self.__dir = dirName

    def setNoDir(self):
        self.__dir = ""
        
    def write(self, cfg='default.cfg', owrite=True):
        #TODO: Add overwrite part
        
        if not os.path.isdir(self.__dir):
            os.makedirs(self.__dir)
        else:
            pass

        with open(self.__dir + cfg,'w') as cfgFile:
            if self.__prmtr is not None:
                for sec in self.__prmtr:
                    self.add_section(sec)
                    for key in self.__prmtr[sec]:
                        self.set(sec,key,self.__prmtr[sec][key])
            ConfigParser.write(self,cfgFile)
                        
    def update(self, cfg='default.cfg'):
        tmpDict = self.__load(self.__dir + cfg)

        #TODO compare tmpDict with self.__prmtr

        
if __name__ == '__main__':        

    write = True
    
    pDict = {'General':{'vad_file':'VAD',
                        'vdd_file':'VDD',
                        't_file':'temperature',
                        'path':'/mnt/1-wire/honeywell/'},
             'Special':{'d':4,
                        'e':5,
                        'f':6},
             'More':{'g':7,
                     'h':8,
                     'i':9}}

    cfg = ConfigHandler()
    
    if write:
        cfg.init(pDict)        
        cfg.write()
    else:
        cfg.load("default.cfg")
        
    print cfg.get("General","path")
    print cfg.get("Special","d")
