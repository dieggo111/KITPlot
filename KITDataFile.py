import os
import numpy as np

class KITDataFile(object):

    def __init__(self, fileName):
        
        self.__x = []
        self.__y = []
	
        with open(fileName, 'r') as file:
            for line in file:
                splited = line.split();
                self.__x.append(abs(float(splited[0])))
                self.__y.append(abs(float(splited[1])))

        self.__name = os.path.basename(fileName).split("-")[0]

  
    def getDataSet(self, dataSet):
        if (str(dataSet) == "x") | (dataSet == 0) :
            return self.__x
        elif (str(dataSet) == "y") | (dataSet == 1) :
            return self.__y
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


    def getSize(self):
        return len(self.__x)


    def getName(self):
        return self.__name


    def getScaleX(self):
	return min(__x), max(__x) 

    def getScaleY(self):
	return 0, 1.3*max(__y)

