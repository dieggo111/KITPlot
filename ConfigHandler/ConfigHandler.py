#!/usb/bin/python
import os,sys
from ConfigParser import ConfigParser

class ConfigHandler(ConfigParser):

    def __init__(self, parDict = None):
        ConfigParser.__init__(self)
        self.optionxform = str
        self.__dir = "cfg/"
        #self.__dir = "/home/metzler/KITPlot/cfgSave/"
        self.__prmtr = None     
        if parDict is not None:
            self.init(parDict)
            
    def __cfgExists(self):
        return os.path.exists(self.__cfg)

    def __cfgName(self, name='default'):

        if os.path.isdir(name):
            name = os.path.normpath(name).split("/")[-1] + ".cfg"
            return name
        else:
            name = os.path.splitext(os.path.basename(os.path.normpath(name)))[0] + ".cfg"
            return name

    def __load(self, cfg='default.cfg'):

        cfg = self.__cfgName(cfg)

        if os.path.exists(self.__dir + cfg):
            fullDict = {}

            self.read(self.__dir + cfg)
            for sec in self.sections():
                tmpDict = {}
                for (key,val) in self.items(sec):
                    tmpDict[key] = val
                fullDict[sec] = tmpDict
            self.__prmtr = fullDict

        else:
            sys.exit("No cfg found!")
        
        return fullDict

    def get(self, sec, par=None, dataType = 'string'):
        if self.__prmtr is not None:
            if par is not None:
                if dataType == ('int' or 'integer'):
                    return int(self.__prmtr[sec][par])
                else:
                    return self.__prmtr[sec][par]
            else:
                return self.__prmtr[sec]

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
        
        cfg = self.__cfgName(cfg)
        
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

    def getCfgName(self, name='default'):
        return self.__cfgName(name)


    def setParameter(self, cfg, sec, key, val):

        self.read(cfg)

        with open(cfg,'w') as cfgFile:
            self.set(sec, key, val)
            ConfigParser.write(self,cfgFile)

        return True

    def update(self, Input, InputType, refFile='default.cfg'):

        print "###############################################\n"+"### ConfigHandler update method initialized ###\n"+"###############################################"
               
        if InputType == "File":
            File = os.path.basename(Input)
            print "1 File is ready to be updated according to '" + refFile + "': \n" + str(File)
        elif InputType == "Folder":
            Folder = Input.split("/")[-2] + "/"
            print str(len(self.getFilesInFolder(Input, cfg))) + " file(s) are ready to be updated according to '" + refFile + "':"
            for Name in self.getFilesInFolder(Input, cfg):
               print Name
        print os.path.basename(Input)
        
        refDict = self.__load(self.__dir + refFile)
        oldDict = {}
        config = ConfigParser()
        config.read(self.__dir + File)

#        for sec in ConfigParser().sections():
#            tmpDict = {}
#            for (key,val) in ConfigParser().items(sec):
#                tmpDict[key] = val
#            oldDict[sec] = tmpDict


#        print (oldDict, len(oldDict))
#                    for key in self.__prmtr[sec]:
#                        for old_key in oldDict[old_sec]:
#                            if key == old_key:
#                                if self.__prmtr[sec][key] == oldDict[old_sec][old_key]:
#                                    print "same"
#                                else:
#                                    #print self.__prmtr[sec][key]
#                                    print "dif"
        #TODO compare tmpDict with self.__prmtr

    def getFilesInFolder(self, path, cfg):

        List = []
        for Name in os.listdir(path):
            if "~" in Name or Name == cfg:
                pass
            else:
                List.append(Name)
        return List

    def setType(self,func):
      
        for sec in self.__prmtr:
            for key in self.__prmtr[sec]:
                if callable(func):
                    self.__prmtr[sec][key] = func(self.__prmtr[sec][key])
        return True
        
if __name__ == '__main__':        

    Input = sys.argv[1]
    if len(sys.argv) < 2:
        pass
    else:
        refFile = os.path.basename(sys.argv[2])

    if os.path.isdir(Input):
        ConfigHandler().update(Input, "Folder", refFile)
    elif Input[-4:] == ".cfg":
        ConfigHandler().update(Input, "File", refFile)
    else:
        sys.exit("Unkown input type. Only fodlers or cfg-files can be updated!")

#    write = True
#    
#    pDict = {'General':{'vad_file':'VAD',
#                        'vdd_file':'VDD',
#                        't_file':'temperature',
#                        'path':'/mnt/1-wire/honeywell/'},
#             'Special':{'d':4,
#                        'e':5,
#                        'f':6},
#             'More':{'g':7,
#                     'h':8,
#                     'i':9}}

#    cfg = ConfigHandler()
#    
#    if write:
#        cfg.init(pDict)        
#        cfg.write()
#    else:
#        cfg.load("default.cfg")
        
#    print cfg.get("General","path")
#    print cfg.get("Special","d")
