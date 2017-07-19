#!/usr/bin/env python3

import os,sys
import numpy as np
import mysql.connector
from .KITConfig import KITConfig
from collections import OrderedDict
import datetime

class KITData(object):
    """ The KITData class is a very simple data container that is able
    to connect to the IEKP database in order to read and store all relevant
    data into private member variables.

    """

    __dbCnx = None
    __dbCrs = None

    def __init__(self, dataInput=None, measurement="probe",
                 credentials='db.cfg', show_input=None):
        """ Initialize KITData object based on the input that is passed.

        Args:
            dataInput (None|pid|file): Only pid inputs will fill all additional
                information automatically
            measurement (probe|alibava): Specify if PID belongs to a probe
                station or alibava measurement
            credentials (str): Specify the credentials file for the database if
                the file is not located in the current working directory

        """
        self.__id = None
        self.__name = None

        self.__x = []
        self.__y = []
        self.__z = []

        self.__dx = []
        self.__dy = []
        self.__dz = []

        self.__temp = []
        self.__humid = []

        self.__px = None
        self.__py = None
        self.__pz = None

        self.__t0 = None
        self.__h0 = None

        self.__RPunchDict = None
        self.__credentials = credentials

        # ALiBaVa specific
        self.__gain = None
        self.__seed = None
        self.__seederr = None

        # Empty object
        if dataInput is None:
            pass

        # A single PID for either a probe station or ALiBaVa measurement
        # Sometimes integers are interpreted as strings, therefore
        # isdigit() is called to check for missinterpreted integers
        elif isinstance(dataInput, int) or dataInput.isdigit():
            self.__id = dataInput

            # Establish database connection if its no already established
            if KITData.__dbCrs is None:
                self.__init_db_connection()

            # Distinguish between probe station and ALiBaVa ID
            if measurement is "alibava":
                if show_input is not False:
                    print("Input: ALiBaVa run")
                else:
                    pass
                self.__allo_db_alibava(dataInput)
            elif measurement is "probe" and show_input is not False:
                if show_input is not False:
                    print("Input: Probe station PID")
                else:
                    pass
                self.__allo_db(dataInput)

        # Check if dataInput is a file
        elif isinstance(dataInput, str) and os.path.isfile(dataInput):

            print("Input: File: " + dataInput)

            with open(dataInput, 'r') as inputFile:
                for line in inputFile:
                    splited = line.split();

                    try:
                        # First two columns are always interpreted as x and y
                        self.__x.append(float(splited[0]))
                        self.__y.append(float(splited[1]))

                        # Three columns are seen as x,y,z
                        if len(splited) == 3:
                            self.__z.append(float(splited[2]))
                        # Four columns represent x,y and their errors dx,dy
                        elif len(splited) == 4:
                            self.__dx.append(float(splited[2]))
                            self.__dy.append(float(splited[3]))
                        # Six column are seen as x,y,z and their errors dx,dy,dz
                        elif len(splited) == 6:
                            self.__z.append(float(splited[2]))
                            self.__dx.append(float(splited[3]))
                            self.__dy.append(float(splited[4]))
                            self.__dz.append(float(splited[5]))
                        # Rpunch measurement from file
                        elif len(splited) > 6 and "REdge" in dataInput:
                            self.__z.append(float(splited[2]))
                    except:
                        pass

                # Reorder variables if file contains a RPunch measurement
                if self.checkRpunch(self.__x):

                    dic = OrderedDict()
                    bias = self.__x[0]
                    ix = []
                    iy = []

                    # Rpunch Ramps: x = V_bias, y = V_edge, z = I_edge
                    for (valX, valY, valZ) in zip(self.__x, self.__y, self.__z):
                        # create the IV keys for one bias voltage
                        if bias == valX:
                            ix.append(valY)
                            iy.append(valZ)
                        else:
                            dic[bias] = zip(ix,iy)
                            bias = valX
                            ix = [valY]
                            iy = [valZ]

                    dic[bias] = zip(ix,iy)

                    self.__RPunchDict = dic

                else:
                    self.__name = os.path.basename(dataInput).split(".")[0]
                    for char in os.path.basename(dataInput):
                        if char == "-":
                            self.__name = os.path.basename(dataInput).split("-")[0]
                        else:
                            pass


        # Data input contains list of KITData objects
        # TODO
        elif isinstance(dataInput,list) and all(isinstance(i, KITData)
                                                for i in dataInput):

            self.__px = dataInput[0].getParaX()
            self.__py = dataInput[0].getParaY()
            self.__pz = dataInput[0].getParaZ()
            self.__name = dataInput[0].getName()
            self.__Fp = dataInput[0].getFluenceP()

            for kitFile in dataInput:
                self.__x.append(kitFile.getX()[0])
                self.__y.append(kitFile.getY()[0])
                self.__z.append(kitFile.getZ()[0])
                self.__dy.append(kitFile.getdY()[0])


        else:
            raise OSError("Input could not be identified (Input: %s)"
                          %(dataInput))


    def getRPunchDict(self):
        return self.__RPunchDict

    def checkRpunch(self, List):

        for val in List:
            if List.count(val) > 2:
                return True
            else:
                return False

    def __init_db_connection(self, credentials='db.cfg', section='database'):
        """Initialize db_connection and set static connection and curser

        Args:
            filename: database config file that contains all necessary data
            section: config section where login data can be found

        """


        try:
            cnxConf = KITConfig()

            cnxConf.load(credentials)
            db_config = cnxConf[section]

            KITData.__dbCnx = mysql.connector.MySQLConnection(**db_config)

