import os,sys
import numpy as np
import mysql.connector
import ConfigParser

class KITDataFile(object):

    __dbCnx = None
    __dbCrs = None

    def __init__(self, input=None):
        
        self.__x = []
        self.__y = []
        self.__z = []
        self.__temp = []
        self.__humid = []
        self.__name = None
        self.__pid = None        
        self.__px = None
        self.__py = None
        self.__t0 = None
        self.__h0 = None
        
        if isinstance(input, int):
            self.__pid = input
            self.__init_db_connection() # Establish database connection
            self.__allo_db(input)
        
        elif input.isdigit():
            print "Input: ProbeID"
            self.__pid = input
            self.__init_db_connection() # Establish database connection
            self.__allo_db(input)
        
        elif os.path.isfile(input):

            print "Input: File"
        
            with open(input, 'r') as file:
                for line in file:
                    splited = line.split();
                    self.__x.append(float(splited[0]))
                    self.__y.append(float(splited[1]))

                    if len(splited) > 2:
                        self.__z.append(float(splited[2]))

            self.__name = os.path.basename(input).split("-")[0]
        
        #elif self.__check_if_folder_pid(input):
        #    print "Input: Folder"
        #    self.__init_db_connection() # Establish database connection

        else:
            raise OSError("Input could not be identified (Input: %s)" %(input))

    def __init_db_connection(self, filename='db.cfg', section='database'):

        if not os.path.isfile(filename):            
            self.__createCfg()        
            sys.exit("Please add database parameters to 'db.cfg' ")

        else:
        
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
                sys.exit("Connection failed! Did you changed the database parameters in 'db.cfg'? ")
                
            KITDataFile.__dbCrs = KITDataFile.__dbCnx.cursor()
        
       
    def __createCfg(self):
        
        with open('db.cfg','w') as cfg:
            cfg.write("[database]\n")
            cfg.write("hostname=\n")
            cfg.write("database=\n")
            cfg.write("user=\n")
            cfg.write("passwd=")


    def __check_if_folder_pid(self, fileName):
        
        with open(fileName) as file:
            if len(file.readline().split()) == 1:
                return True
            else:
                return False 
        

    def __allo_db(self, pid):

        qryProbeData = ("SELECT * FROM probe_data WHERE probeid=%s" %(pid))
        KITDataFile.__dbCrs.execute(qryProbeData)
        for (uid, pid, x, y, z, t, h) in KITDataFile.__dbCrs:
            self.__x.append(x)
            self.__y.append(y)
            self.__z.append(z)
            self.__temp.append(t)
            self.__humid.append(h)
            
        name = None

        qryProbe = ("SELECT * FROM probe WHERE probeid=%s" %(pid))
        KITDataFile.__dbCrs.execute(qryProbe)

        for (pid, sid, pX, pY, pZ, date, op, t, h, stat, f, com, flag, cernt, guard, aLCR, 
             mLCR, n, start, stop, bias, vdep, fmode) in KITDataFile.__dbCrs:
            self.__px = pX
            self.__py = pY
            self.__t0 = t
            self.__h0 = h
            name = sid
            
        qrySensorName = ("SELECT * FROM info WHERE id=%s" %(name))
        KITDataFile.__dbCrs.execute(qrySensorName)
        for (sid,name,project,man,cls,stype,spec,thick,width,length,strips,
             pitch,coupling,date,op,inst,stat,bname,Fp,Fn,par,defect) in KITDataFile.__dbCrs:
            self.__name = name
            

    def getDataSet(self, dataSet):
        if (str(dataSet) == "x") | (dataSet == 0) :
            return self.__x
        elif (str(dataSet) == "y") | (dataSet == 1) :
            return self.__y
        else:
            return []


    def getID(self):
        return self.__pid


    def getX(self, asarray=False):
        
        if asarray:
            return np.asarray(self.__x)
        else:
            return self.__x


    def getY(self,  asarray=False):
        
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


    def getParaX(self):
        return self.__px


    def getParaY(self):
        return self.__py


    def getTemp(self):
        return self.__t0


    def getHumidity(self):
        return self.__h0


    def getScaleX(self):
	return min(__x), max(__x) 


    def getScaleY(self):
	return 0, 1.3*max(__y)


