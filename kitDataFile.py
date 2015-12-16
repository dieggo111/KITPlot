class kitDataFile:

    __x = []
    __y = []
    __z = []
    
    def __init__(self, fileName):

        with open(fileName, 'r') as file:
            for line in file:
                splited = line.split();
                self.__x.append(float(splited[0]))
                self.__y.append(float(splited[1]))
                self.__z.append(float(splited[2]))


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

