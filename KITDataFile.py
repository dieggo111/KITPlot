import os
import numpy as np

class KITDataFile(object):

    def __init__(self, fileName):
        
        self.__x = []
        self.__y = []
        self.__z = []

        with open(fileName, 'r') as file:
            for line in file:
                splited = line.split();
                self.__x.append(float(splited[0]))
                self.__y.append(float(splited[1]))
                self.__z.append(float(splited[2]))

        self.__name = os.path.basename(fileName).split("-")[0]

        print self.__name


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

