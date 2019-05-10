#!/usr/bin/env python3
#pylint: disable=C0103,W0201,W0703,C0111,W0702,R1710,R1702
import os
import re
import inspect
import json
import logging
from pathlib import Path
from collections import OrderedDict

class KITConfig(object):
    """ Class that converts json based config files into dictonaries

    The ConfigParser class is used to parse JSON based config files.
    This small program is mainly used in the context of KITPlot and other
    scipts developed in the hardware group of the ETP at KIT.

    """

    defaultConfig = {}
    defaultConfigPath = os.path.join(
        Path(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))).parents[0],
        "Utils")
    configDir = ""

    def __init__(self, cfg=None):
        """ Initialize KITConfig by loading the config file.

        The __init__ method sets the working directory to ./cfg and loads the
        config file.

        Args:
            cfg (str): The config file that is loaded

        Members:
            __cfgFile (str): absolute path of cfg file
            __dir (str): absolute path of cfg dir where cfg are stored
            __default (OrderedDict): default config dictionary
            __cfg (OrderedDict): loaded config dictionary

        """
        self.log = logging.getLogger(__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        if self.log.hasHandlers() is False:
            format_string = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            formatter = logging.Formatter(format_string)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.log.addHandler(console_handler)

        self.__dir = KITConfig.configDir
        self.__cfgFile = cfg

        self.__cfg = {}
        # initialize the default dict
        self.__default = KITConfig.defaultConfig

        if cfg is not None:
            self.load(cfg)

    def Default(self, fName='default.cfg'):
        """Load parameters from default config Set default config file which
        is the blueprint for creating new cfg files"""
        # try:
        if os.path.isabs(fName):
            with open(fName, 'r') as defaultCfg:
                self.__default = json.load(defaultCfg, object_pairs_hook=OrderedDict)
        else:
            with open(os.path.join(os.getcwd(), "KITPlot", "Utils", fName), 'r') as defaultCfg:
                self.__default = json.load(defaultCfg, object_pairs_hook=OrderedDict)
        # except (TypeError, FileNotFoundError):
        #     pass
        try:
            with open(os.path.join(KITConfig.defaultConfigPath, fName), 'r') as defaultCfg:
                KITConfig.defaultConfig = json.load(defaultCfg, object_pairs_hook=OrderedDict)
        except Exception as e:
            self.log.debug(e)
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

    def getDict(self):
        return self.__cfg

    def getDefDict(self):
        return self.__default

    def __getitem__(self, keys):

        if isinstance(keys, str):
            keys = [keys]
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

        self.__setInDict(self.__cfg, keys, value)

        self.write(self.__cfgFile, log=False)


    def load(self, cfg='default', log=True):
        """ Look at path in __cfgFile or create path if not present. Try to
        load config file. If it is not there yet, then create a cfg
        file using the default values.

        Args:
            cfg (str): Name of the input without ".cfg" ending
        """
        if self.__cfgFile is None:
            self.__cfgFile = os.path.join(self.__dir, self.__getfName(cfg))

        try:
            with open(self.__cfgFile) as cfgFile:
                self.__cfg = json.load(cfgFile, object_pairs_hook=OrderedDict)
            if log is True:
                self.log.info("Found %s", self.__cfgFile)
        except (TypeError, FileNotFoundError):
            if self.__default != {}:
                self.__cfg = self.__default
                self.write(self.__cfgFile, log=True)
            else:
                raise OSError("Cfg not found and no default config specified")


    def write(self, cfg='default.cfg', log=True):
        """Create new cfg file. If folder doesn't exist create it.

        Args:
            cfg (str): absolute path of cfg file that needs to be written
        """
        if self.__dir != "" and not os.path.exists(self.__dir):
            os.makedirs(self.__dir)
        with open(self.__cfgFile, 'w') as cfgFile:
            json.dump(OrderedDict(self.__cfg), cfgFile, indent=4, sort_keys=True)
            if log is True:
                self.log.info("Created %s", self.__cfgFile)


    # def setDefaultCfg(self, fName='default.cfg'):
    #     try:
    #         with open(os.path.join(KITConfig.defaultConfigPath, fName), 'r') as defaultCfg:
    #             self.__default = json.load(defaultCfg, object_pairs_hook=OrderedDict)
    #     except Exception:
    #         raise OSError("Default config file not found")


    def setDict(self, dictionary):
        self.__cfg = dictionary


    def __getfName(self, name='default'):
        if os.path.isdir(str(name)):
            #return os.path.normpath(str(name)).split("/")[-1] + ".cfg"
            return re.split(r'[/\\]', os.path.normpath(str(name)))[-1]+".cfg"
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
        for i, key in enumerate(mapList[:-1]):

            prevDict = dataDict
            try:

                dataDict = dataDict[key]
            except KeyError:
                dataDict[key] = {mapList[i+1]: None}
                dataDict = dataDict[key]

            if not isinstance(dataDict, (dict, OrderedDict)):
                dataDict = prevDict
                dataDict[key] = {mapList[i+1]: None}
                dataDict = dataDict[key]

        dataDict[mapList[-1]] = value

    def getDir(self):
        return self.__dir

    def get(self, keyList, defaultValue):
        try:
            return self.__cfg[keyList]
        except Exception:
            return defaultValue
