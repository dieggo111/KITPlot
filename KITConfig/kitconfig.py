#!/usr/bin/env python3
import os
import re
import json
import logging
from collections import OrderedDict

class KITConfig(object):
    """ Class that converts json based config files into dictonaries

    The ConfigParser class is used to parse JSON based config files.
    This small program is mainly used in the context of KITPlot and other
    scipts developed in the hardware group of the ETP at KIT.

    """

    defaultConfig = {}
    configDir = ""
    
    def __init__(self, cfg=None, **kwargs):
        """ Initialize KITConfig by loading the config file.

        The __init__ method sets the working directory to ./cfg and loads the
        config file.

        Args:
            cfg (str): The config file that is loaded

        """
        self.__dir = KITConfig.configDir
        self.__cfgFile = ""
        
        self.__cfg = {}
        self.__default = KITConfig.defaultConfig
        
        self.__setupLogger()
        
        if cfg is not None:
            self.load(cfg)

            
    def Default(self, fName='default.cfg'):
        try:
            with open(os.path.join(os.getcwd(), fName), 'r') as defaultCfg:
                self.__default = json.load(defaultCfg, object_pairs_hook=OrderedDict)
        except Exception:
            pass

        try:
            with open(os.path.join(os.getcwd(), fName), 'r') as defaultCfg:
                KITConfig.defaultConfig = json.load(defaultCfg, object_pairs_hook=OrderedDict)
        except Exception:
            raise OSError("Default config file not found")

        
    def Dir(self, directory='cfg/'):
        """ Set the working directory

        Args:
            directory (str): Working directory where the config files are
                located

        """
        try:
            self.__dir = os.path.join(os.getcwd(), directory.lstrip('/\\'))
        except Exception:
            KITConfig.configDir = os.path.join(os.getcwd(), directory.lstrip('/\\'))
    
        
            
    def __getitem__(self, keys):

        # Looking for key in config file
        try:
            return self.__getFromDict(self.__cfg, keys)
        except:
            pass

        # If key is not present in config use default value instead
        # and save that value in the config file
        if len(self.__default):
            try:
                value = self.__getFromDict(self.__default, keys)
                try:
                    self.__setitem__(keys, value)
                except Exception:
                    raise KeyError("Couldn't update Cfg with default value")
                return value
            except Exception:
                raise KeyError("Key is not present in Cfg and default file")
        raise OSError("No default file present")

    
    def __setitem__(self, keys, value):
        """ Set or change a value of a new or existing parameter

        Args:
            key (dict): List of keys with unlimited levels
            value (): Value that will be set

        """

        if isinstance(keys, str):
            keys = [keys]

        #print("KEYTYPE: {0}".format(keys))
        self.__setInDict(self.__cfg, keys, value)
        self.write(self.__cfgFile)
            
        
    def load(self, cfg='default', **kwargs):


        """ Load config file

        Args:
            cfg (str): Name of cfg file inside the working directory

        """
        if self.__cfgFile is "":
            self.__cfgFile = os.path.join(os.getcwd(), self.__dir, self.__getfName(cfg))

        try:
            with open(self.__cfgFile) as cfgFile:
                self.__cfg = json.load(cfgFile, object_pairs_hook=OrderedDict)
            print("Found {0}".format(self.__cfgFile))
        except Exception: 
            if len(self.__default):
                self.__cfg = self.__default
                self.write(self.__cfgFile)
            else:
                raise OSError("Cfg not found and no default config specified")
            
        
    def write(self, cfg='default.cfg'):

        if self.__dir != "" and not os.path.exists(self.__dir):
            os.makedirs(self.__dir)
        
        self.__cfgFile = os.path.join(os.getcwd(), self.__dir, self.__getfName(cfg))
        with open(self.__cfgFile, 'w') as cfgFile:
            json.dump(OrderedDict(self.__cfg), cfgFile, indent=4, sort_keys=True)


    def setDefaultCfg(self, fName='default.cfg'):
        try:
            with open(os.path.join(os.getcwd(), fName), 'r') as defaultCfg:
                self.__default = json.load(defaultCfg, object_pairs_hook=OrderedDict)
        except Exception:
            raise OSError("Default config file not found")


    def setDict(self, dictionary):
        self.__cfg = dictionary
        
        
    def __getfName(self, name='default'):
        if os.path.isdir(str(name)):
            #return os.path.normpath(str(name)).split("/")[-1] + ".cfg"
            return re.split(r'[/\\]', os.path.normpath(str(name)))[-1]+".cfg"
        else:
            return os.path.splitext(os.path.basename(os.path.normpath(str(name))))[0] + ".cfg"
    
            
    # Get data from a dictionary with position provided as a list
    def __getFromDict(self, dataDict, mapList):
        try:
            for key in mapList:
                dataDict = dataDict[key]

            return dataDict
        except Exception:
            raise KeyError("Couln't find {0}".format(mapList))
    
    # Set data in a dictionary with position provided as a list
    def __setInDict(self, dataDict, mapList, value):
        # Set new value if key already exists

        #print("Dict at call: {0}".format(dataDict))
        #print("Maplist at call: {0}".format(mapList))
        #print("Maplist Type: {0}".format(type(mapList)))
        
        for i, key in enumerate(mapList[:-1]):
            
            prevDict = dataDict
            try:
                #print("Before: {0}".format(dataDict))
                #print("Key: {0}".format(key))
                dataDict = dataDict[key]
                #print("After: {0} \ntype: {1}".format(dataDict, type(dataDict)))
            except KeyError:
                dataDict[key] = {mapList[i+1]: None}
                dataDict = dataDict[key]
                #print("Created {0}".format(key))

            if not (isinstance(dataDict, dict) or isinstance(dataDict, OrderedDict)):
                #print("Not of type OrderedDict or dict\n")
                dataDict = prevDict                
                dataDict[key] = {mapList[i+1]: None}
                dataDict = dataDict[key]
                
        dataDict[mapList[-1]] = value

    def get(keyList, defaultValue):
        try:
            return self.__cfg[keyList]
        except Exception:
            return defaultValue

        
    def __setupLogger(self):
        self.__log = logging.getLogger(__name__)
        self.__log.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)

        consoleFormatter = logging.Formatter('%(levelname)s - %(message)s')
        consoleHandler.setFormatter(consoleFormatter)

        self.__log.addHandler(consoleHandler)

        
    # Old API

    def init(self, dictionary):
        self.setDict(dictionary)

    def setParameter(self, cfg, sec, key, val):
        self.__cfg[sec][key] = val
        self.write(cfg)

    def setValue(self, mapList, value):
        """ Set or change a value of a new or existing parameter

        Args:
            mapList (dict): Dictionary with unlimited levels
            value (): Value that will be set

        """
        self.__setInDict(self.__cfg, mapList, value)

           

if __name__ == '__main__':


    testDict = { "a": 1,
                 "b": 2,
                 "c":
                 { "d": 3,
                   "e": 4,
                   "f": 5}}

    print("Set first dictionary")
    cfg = KITConfig()
    cfg.setDict(testDict)
    cfg.write()


    print("Change one value")
    cfg["c","d"]=5

    print("c,f: %s" %cfg["c", "f"])

    d = {'a': 1,
         'b': 2,
         'c': { 'd' : 3,
                'e' : 4,
                'f' : { 'f' : 5,
                        'g' : 6
                },
                'h' : { 'i' : 7,
                        'j' : { 'l' : 8
                        }
                },
                'k' : 9
         }
    }

    print("Update")
    cfg.update(d)