#            if KITData.__dbCnx.is_connected():
            print("Database connection established")
#            else:
#                sys.exit("Connection failed! Did you changed "
#                         "the database parameters in 'db.cfg'? ")

            KITData.__dbCrs = KITData.__dbCnx.cursor()
# TODO: except case for calling a none-existend probeID
        except:
            if "db.cfg" not in os.listdir(os.getcwd()):
                self.__createCfg()
            else:
                raise ValueError("No credentials file found. "
                                 "Please add correct database parameters "
                                 "to 'db.cfg'")


    def __createCfg(self):
        """Create empty config file dummy that has to be filled

        """

        dic = { "database":
                {
                    "host": "",
                    "database": "",
                    "user": "",
                    "passwd": ""}}

        cfg = KITConfig()
        cfg.setDict(dic)
        cfg.write("db.cfg")


    def __check_if_folder_pid(self, fileName):
        """Check if file contains PIDs or datasets

        Args:
            fileName: file with pids or datasets

        Returns:
            True|False whether file contains PIDs(True) or datasets(False)

        """

        with open(fileName) as file:
            if len(file.readline().split()) == 1:
                return True
            else:
                return False


    def __allo_db(self, pid):
        """Allocate measurement information.
           This works only if database connection is already established.

        Args:
            pid: probe id in the IEKP database

        """

        qryProbeData = ("SELECT * FROM probe_data WHERE probeid=%s" %(pid))
        KITData.__dbCrs.execute(qryProbeData)
        for (uid, pid, x, y, z, t, h) in KITData.__dbCrs:
            self.__x.append(x)
            self.__y.append(y)
            self.__z.append(z)
            self.__temp.append(t)
            self.__humid.append(h)

        name = None

        qryProbe = ("SELECT * FROM probe WHERE probeid=%s" %(pid))
        KITData.__dbCrs.execute(qryProbe)

        for (pid, sid, pX, pY, pZ, date, op, t, h,
             stat, f, com, flag, cernt, guard, aLCR,
             mLCR, n, start, stop, bias, vdep, fmode) in KITData.__dbCrs:

            self.__px = pX
            self.__py = pY
            self.__t0 = t
            self.__h0 = h
            name = sid

        qrySensorName = ("SELECT * FROM info WHERE id=%s" %(name))
        KITData.__dbCrs.execute(qrySensorName)
        for (sid,name,project,man,cls,stype,spec,
             thick,width,length,strips,pitch,coupling,
             date,op,inst,stat,bname,Fp,Fn,par,defect) in KITData.__dbCrs:

            self.__name = name
            self.__Fp = Fp


    def __allo_db_alibava(self, run):

        self.__px = "Voltage"
        self.__py = "Signal"
        self.__pz = "Annealing"
        self.__name = "ALiBaVa"

        tmpID = None
        tmpDate = None
        annealing = 0

        qryRunData = ("SELECT voltage, current, gain, electron_sig, "
                      "signal_e_err, SeedSig_MPV, SeedSig_MPV_err, id, date "
                      "FROM alibava WHERE run=%s" %(run))
        KITData.__dbCrs.execute(qryRunData)

        for (voltage, current, gain, electron_sig, signal_e_err,
             SeedSig_MPV, SeedSig_MPV_err, id, date) in KITData.__dbCrs:
            self.__x.append(voltage)
            self.__y.append(electron_sig)
            self.__dy.append(signal_e_err)
            self.__gain = gain
            self.__seed = SeedSig_MPV
            self.__seederr = SeedSig_MPV_err

            tmpID = id
            tmpDate = date

        qryAnnealing = ("SELECT date,equiv FROM annealing "
                        "WHERE id=%s and "
                        "TIMESTAMP(date)<='%s'" %(tmpID,tmpDate))

        try:
            KITData.__dbCrs.execute(qryAnnealing)
        except mysql.connector.errors.ProgrammingError:
            sys.exit("Couldn't find run " + run + " in Database")

        for (date,equiv) in KITData.__dbCrs:
            annealing += equiv
        self.__z.append(annealing)

        qrySensorName = ("SELECT name, F_p_aim_n_cm2 "
                         "FROM info WHERE id=%s" %(tmpID))

        KITData.__dbCrs.execute(qrySensorName)

        for (name, Fp) in KITData.__dbCrs:
            self.__name = name
            self.__Fp = Fp


    def dropXLower(self, xlow=0):
        """Drops datasets if x < xlow

        Args:
            xlow: everything below xlow will be droped

        Returns:
            True

        """

        xTemp = []
        yTemp = []

        for i,x in enumerate(self.__x):
            if x >= float(xlow):
                xTemp.append(x)
                yTemp.append(self.__y[i])

        self.__x = xTemp
        self.__y = yTemp

        return True


    def dropXHigher(self, xhigh=0):
        """Drops datasets if x > xhigh

        Args:
            xhigh: everything above xhigh will be droped

        Returns:
            True

        """

        xTemp = []
        yTemp = []

        for i,x in enumerate(self.__x):
            if x <= float(xhigh):
                xTemp.append(x)
                yTemp.append(self.__y[i])

        self.__x = xTemp
        self.__y = yTemp

        return True


    def dropYLower(self, ylow=0):
        """Drops datasets if y < ylow

        Args:
            ylow: everything below ylow will be droped

        Returns:
            True

        """

        xTemp = []
        yTemp = []

        for i,y in enumerate(self.__y):
            if y >= float(ylow):
                xTemp.append(self.__x[i])
                yTemp.append(y)

        self.__x = xTemp
        self.__y = yTemp

        return True


    def dropYHigher(self, yhigh=0):
        """Drops datasets if y > yhigh

        Args:
            yhigh: everything below yhigh will be droped

        Returns:
            True

        """

        xTemp = []
        yTemp = []

        for i,y in enumerate(self.__y):
            if y <= float(yhigh):
                xTemp.append(self.__x[i])
                yTemp.append(y)

        self.__x = xTemp
        self.__y = yTemp

        return True


    def setRange(self, var="x", low=0, high=0):
        """Set a certain data range. Every dataset outside this
        range will be droped.

        Args:
            var ("x"|"y"): range referes to either x or y
            low: lower limit
            high: upper limit

        """

        if var is "x":
            self.dropXLower(low)
            self.dropXHigher(high)
        elif var is "y":
            self.dropYLower(low)
            self.dropYHigher(high)

        return True


    def includesErrors(self):
        return True if len(self.__dx) != 0 else False


    ###################
    ### Set methods ###
    ###################


    def setX(self, inputArray=None):
        """Set new or initialize x values of data file

        Args:
            inputArray: array or list of floats

        Returns:
            True|False if the data format is correct or wrong

        """

        if inputArray is not None:
            try:
                self.__x = inputArray
                return True
            except:
                print("Cannot set x: wrong format")
                return False


    def setY(self, inputArray=None):
        """Set new or initialize y values of data file

        Args:
            inputArray: array or list of floats

        Returns:
            True|False if the data format is correct or wrong

        """

        if inputArray is not None:
            try:
                self.__y = inputArray
                return True
            except:
                print("Cannot set y: wrong format")
                return False


    def setZ(self, inputArray=None):
        """Set new or initialize z values of data file

        Args:
            inputArray: array or list of floats

        Returns:
            True|False if the data format is correct or wrong

        """


        if inputArray is not None:
            try:
                self.__z = inputArray
                return True
            except:
                print("Cannot set z: wrong format")
                return False


    def setData(self, **kwargs):
        """Set whole data sets

        Args:
            kwargs (x=[],y=[],z=[]): only x,y,z will be considered

        Returns:
            True

        """

        for key in kwargs:
            if key is "x":
                self.setX(kwargs[key])
            elif key is "y":
                self.setY(kwargs[key])
            elif key is "z":
                self.setZ(kwargs[key])
            return True


    def setName(self, name=""):
        """Set name of data file

        Args:
            name: name of data file

        Returns:
            True

        """

        self.__name = name
        return True


    def setPX(self, paraX=""):
        """Set x parameter name of data file

        Args:
            paraX: x parameter name of data file

        Returns:
            True

        """

        self.__px = paraX

        return True



    def setPY(self, paraY=""):
        """Set y parameter name of data file

        Args:
            paraY: y parameter name of data file

        Returns:
            True

        """

        self.__py = paraY

        return True


    ###################
    ### Get Methods ###
    ###################

    def getData(self, dataSet="x"):
        """Returns x or y array

        Args:
            dataSet ("x"|"y"): whether x or y data will be returned

        Returns:
            List of x or y data set

        """

        if (str(dataSet) == "x") | (dataSet == 0) :
            return self.__x
        elif (str(dataSet) == "y") | (dataSet == 1) :
            return self.__y
        else:
            return []

    def getRun(self):
        """Returns PID or Run number

        Returns:
            PID/Run

        """

        return self.__id


    def getID(self):
        """Returns PID or Run number

        Returns:
            PID/Run

        """

        return self.__id


    def getX(self, asarray=False):
        """Returns x dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of x dataset

        """
        if asarray:
            return np.asarray(self.__x)
        else:
            return self.__x


    def getY(self,  asarray=False):
        """Returns y dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of y dataset

        """

        if asarray:
            return np.asarray(self.__y)
        else:
            return self.__y

    def getZ(self, asarray=False):
        """Returns z dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of z dataset

        """

        if asarray:
            return np.asarray(self.__z)
        else:
            return self.__z

    def getSeed(self):
        """Returns dx dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of dy dataset

        """
        return self.__seed

    def getSeederr(self):
        """Returns dx dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of dy dataset

        """
        return self.__seederr

    def getGain(self):
        """Returns dx dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of dy dataset

        """
        return self.__gain


    def getdX(self, asarray=False):
        """Returns dx dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of dy dataset

        """
        if asarray:
            return np.asarray(self.__dx)
        else:
            return self.__dx


    def getdY(self, asarray=False):
        """Returns dy dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of dy dataset

        """
        if asarray:
            return np.asarray(self.__dy)
        else:
            return self.__dy


    def getdZ(self, asarray=False):
        """Returns dz dataset as list or array

        Args:
            asarray (True|False): dataset will be returned as
                array(True) or list(false)

        Returns:
            list or array of dy dataset

        """
        if asarray:
            return np.asarray(self.__dz)
        else:
            return self.__dz


    def getSize(self):
        """Returns size of dataset

        Returns:
            Int: length of dataset

        """

        return len(self.__x)


    def getName(self):
        """Returns name parameter

        Returns:
           string: name of dataset

        """

        return self.__name


    def getParaX(self):
        """Returns name of x variable

        Returns:
            string: name of x variable

        """

        return self.__px


    def getParaY(self):
        """Returns measured variable

        Returns:
            string: measured variable

        """

        return self.__py

    def getParaZ(self):
        """Returns measured variable

        Returns:
            string: measured variable

        """

        return self.__pz



    def getTemp(self):
        """Returns measured temperature

        Returns:
            float: measured temperature

        """

        return float(self.__t0)


    def getHumidity(self):
        """Returns measured humidity

        Returns:
            float: measured humidity

        """

        return self.__h0


    def getFluenceP(self):
        """Returns fluence of irradiated sensors

        Returns:
            string: fluence of irradiated sensor

        """

        return self.__Fp


    #TODO: Do we need these two methods?
    def getScaleX(self):
        """Returns min and max of x dataset

        Returns:
            float,float: min and max of x

        """

        return min(self.__x), max(self.__x)

    def getScaleY(self):

        return 0, 1.3*max(__y)


if __name__ == '__main__':

    data = KITData(38268)
    print(data.getX())
