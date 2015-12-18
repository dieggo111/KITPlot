import os
import numpy as np
import mysql.connector
import ConfigParser

class KITDataFile(object):

    __dbCnx = None
    __dbCursor = None

    def __init__(self, fileName=None):
        
        self.__x = []
        self.__y = []
        self.__z = []

        # Establish database connection

        if KITDataFile.__dbCnx is None:
            self.__init_db_connection()
        else:
            pass


        # Open file
        
        if fileName is not None:
            with open(fileName, 'r') as file:
                for line in file:
                    splited = line.split();
                    self.__x.append(float(splited[0]))
                    self.__y.append(float(splited[1]))
                    self.__z.append(float(splited[2]))
        else:
            pass
            
        # Allocate sensor name

        self.__name = os.path.basename(fileName).split("-")[0]
        


    def __init_db_connection(self, filename='db.cfg', section='database'):

        cnxConf = ConfigParser.ConfigParser()
        cnxConf.read(filename)

        db_config = {}
        
        if cnxConf.has_section(section):
            for item in cnxConf.items(section):
                db_config[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format(section, filename))
 
        KITDataFile.__dbCnx = mysql.connector.MySQLConnection(**db_config)
        
        if KITDataFile.__dbCnx.is_connected():
            print "Connection established"
        else:
            print "Connection failed"
            return False

        KITDataFile.__dbCursor = KITDataFile.__dbCnx.cursor()
        

    def __gez

    def getDataSet(self, dataSet):
        if (str(dataSet) == "x") | (dataSet == 0) :
            return self.__x
        elif (str(dataSet) == "y") | (dataSet == 1) :
            return self.__y
        elif (str(dataSet) == "z") | (dataSet == 2) :
            return self.__z
        else:
            return []
        

    def getX(self, asarray=False):
        
        if asarray:
            return np.asarray(self.__x)
        else:
            return self.__x


    def getY(self, asarray=False):
        
        if asarray:
            return np.asarray(self.__y)
        else:
            return self.__y
    

    def getZ(self, asarray=False):
        if asarray:
            return np.asarray(self.__z)
        else:
            return self.__z


    def getSize(self):
        return len(self.__x)


    def getName(self):
        return self.__name

