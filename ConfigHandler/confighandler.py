import os
import json
from collections import OrderedDict

class ConfigHandler(object):
    """ Class that converts json based config files into dictonaries

    The ConfigParser class is used to parse JSON based config files. 
    This small program is mainly used in the context of KITPlot and other
    scipts developed in the hardware group of the ETP at KIT.
    
    """
    
    def __init__(self,cfg=None):
        """ Initialize ConfigHandler by loading the config file.
        
        The __init__ method sets the working directory to ./cfg and loads the 
        config file.

        Args:
            cfg (str): The config file that is loaded

        """
        self.__dir = ""
        if cfg is not None:
            self.name = self.getCfgName(cfg)
            self.__cfg = self.__load(cfg)
        
    def __load(self,cfg='default.cfg'):
        self.name = self.getCfgName(cfg)
        try:
            with open(self.__dir+self.name) as cfgFile:
                return json.load(cfgFile, object_pairs_hook=OrderedDict)
        except:
            raise OSError("No file found")
        
    def get(self,sec=None,par=None):      
        """ Get the value of (par)ameter in the given (sec)tion

        Args:
            sec (str): Section where the parameter is located.
            par (str): Parameter

        """

        # Return whole dictionary
        if sec==None:
            return self.__cfg
        # Return one section
        elif sec!=None and par==None:
            try:
                return self.__cfg[sec]
            except:
                raise IOError("Section not found!")
        else:
            try:
                return self.__cfg[sec][par]
            except:
                raise IOError("Section and/or parameter not found")

            
    def setDir(self,directory='cfg/'):
        """ Set the working directory

        Args:
            directory (str): Working directory where the config files are 
                located
        
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        self.__dir = directory

    def load(self,cfg='default.cfg'):
        """ Load config file

        Args:
            cfg (str): Name of cfg file inside the working directory

        """
        self.__cfg = self.__load(cfg)
        
    def setValue(self,mapList,value):
        """ Set or change a value of a new or existing parameter

        Args:
            mapList (dict): Dictionary with unlimited levels
            value (): Value that will be set 

        """
        self.__setInDict(self.__cfg,mapList,value)
        
    def write(self, cfg='default.cfg'):
        self.name = self.getCfgName(cfg)
        with open(self.__dir + self.name,'w') as cfgFile:
            json.dump(OrderedDict(self.__cfg), cfgFile, indent=4, sort_keys=False)


    def setDict(self, dictionary):
        self.__cfg = dictionary 
        

    def __getitem__(self,keys):
        try:
            return self.__cfg[keys] 
        except(KeyError):
            pass

        try:
            return self.__getFromDict(self.__cfg,keys)
        except:
            raise KeyError("Key not found")


    def __setitem__(self, key, value):
        self.__setInDict(self.__cfg,key,value)
        self.write(self.name)


    def getCfgName(self, name='default'):
        if os.path.isdir(str(name)):
            return os.path.normpath(str(name)).split("/")[-1] + ".cfg"
        else:
            return os.path.splitext(os.path.basename(os.path.normpath(str(name))))[0] + ".cfg"
    
    # Get data from a dictionary with position provided as a list
    def __getFromDict(self, dataDict, mapList):    
        for k in mapList: dataDict = dataDict[k]
        return dataDict
    
    # Set data in a dictionary with position provided as a list
    def __setInDict(self, dataDict, mapList, value): 
        for k in mapList[:-1]: dataDict = dataDict[k]
        dataDict[mapList[-1]] = value

        
    # Old API
        
    def init(self, dictionary):
        self.setDict(dictionary)
        
    def setParameter(self, cfg, sec, key, val):
        self.__cfg[sec][key] = val
        self.write(cfg)
        
if __name__ == '__main__':

    
    testDict = { "a": 1,
                 "b": 2,
                 "c":
                 { "d": 3,
                   "e": 4 }}

    cfg = ConfigHandler()
    cfg.setDict(testDict)
    cfg.write()

    cfg["c","d"]=5
    
                 