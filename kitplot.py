#!/usr/bin/env python3

import numpy as np
import ROOT
import os, sys
from .kitdata import KITData
from .ConfigHandler import ConfigHandler
from .LegHandler import LegHandler
from collections import OrderedDict

""" A simple ROOT based python plot script

1) Synopsis:
Hello World! Welcome to the KITPlot script. This script was created by
Daniel Schell (daniel.schell@kit.edu) and Marius Metzler
(marius.metzler@kit.edu). This script is about creating distinctive,
well-arranged plots especially for bachelor/master students at IEKP, who find
common, commercially availible plotting software as lame and unconvinient
as we do. The greatest benifit of KITPlot is that it is able to directly
communicate with the IEKP database. It also automatizes standard operations and
procedures as well as making plots easily editable and reproducible via
distinctive config files.

2) Structure:
The script consists of 4 modules:
    a) The KITData module determines the input type of the data you want to
       plot. It accepts:
        - single .txt file that contains a data table (x-value, y-value,
          x-error, y-error seperated by tabs or spaces)
        - folder that houses several .txt files
        - single ID ('probe ID' for probe station measurements,
          'Run' for alibava measurements)
        - single .txt file that contains a list of IDs

        KITData then creates a KITData object for every graph, which contains
        the data table and provides convenient methods for handling all
        sensor parameters.

    b) The KITPlot module handles the conversion of a given input type into
       ROOT objects via pyROOT. It then handles all the plotting and drawing
       by using parameters from a .cfg file. Eventually, the output contains:
        - 2 plot graphics (.png and .pdf file) that will be automatically
          stored in your output folder (will be created in your main
          folder if necessary)
        - and a .cfg file that will be automatically stored in your cfg folder
          (will be created in your main folder if necessary)

    c) The LegHandler module handles the arrangement, position and style of the
       legend box and its elements. It also uses a very rudimentary algorithm
       to search for the most convinient spot inside the canvas
       (one of the 4 corners), so that the legend doesn't cover any data points.

    d) The ConfigHandler module writes/reads/edits a plot-specific .cfg file.
       Since KITPlot is console-based and has no graphical interface, the
       config file solution makes up for it.

3) Installation:
    a) Create a main folder and give it a nice name (f.e. 'KITPlot')
    b) Clone the KITPlot repository from 'https://github.com/SchellDa/KITPlot',
       put its content inside an extra folder within your main folder and name
       it 'modules'. If you feel the need to name it otherwise you will have to
       append its path the sys.path list).
    c) Download and install python 2.7 on your system
       (https://www.python.org/downloads/).
    d) The most recent version of python 2 contains 'pip', a download
       manager/installer for python modules, which should be used to download
       the following modules:
        'numpy', 'mysql.connector, 'ConfigParser' and 'collections'
       (the rest should be standard python modules... there's nothing fancy
        here!').
    e) Download and build ROOT v5.34/36 on your system. When building ROOT,
       make sure you enable the use of pyROOT. This is easy on Linux. However,
       doing this on Windows or Mac is a different story... although it's
       generally possible to do this on every system.
    f) For security reasons the login

4) Let's get started:
    Before creating your first plot you need to write a few lines of code for
    yourself. Create a 'main.py' file import KITPlot and KITData as well as sys
    or other modules you need. KITPlot needs at least 1 arguement to do its
    magic. A second argument is optional.
        - First argument: data input. As described earlier, this can be a path
          of a file, folder or a run number from the database.

        - Second argument: cfg file. If this is not given (None), then the
          script will search the cfg folder for a cfg file with the same name
          as the input. If you want to use a cfg file from another plot then
          this argument should be the path of this cfg file. Bottom line: names
          are important! Do not try to plot two folders that happen to have the
          same name. The former output will be overwritten with the new plot.

    A basic example of a main file could look like this:

    ####################################################

    import sys
    import numpy as np
    import ROOT
    sys.path.append('modules/')
    from KITData import KITData
    from KITPlot import KITPlot

    if len(sys.argv) > 2:
        kPlot1 = KITPlot(sys.argv[1],sys.argv[2])
    else:
        kPlot1 = KITPlot(sys.argv[1])


    kPlot1.draw("APL")

    raw_input()

    ####################################################

    If no errors are being raised, the plot will show up on your screen.
    You can now start to edit plot with the related cfg file in your cfg folder.

5) cfg file:
    Most parameters in our cfg file are self-explanatory. Some have a special
    syntax that needs be considered or need some explanation:

    - 'Range = [200:1000]': sets axis range from 200 to 1000 units.
                            Mind the brackets!
    - 'Font = 62': 62 is standard arial, bulky and ideal for presentations.
                   See ROOT documention for other options.
    - 'Log = False': This needs to be a boolean value. Remember that having a 0
                     in your data table may raise errors.
    - 'Abs = True': This needs to be a boolean value.
    - 'Title = Voltage (V)': You can announce special characters here with an
                             '#' like '#circ', '#sigma' or super/subscript
                             by '_{i}' and '^{2}'.
    - 'GraphGroup = off': Default values are 'off', 'name', 'fluence'.
                          Sometimes you might want to visualize that certain
                          graphs belong together by giving them a similar color.
                          'off' will just alter marker color and style for
                          every graph. By choosing 'name', all graphs that
                          share the first 5 letters of their name will be drawn
                          in the same color but with altering markers (f.e.
                          sensors of the same type but from different wafers).
                          If 'fluence' is choosen then then sensors with equal
                          fluences will be drawn in the same color (the flunces
                          are retreived from the database). Lastly, you can
                          make your own 'GraphGroup' by using the original
                          sensor order and put them into brackets like
                          '[1,2][6][3,4,5]'.
    - 'ColorShades = False': This needs to be a boolean value. If you use
                             GraphGroups, you might as well want to use
                             ColorShades. Let's say you have 3 red graphs and
                             set this to True, then you will get 3 different
                             kinds of red instead of one to make the graphs more
                             distinctive and reconizable.
    - 'Normalization = off': When ploting quantities like currents or
                             resistances you might want to normalize them.
                             This can be done by inserting the normalization
                             factors (denominators) like
                             '[7.590296,7.590296,1.277161,1.277161]' in respect
                             of the original sensor order. In this case, every
                             y-value of graph 1 and 2 (original sensor order)
                             would be divided (normalized) by 7.590296.
    - 'Position = auto': If this is set to auto then the scripts will search all
                         4 corners for the best spot to place the legend. You
 .                         might wanna adjust this by using
                         'TR' (top right corner),
                         'TL',
                         'BR' (bottom right corner) or
                         'BL'.
    - 'BoxPara = 1': If you change the name of a legend element you might want
                     to adjust the legend box width by changing this factor in
                     between 0.5 and 1.5.
    - 'SortPara = list': Pronounces the parameter that determines the order of
                         all legend element.
    - 'EntryList = (0)a, (1)b, (3)c, (2)d': The legend elements are naturally
                                            ordered by ROOT. This original order
                                            (here: a = 0, b = 1, c = 2, d = 3)
                                            can be edited by changing the number
                                            in the brackets. However, other
                                            options will always refere to the
                                            original order.

"""

class KITPlot(object):

    __kitGreen = []
    __kitBlue = []
    __kitMay = []
    __kitYellow = []
    __kitOrange = []
    __kitBrown = []
    __kitRed = []
    __kitPurple = []
    __kitCyan = []

    __init = False
    __color = 0

    def __init__(self, dataInput=None, cfgFile=None):


        # init lists
        self.__files = []
        self.__graphs = []

        # init colors and markers
        if self.__init == False:
            self.__initColor()
            #self.__markerSet = [21,20,22,23,25,24,26,32,34]
            self.cfg_initialized = False
        else:
            pass

        # Load parameters and apply default style
        self.__cfg = ConfigHandler()
        self.__cfg.setDir("cfg/")
        self.cfgPath = self.__cfg.getCfgName(dataInput)

        # Load cfg file given in initial argument
        if cfgFile is not None:
            self.__cfg.load(cfgFile)
        # Empty KITPlot with existing default cfg
        elif dataInput is None and self.__cfgPresent():
            self.__cfg.load('default.cfg')
            print("Initialized default.cfg")
        # Empty KITPlot / create new default cfg
        elif dataInput is None and self.__cfgPresent() is not True:
            self.__initDefaultCfg()
            self.__cfg.write()
            print("Created new default.cfg")
        # Load existing cfg belonging to dataInput
        elif dataInput is not None and self.__cfgPresent(dataInput):
            self.__cfg.load(dataInput)
            print("Initialized cfg file: %s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(str(dataInput))))[0]))
        else:
            # new plot / create new cfg for dataInput
            self.cfg_initialized = True
            self.__initDefaultCfg()
            self.__cfg.write(dataInput)
            print("%s.cfg has been created" %dataInput)

        self.__initStyle()

#        a = self.__cfg['General','Measurement']
        a = "probe"
        # add files
        # TODO: 'probe' is hard-coded ??? wtf???
        if dataInput is not None:
            self.add(dataInput, a)
        else:
            pass

    #####################
    ### ConfigHandler ###
    #####################

    def __initDefaultCfg(self):

        pDict = OrderedDict()
        pDict = {'General' :{ 'Measurement'  : 'probe'      },
                 'Title'   :{ 'Title'        : 'Title',
                              'X0'           : 0.5,
                              'Y0'           : 0.97,
                              'H'            : 0.05,
                              'Font'         : 62           },
                 'XAxis'   :{ 'Title'        : 'X Value',
                              'Size'         : 0.05,
                              'Offset'       : 1.1,
                              'LabelSize'    : 0.04,
                              'Font'         : 62,
                              'Abs'          : True,
                              'Log'          : False,
                              'Range'        : 'auto',      },
                 'YAxis'   :{ 'Title'        : 'Y Value',
                              'Size'         : 0.05,
                              'Offset'       : 1.1,
                              'LabelSize'    : 0.04,
                              'Font'         : 62,
                              'Abs'          : True,
                              'Log'          : False,
                              'Range'        : 'auto'       },
                 'Legend'  :{ 'SortPara'     : 'list',
                              'Position'     : 'auto',
                              'TextSize'     : 0.03,
                              'BoxPara'      : 1,
                              'EntryList'    : ''           },
                 'Marker'  :{ 'Set'          : "[21,20,22,23,25,24,26,32,34]",
                              'Size'         : 1.5,         },
                 'Line'    :{ 'NoLine'       : False,
                              'Color'        : "[1400,1500,1700,1800,1100,1200,1300,1600]",
                              'Style'        : 1,
                              'Width'        : 2            },
                 'Canvas'  :{ 'SizeX'        : 1280,
                              'SizeY'        : 768,
                              'PadBMargin'   : 0.12,
                              'PadLMargin'   : 0.15,
                              'MaxDigits'    : 4            },
                 'Misc'    :{ 'GraphGroup'   : 'off',
                              'ColorShades'  : False,
                              'Normalization': 'off',       }
        }

        self.__cfg.init(pDict)

        return True


    def __cfgPresent(self, fileName='default'):

        file_path = os.getcwd() + "/cfg"
        if os.path.exists(file_path) == False:
            return False
        else:
            if os.listdir(file_path) == []:
                return False
            for cfg in os.listdir(file_path):
                if cfg == ("%s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(str(fileName))))[0])):
                    return True
            else:
                return False


    ##################
    ### Auto Title ###
    ##################

    def MeasurementType(self):
        """If KITPlot is initialized with probe IDs it is able to determine the
        measurement type by checking database information. The default axis
        labels and titles are then set according to this information as soon as
        the respective cfg file is created.
        """

        if self.__files[0].getParaY() == None:
            self.autotitle = "Title"
            self.autotitleY = "Y Value"
            self.autotitleX = "X Value"

        if self.__files[0].getParaY() != None:
            self.MT = self.__files[0].getParaY()
            if self.MT == "I_tot":
                self.autotitle = "Current Voltage Characteristics"
                self.autotitleY = "Current (A)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "Pinhole":
                self.autotitle = "Pinhole Leakage"
                self.autotitleY = "Current (A)"
                self.autotitleX = "Strip No"
            elif self.MT == "I_leak_dc":
                self.autotitle = "Strip Leakage Current"
                self.autotitleY = "Current (A)"
                self.autotitleX = "Strip No"
            elif self.MT == "C_tot":
                self.autotitle = "Capacitance Voltage Characteristics"
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "C_int":
                self.autotitle = "Interstrip Capacitance Measurement"
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Strip No"
            elif self.MT == "CC":
                self.autotitle = "Coupling Capacitance Measurement"
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Strip No"
            elif self.MT == "R_int":
                self.autotitle = "Interstrip Resistance Measurement"
                self.autotitleY = "Resistance (#Omega)"
                self.autotitleX = "Strip No"
            elif self.MT == "R_poly_dc":
                self.autotitle = "Strip Resistance Measurement"
                self.autotitleY = "Resistance (#Omega)"
                self.autotitleX = "Strip No"
            elif self.MT == "C_int_Ramp":
                self.autotitle = "Interstrip Capacitance Measurement"
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "R_int_Ramp":
                self.autotitle = "Strip Resistance Measurement"
                self.autotitleY = "Resistance (#Omega)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "I_leak_dc_Ramp":
                self.autotitle = "Interstrip Current Leakage"
                self.autotitleY = "Current (A)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "Rpunch":
                self.autotitle = "R_{Edge} of " + self.cfgPath.replace("cfg/","").replace(".cfg","").replace("for_","for ").replace("rev_","rev ").replace("m20C","(T = -20#circC)").replace("20C","(T = 20#circC)")[15:]
                self.autotitleY = "Current (A)"
                self.autotitleX = "Voltage (V)"
            else:
                self.autotitle = "Title"
                self.autotitleY = "Y Value"
                self.autotitleX = "X Value"

        if len(self.__files) >= 2 and self.__files[0].getParaY() != None:
            if self.__files[0].getParaY() != self.__files[1].getParaY():
                sys.exit("Measurement types are not equal!")

        return True

    def checkPID(self, dataInput):
        # checks if PIDs are listed in the file
        if os.path.isfile(dataInput):
            with open(dataInput) as inputFile:
                if len(inputFile.readline().split()) == 1:
                    return True
                else:
                    return False

    #####################
    ### Graph methods ###
    #####################


    def __initStyle(self):

        # Title options
        ROOT.gStyle.SetTitleX(self.__cfg.get('Title','X0'))
        ROOT.gStyle.SetTitleY(self.__cfg.get('Title','Y0'))
        ROOT.gStyle.SetTitleH(self.__cfg.get('Title','H'))
        ROOT.gStyle.SetTitleFont(self.__cfg.get('Title','Font'), "")

        # Axis Options
        ROOT.gStyle.SetTitleSize(self.__cfg.get('XAxis','Size'), "X")
        ROOT.gStyle.SetTitleSize(self.__cfg.get('YAxis','Size'), "Y")
        ROOT.gStyle.SetTitleOffset(self.__cfg.get('XAxis','Offset'), "X")
        ROOT.gStyle.SetTitleOffset(self.__cfg.get('YAxis','Offset'), "Y")
        ROOT.gStyle.SetTitleFont(self.__cfg.get('XAxis','Font'), "X")
        ROOT.gStyle.SetTitleFont(self.__cfg.get('YAxis','Font'), "Y")
        ROOT.gStyle.SetLabelFont(self.__cfg.get('XAxis','Font'),"X")
        ROOT.gStyle.SetLabelFont(self.__cfg.get('YAxis','Font'),"Y")
        ROOT.gStyle.SetLabelSize(self.__cfg.get('XAxis','Size'),"X")
        ROOT.gStyle.SetLabelSize(self.__cfg.get('YAxis','Size'),"Y")
        ROOT.TGaxis.SetMaxDigits(self.__cfg.get('Canvas','MaxDigits'))

        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(self.__cfg.get('Canvas','PadBMargin'))
        ROOT.gStyle.SetPadLeftMargin(self.__cfg.get('Canvas','PadLMargin'))

        # Marker Options
        ROOT.gStyle.SetMarkerSize(self.__cfg.get('Marker','Size'))
        # ROOT.gStyle.SetMarkerStyle(self.__cfg.get('Marker','Style'))
        # ROOT.gStyle.SetMarkerColor(self.__cfg.get('Marker','Color'))
        self.markerSet = self.__cfg['Marker','Set'].replace("[","").replace("]","").split(",")

        #Line options
        self.noLine = self.__cfg['Line','NoLine']
        self.colorSet = self.__cfg['Line','Color'].replace("[","").replace("]","").split(",")
        self.lineWidth = self.__cfg['Line','Width']
        self.lineStyle = self.__cfg['Line','Style']

        # Pad Options
        ROOT.gStyle.SetPadGridX(True)
        ROOT.gStyle.SetPadGridY(True)

        # KITPlot specific options
        self.ColorShades = self.__cfg['Misc','ColorShades']
        self.absX = self.__cfg['XAxis','Abs']
        self.absY = self.__cfg['YAxis','Abs']
        self.logX = self.__cfg['XAxis','Log']
        self.logY = self.__cfg['YAxis','Log']
        KITPlot.__init = True

        return True


    def add(self, dataInput=None, measurement="probe"):
        """ Depending on the type, the 'self.__files' list is filled with
        KITData objects. An integer represents a single probe ID. A string
        represents a .txt file or a folder path.

        Args:
            dataInput(None|int|str): Determines the way the 'self.__files'
                is filled.
            measurement(str): probe station and ALiBaVa measurements must be
                handled differently due to different database paramters
        """

        # Load KITData
        if isinstance(dataInput, KITData):
            self.__files.append(dataInput)
            self.addGraph(dataInput.getX(),dataInput.getY())

        # Load single PID
        elif isinstance(dataInput, int):
            self.__files.append(KITData(dataInput))
            if "Ramp" in self.__files[-1].getParaY():
                print("Ramp measurement")
                self.addGraph(self.__files[-1].getZ(), self.__files[-1].getY())
            else:
                self.addGraph(self.__files[-1].getX(), self.__files[-1].getY())

        elif isinstance(dataInput, str):
            # Load single PID
            if dataInput.isdigit():
                self.__files.append(KITData(dataInput))
                if "Ramp" in self.__files[-1].getParaY():
                    print("Ramp measurement")
                    self.addGraph(self.__files[-1].getZ(), self.__files[-1].getY())
                else:
                    self.addNorm()

            # Load multiple data files in a folder
            elif os.path.isdir(dataInput):
                for inputFile in os.listdir(dataInput):
                    if (os.path.splitext(inputFile)[1] == ".txt"):
                        self.__files.append(KITData(dataInput + inputFile))
                    else:
                        pass

                self.arrangeFileList()
                self.addNorm()

            # Load file
            elif os.path.isfile(dataInput):

                # multiple PIDs
                if self.checkPID(dataInput) == True:

                    with open(dataInput) as inputFile:
                        fileList = []
                        for line in inputFile:
                            entry = line.split()
                            if entry[0].isdigit():
                                fileList.append(KITData(entry[0],measurement))

                        if measurement is "probe":
                            self.__files = fileList
                        elif measurement == "alibava":
                            self.__files.append(KITData(fileList))

                    self.arrangeFileList()

                    for i,File in enumerate(self.__files):
                        if "Ramp" in File.getParaY():
                            self.addGraph(File.getZ(), File.getY())
                        elif File.getParaY() is "Signal":
                            self.addGraph(File.getX(), File.getY())
                        else:
                            self.addNorm(False, i)

                # Rpunch/REdge Ramp file
                elif "REdge" in dataInput:

                    data = KITData(dataInput).getRPunchDict()

                    x = []
                    y = []
                    labels = []

                    for i, bias in enumerate(data):
                        x, y = zip(*data[bias])
                        kdata = KITData()
                        kdata.setX(list(x))
                        kdata.setY(list(y))
                        kdata.setName(str(bias) + " V")
                        kdata.setPX("Voltage")
                        kdata.setPY("Rpunch")
                        self.__files.append(kdata)

                    self.addNorm()

                # singel file
                else:
                    self.__files.append(KITData(dataInput))
                    self.addNorm()


        if self.cfg_initialized == True:
            self.MeasurementType()
            self.setAutoTitles()
        else:
            pass

        self.readEntryList()

        return True


    def addNorm(self, loop=True, j=0):
        """ This method enables normalizations of data tables. It has the
        same function as 'addGraph' but with more options. If the user wants to
        take advantage of normalization options then the data from the KITData
        objects needs to be manipulated while creating the ROOT graphs.

        Args:
            loop(bool), j(integer): ???

        """

    # Sends normalized graph values to addGraph
        if loop == True:
            for i, File in enumerate(self.__files):
                # if data points have error bars
                if self.__files[i].includesErrors():
                     if self.__cfg.get('Misc','Normalization') == "off":
                         self.addGraph(self.__files[i].getX(),
                                       self.__files[i].getY(),
                                       self.__files[i].getdX(),
                                       self.__files[i].getdY())
                     elif self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
                         self.addGraph(self.__files[i].getX(),
                                       self.manipulate(self.__files[i].getY(),i),
                                       self.__files[i].getdX(),
                                       self.manipulate(self.__files[i].getdY(),i))
                     elif self.__cfg.get('Misc','Normalization') == "1/C^{2}":
                         self.addGraph(File.getX(),
                         self.manipulate(File.getY(),i),
                         File.getdX(),
                         self.manipulate(File.getdY(),i))
                     else:
                         raise ValueError("Invalid normalization input! Try "
                                          "'off', '1/C^{2}' or '[float,"
                                          "float,...]'!")
                # if data points have no error bars
                else:
                    if self.__cfg.get('Misc','Normalization') == "off":
                        self.addGraph(self.__files[i].getX(),
                                      self.__files[i].getY())
                    elif self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
                        self.addGraph(self.__files[i].getX(),
                                      self.manipulate(self.__files[i].getY(),i))
                    elif self.__cfg.get('Misc','Normalization') == "1/C^{2}":
                        self.addGraph(File.getX(),self.manipulate(File.getY(),i))
                    else:
                         raise ValueError("Invalid normalization input! Try "
                                          "'off', '1/C^{2}' or '[float,"
                                          "float,...]'!")
        else:
            if self.__cfg.get('Misc','Normalization') == "off":
                self.addGraph(self.__files[j].getX(),self.__files[j].getY())
            elif self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
                self.addGraph(self.__files[j].getX(),self.manipulate(self.__files[j].getY(),j))
            elif self.__cfg.get('Misc','Normalization') == "1/C^{2}":
                self.addGraph(self.__files[j].getX(),self.manipulate(self.__files[j].getY(),j))
            else:
                raise ValueError("Invalid normalization input! Try 'off', '1/C^{2}' or '[float,float,...]'!")

        return True



    def addGraph(self, *args):
        """ The KITData objects within the 'self.__files' list (containing
        the data tables) are now converted into ROOT objects. A ROOT object
        represents a single graph of the future plot. These ROOT objects are
        stored within the 'self.__graphs' list.

        Args: x, y or KITData

        """

        # args: x, y or KITData

        if isinstance(args[0], KITData):
            if KITData.getDic() == None:
                self.__files.append(args[0])

                if self.absX:
                    x = np.absolute(args[0].getX())
                else:
                    x = args[0].getX()

                if self.absY:
                    if str(args[1]) == "y":
                        y = np.absolute(args[0].getY())
                    elif str(args[1]) == "z":
                        y = np.absolute(args[0].getZ())
                else:
                    if args[1] == "y":
                        y = args[0].getY()
                    elif args[1] == "z":
                        y = args[0].getZ()
            # Rpunch
            else:
                sys.exit("Dictinary error")

        elif len(args) == 2 and not isinstance(args[0], KITData):

            if self.absX:
                x = np.absolute(args[0])
            else:
                x = args[0]

            if self.absY:
                y = np.absolute(args[1])
            else:
                y = args[1]

        elif len(args) == 4 and not isinstance(args[0], KITData):

            if self.absX:
                x = np.absolute(args[0])
            else:
                x = args[0]

            if self.absY:
                y = np.absolute(args[1])
            else:
                y = args[1]

            dx = args[2]
            dy = args[3]

        else:
            sys.exit("Cant add graph")

        if len(args) == 2:
            self.__graphs.append(ROOT.TGraph(len(x),np.asarray(x),np.asarray(y)))
        elif len(args) == 4:
            self.__graphs.append(ROOT.TGraphErrors(len(x),np.asarray(x),np.asarray(y),np.asarray(dx),np.asarray(dy)))

        return True


    def draw(self, arg=None):
        """ Finally, a canvas needs to be created and all the ROOT objects
        within 'self.__graphs' need to be drawn. Different plot styles are set
        in respect of the cfg file and as a last step the legend is created and
        drawn on the canvas.

        Args:
            arg(str): This is a ROOT specific argument (TGraph  Draw):
                'A' -> draw axis
                'L' -> draw lines
                'P' -> draw markers
                'C' -> draw smooth curve
                See ROOT documentation for more details.

        """

        if arg == None:
            arg = "APL"
        else:
            pass

        if self.__cfg.get('Line','NoLine') == True and "L" in arg:
            arg = arg.replace("L","")
        elif self.__cfg.get('Line','NoLine') == False and "L" not in arg:
            arg = arg + "L"
        else:
            pass

        if len(self.__graphs) == 0:
            print("No graphs to draw")
            return False

        # init canvas
        self.canvas = ROOT.TCanvas("c1","c1",
                                   int(self.__cfg.get('Canvas','SizeX')),
                                   int(self.__cfg.get('Canvas','SizeY')))
        self.canvas.cd()

        # apply plot styles
        self.plotStyles(self.__cfg.get('XAxis','Title'),
                        self.__cfg.get('YAxis','Title'),
                        self.__cfg.get('Title','Title'))

        # set log scale if
        if self.logX:
            self.canvas.SetLogx()
        if self.logY:
            self.canvas.SetLogy()

        # Draw plots
        for n,graph in enumerate(self.__graphs):
            if n==0:
                graph.Draw(arg)
            else:
                graph.Draw(arg.replace("A","") + "SAME")

        # Set legend (always at the very end!)

        LegH = LegHandler()
        LegH.setKITLegend(self.__cfg.get('Legend'),
                          self.__graphs,
                          self.__files,
                          self.__cfg.get('Canvas','SizeX'),
                          self.__cfg.get('Canvas','SizeY'),
                          self.Scale)
        self.leg = LegH.getLegend()
#        self.leg.SetHeader("n-in-p FZ, 240#mum")
        self.leg.Draw()
        self.canvas.Update()

        self.saveAs(self.cfgPath.replace("cfg/","").replace(".cfg",""))


        return True


    def saveAs(self, fileName):

        if not os.path.exists("output"):
            os.makedirs("output")
        self.canvas.SaveAs("output/%s.png" %(fileName))
        self.canvas.SaveAs("output/%s.pdf" %(fileName))


    def update(self):

        try:
            self.canvas.Update()
        except:
            pass


    def plotStyles(self, XTitle, YTitle, Title):

        self.__graphs[0].GetXaxis().SetTitle(XTitle)
        self.__graphs[0].GetYaxis().SetTitle(YTitle)
        self.__graphs[0].SetTitle(Title)
        #self.getLegendOrder()

        # set titles (take auto titles when creating the cfg and the cfg value from here after)
        self.setTitles()
        # set axis ranges
        self.setRanges()
        # set marker styles (std assigning and/or graph group assigning)
        self.setMarkerStyles()
        # assign colors
        self.setGraphColor()

        return True


#####################
### Fancy methods ###
#####################

    def arrangeFileList(self):
        """ The KITData files in 'self.__files' are somewhat arbitrarily
        ordered at first. This method pre-orders them in respect of their names.

        """
        TempList1 = []
        TempList2 = []
        IDList = []
        IndexList = []

        for temp in self.__files:
            TempList1.append(temp.getName())
            TempList2.append(temp.getName())

        # if same name appears more than once...
        for i, Name1 in enumerate(TempList1):
            if TempList1.count(Name1) > 1:
                Test = Name1 + "_" + "(" + str(i) + ")"
                TempList2[i] = Test
                TempList1[i] = Test
            else:
                pass

        TempList2.sort()

        for i,Name2 in enumerate(TempList2):
            if Name2 == TempList1[i]:
                IndexList.append(i)
            else:
                for j, Name in enumerate(TempList1):
                    if Name == Name2:
                        IndexList.append(j)

        TempList1[:] = []

        for index in IndexList:
            TempList1.append(self.__files[index])
        self.__files = TempList1


    def __autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]

        self.perc = 0.05
        ListX = [0]
        ListY = [0]

        if self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
            for i,inputFile in enumerate(self.__files):
                ListX += inputFile.getX()
                ListY += self.manipulate(inputFile.getY(),i)
        elif self.__cfg.get('Misc','Normalization') == "1/C^{2}":
            for i,inputFile in enumerate(self.__files):
                ListX += inputFile.getX()
                ListY += self.manipulate(inputFile.getY(),i)
        else:
            for i,inputFile in enumerate(self.__files):
                ListX += inputFile.getX()
                ListY += inputFile.getY()

        if self.absX:
            ListX = np.absolute(ListX)
        else:
            pass
        if self.absY:
            ListY = np.absolute(ListY)
        else:
            pass

        if self.absX:
            self.Scale.append(min(ListX)*(1.-self.perc))
            self.Scale.append(min(ListY)*(1.-self.perc))
            self.Scale.append(max(ListX)*(1.+self.perc))
            self.Scale.append(max(ListY)*(1.+self.perc))

        if not self.absX:
            self.Scale.append(min(ListX)*(1.+self.perc))
            self.Scale.append(min(ListY)*(1.-self.perc))
            self.Scale.append(max(ListX)*(1.+self.perc))
            self.Scale.append(max(ListY)*(1.+self.perc))

        #if (self.Scale[2]/self.Scale[3]) > 1e-4:
        #    self.logY = True

        return True


    def manipulate(self, ListY, index):

        FacList = []
        TempList = []

        if self.__cfg.get('Misc','Normalization') == "1/C^{2}":
            for val in ListY:
                    TempList.append(1/(val*val))
        else:
            for char in self.__cfg.get('Misc','Normalization').replace("[", "").replace("]", "").split(","):
                FacList.append(float(char))

            if len(self.__files) != len(FacList):
                sys.exit("Invalid normalization input! Number of factors differs from the number of graphs.")
            else:
                for val in ListY:
                    TempList.append(val/FacList[index])

        ListY = TempList

        return ListY


    def checkTitleLenght(self, Title):

        # adapt title size in case it's too long
        if len(Title) > 30 and float(self.__cfg.get('Title','Y0')) <= 0.97:
            ROOT.gStyle.SetTitleY(0.99)
            #self.__writeSpecifics(self.cfgPath, "Title", "y0", 0.99)
        else:
            pass

        return Title


    def setAutoTitles(self):
        """ Writes certain labels into the cfg.

        """

        self.__cfg['Legend','EntryList'] = self.getDefaultEntryList()
        self.__cfg['Title','Title'] = self.autotitle
        self.__cfg['XAxis','Title'] = self.autotitleX
        self.__cfg['YAxis','Title'] = self.autotitleY

        return True


    def readEntryList(self):
        """'EntryList' makes all graphs, their names and order accessible. This
        subsection is read every time KITPlot is executed. An empty value ("")
        can be used to reset the entry to its default value (the original order
        and names given by the file list).

        """

        # sets entry list to default
        if self.__cfg['Legend','EntryList'] == "":
            self.__cfg['Legend','EntryList'] = self.getDefaultEntryList()
            print("Entry list was set back to default!")
            self.__EntryList = self.getDefaultEntryList()

        #read out all the changes the user made
        else:
            self.__EntryList = self.getEntryList()

        return True


    def changeOrder(self, counter):

        for i, key in enumerate(self.__EntryList):
            if int(key) == counter:

                return i
            else:
                pass

        return 0


    def interpolate(self, x=None, y=None):

        v = []

        if x is not None and y is not None:
            for File in self.__files:
                m, b = np.polyfit(x, y, 1)
                v.append((m, b))

        else:
            x = []
            y = []

            for File in self.__files:
                x = File.getX()
                y = File.getY()
                name = File.getName()
                m, b = np.polyfit(x, y, 1)
                v.append((name, abs(m)))

        return v


#####################
### Legend method ###
#####################


    def setLegend(self):
        """ The whole legend handling is outsourced and done by the 'leghandler'
        module. As a result, all the legend options (stored inside the 'Legend'
        dictionary), the 'self.__graph' list (containing all graphs as ROOT
        objects) and the'self.__files' list (containing the respective KITData
        objects) have to be given as arguments when calling 'leghandler'
        methods.

        """

        LegH = LegHandler()

        LegH.fillKITLegend(self.__cfg.get('Legend'),
                           self.__graphs,
                           self.__files)

        LegH.setOptions(self.__cfg.get('Legend'))

        LegH.moveLegend(int(self.__cfg.get('Canvas','SizeX')),
                        int(self.__cfg.get('Canvas','SizeY')),
                        self.__cfg.get('Legend'),
                        self.__files,
                        self.Scale)

        return LegH.getLegend()



#######################
### Set/get methods ###
#######################


    def getEntryList(self):
        """ Loads names and order in respect to the 'EntryList' section in cfg
        in 'self.__files' list. Keys and values of the dictionary and the cfg
        are strings by default.

        """

        EntryList = self.__cfg['Legend','EntryList']

        List = []

        for key in EntryList:
            List.append(int(key))

        if len(EntryList) != len(self.__files):
            raise KeyError("Unexpected 'EntryList' value! Number of graphs and "
                           "entries does not match or a key is used more than"
                           "once. Adjust or reset 'EntryList'.")
        else:
            pass
        if min(List) != 0:
            raise KeyError("Unexpected 'EntryList' value! First element must "
                           "start with a '0'.")
        else:
            pass
        if len(EntryList)-1 != max(List):
            raise KeyError("Unexpected 'EntryList' value! Skipping numbers is "
                           "forbidden.")
        else:
            pass

        return EntryList



    def getDefaultEntryList(self):
        """ Loads default names and order in respect to the KITData objects
        in 'self.__files' list. Both keys and values of the dictionary must be
        strings.

        """

        EntryList = OrderedDict()

        # write legend entries in a dict
        for i, graph in enumerate(self.__files):
            EntryList[str(i)] = str(graph.getName())

        return EntryList


    def setRanges(self):

        # Scale is always filled ROOT oriantated (xmin, ymin, xmax, ymax)
        self.Scale = []
        self.__autoScaling()

        if self.__cfg.get('XAxis','Range') == "auto":
            self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[2])
        elif ":" in self.__cfg.get('XAxis','Range'):
            Temp = self.__cfg.get('XAxis','Range').split(":")
            self.Scale[0] = float(Temp[0].replace("[",""))
            self.Scale[2] = float(Temp[1].replace("]",""))
            if self.Scale[0] > self.Scale[2]:
                sys.exit("Invalid X-axis range! xmin > xmax?!")
            else:
                pass
            self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[2])
        else:
            sys.exit("Invalid X-axis range! Try 'auto' or '[float:float]'!")

        if self.__cfg.get('YAxis','Range') == "auto":
            self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[1],self.Scale[3])
        elif ":" in self.__cfg.get('YAxis','Range'):
            Temp = self.__cfg.get('YAxis','Range').split(":")
            self.Scale[1] = float(Temp[0].replace("[",""))
            self.Scale[3] = float(Temp[1].replace("]",""))
            if self.Scale[1] > self.Scale[3]:
                sys.exit("Invalid Y-axis range! ymin > ymax?!")
            else:
                pass
            self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[1],self.Scale[3])
        else:
            sys.exit("Invalid Y-axis range! Try 'auto' or '[float:float]'!")



    def setMarkerStyles(self):

        for i, graph in enumerate(self.__graphs):
            if "[" and "]" in self.__cfg.get('Misc','GraphGroup'):
                break
            elif self.__cfg.get('Misc','GraphGroup') == "off":
                self.__graphs[self.changeOrder(i)].SetMarkerStyle(self.getMarkerStyle(i))
            elif self.__cfg.get('Misc','GraphGroup') == "name":
                self.__graphs[self.changeOrder(i)].SetMarkerStyle(self.getMarkerShade(i))


            else:
                sys.exit("Invalid group parameter! Try 'off', 'name' or define user groups with '[...],[...],...'!")

        # User Groups
        if "[" in self.__cfg.get('Misc','GraphGroup') and "]" in self.__cfg.get('Misc','GraphGroup'):
            self.getGroupList()

            j = 0

            if len(self.__GroupList)-self.__GroupList.count(666) != len(self.__graphs):
                raise ValueError("Insufficient UserGroup. Numbers do not match!")
            else:
                pass
            for elem in self.__GroupList:
                if elem == 666:
                    j = 0
                else:
                    self.__graphs[elem].SetMarkerStyle(self.getMarkerStyle(j))
                    j += 1
        else:
            pass



    def setGraphColor(self):

        for i, graph in enumerate(self.__graphs):
            if self.__cfg.get('Misc','GraphGroup') == "off" :
                self.__graphs[self.changeOrder(i)].SetMarkerColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineWidth(self.lineWidth)
#                self.__graphs[self.changeOrder(i)].Set(7)
            elif self.__cfg.get('Misc','GraphGroup') == "name" and self.ColorShades == False:
                self.__graphs[self.changeOrder(i)].SetMarkerColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineWidth(self.lineWidth)
            elif self.__cfg.get('Misc','GraphGroup') == "name" and self.ColorShades == True:
                 self.__graphs[self.changeOrder(i)].SetMarkerColor(self.getColorShades(i))
                 self.__graphs[self.changeOrder(i)].SetLineColor(self.getColorShades(i))
                 self.__graphs[self.changeOrder(i)].SetLineWidth(self.lineWidth)
            elif self.__cfg.get('Misc','GraphGroup')[0] == "[" and self.__cfg.get('Misc','GraphGroup')[-1] == "]" and self.ColorShades == True:
                break
            elif self.__cfg.get('Misc','GraphGroup') == "off" and self.ColorShades == True:
                raise ValueError("Need GraphGroups for applying shades!")

        # User Groups
        if "[" in self.__cfg.get('Misc','GraphGroup') and "]" in self.__cfg.get('Misc','GraphGroup'):

            self.getGroupList()
            colorcount = 0
            shadecount = 0

            if len(self.__GroupList)-self.__GroupList.count(666) != len(self.__graphs):
                raise ValueError("Insufficient UserGroup. Numbers do not match!")
            else:
                pass
            for elem in self.__GroupList:
                if elem == 666:
                    colorcount += 1
                    shadecount = 0
                elif self.ColorShades == True:
                        self.__graphs[elem].SetMarkerColor(int(self.colorSet[colorcount])+shadecount)
                        self.__graphs[elem].SetLineColor(int(self.colorSet[colorcount])+shadecount)
                        self.__graphs[elem].SetLineWidth(self.lineWidth)
                        self.__graphs[elem].SetLineStyle(self.lineStyle)
                        shadecount += 1
                elif self.ColorShades == False:
                        self.__graphs[elem].SetMarkerColor(int(self.colorSet[colorcount]))
                        self.__graphs[elem].SetLineColor((self.colorSet[colorcount]))
                        self.__graphs[elem].SetLineWidth(self.lineWidth)
                        self.__graphs[elem].SetLineStyle(self.lineStyle)
                else:
                    pass
        else:
            pass


    def setTitles(self):

        self.__graphs[0].GetXaxis().SetTitle(self.__cfg.get('XAxis','Title'))
        self.__graphs[0].GetYaxis().SetTitle(self.__cfg.get('YAxis','Title'))
        self.__graphs[0].SetTitle(self.checkTitleLenght(self.__cfg.get('Title','Title')))


    def setAxisTitleSize(self, size):

        ROOT.gStyle.SetTitleSize(size,"X")
        ROOT.gStyle.SetTitleSize(size,"Y")

        return True

    def setAxisTitleOffset(self, offset):

        ROOT.gStyle.SetTitleOffset(offset,"X")
        ROOT.gStyle.SetTitleOffset(offset,"Y")

        return True


    def getMarkerStyle(self, index):

        if index >= 9:
            return int(self.markerSet[index % 8])
        else:
            return int(self.markerSet[index])


    def getMarkerShade(self, index):

        self.getShadeList()
        MarkerShade = []
        color_num = self.ShadeList[0]

        for i, shade in enumerate(self.ShadeList):
            if not self.ShadeList[i]-color_num > 9:
                MarkerShade.append(self.ShadeList[i]-color_num)
            if self.ShadeList[i]-color_num > 9:
                color_num += 100
                MarkerShade.append(self.ShadeList[i]-color_num)

        return int(self.markerSet[MarkerShade[index]])


    def getGroupList(self):

        self.__GroupList = []
        TempList = []
        UserList = []
        for i, Element in enumerate(self.__files):
            if self.__cfg.get('Misc','GraphGroup') == "name":
                TempList.append(self.__files[i].getName()[:5])
            elif self.__cfg.get('Misc','GraphGroup') == "fluence":
                TempList.append(self.__files[i].getFluenceP())
            else:
                pass

        if (self.__cfg.get('Misc','GraphGroup')[0] == "[" and
           self.__cfg.get('Misc','GraphGroup')[-1] == "]"):
           for char in self.__cfg.get('Misc','GraphGroup'):
                if char.isdigit() == True:
                    self.__GroupList.append(int(char))
                elif char == "[" or char == ",":
                    pass
                else:
                    self.__GroupList.append(666)

        for i, TempElement in enumerate(TempList):
            if TempElement not in self.__GroupList:
                  self.__GroupList.append(TempList[i])

        return self.__GroupList


#####################
### Color methods ###
#####################

    def __initColor(self):

        self.__kitGreen.append(ROOT.TColor(1100, 0./255, 169./255, 144./255))
        self.__kitGreen.append(ROOT.TColor(1101,75./255, 195./255, 165./255))
        self.__kitGreen.append(ROOT.TColor(1102,125./255, 210./255, 185./255))
        self.__kitGreen.append(ROOT.TColor(1103,180./255, 230./255, 210./255))
        self.__kitGreen.append(ROOT.TColor(1104,215./255, 240./255, 230./255))

        self.__kitRed.append(ROOT.TColor(1200, 191./255, 35./255, 41./255))
        self.__kitRed.append(ROOT.TColor(1201, 205./255, 85./255, 75./255))
        self.__kitRed.append(ROOT.TColor(1202, 220./255, 130./255, 110./255))
        self.__kitRed.append(ROOT.TColor(1203, 230./255, 175./255, 160./255))
        self.__kitRed.append(ROOT.TColor(1204, 245./255, 215./255, 200./255))

        self.__kitOrange.append(ROOT.TColor(1300, 247./255, 145./255, 16./255))
        self.__kitOrange.append(ROOT.TColor(1301, 249./255, 174./255, 73./255))
        self.__kitOrange.append(ROOT.TColor(1302, 251./255, 195./255, 118./255))
        self.__kitOrange.append(ROOT.TColor(1303, 252./255, 218./255, 168./255))
        self.__kitOrange.append(ROOT.TColor(1304, 254./255, 236./255, 211./255))

        self.__kitBlue.append(ROOT.TColor(1400, 67./255, 115./255, 194./255))
        self.__kitBlue.append(ROOT.TColor(1401, 120./255, 145./255, 210./255))
        self.__kitBlue.append(ROOT.TColor(1402, 155./255, 170./255, 220./255))
        self.__kitBlue.append(ROOT.TColor(1403, 195./255, 200./255, 235./255))
        self.__kitBlue.append(ROOT.TColor(1404, 225./255, 225./255, 245./255))

        self.__kitPurple.append(ROOT.TColor(1500, 188./255, 12./255, 141./255))
        self.__kitPurple.append(ROOT.TColor(1501, 205./255, 78./255, 174./255))
        self.__kitPurple.append(ROOT.TColor(1502, 218./255, 125./255, 197./255))
        self.__kitPurple.append(ROOT.TColor(1503, 232./255, 175./255, 220./255))
        self.__kitPurple.append(ROOT.TColor(1504, 243./255, 215./255, 237./255))

        self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))
        self.__kitBrown.append(ROOT.TColor(1601, 193./255, 157./255, 82./255))
        self.__kitBrown.append(ROOT.TColor(1602, 208./255, 181./255, 122./255))
        self.__kitBrown.append(ROOT.TColor(1603, 226./255, 208./255, 169./255))
        self.__kitBrown.append(ROOT.TColor(1604, 241./255, 231./255, 210./255))

        self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))
        self.__kitMay.append(ROOT.TColor(1701, 148./255, 213./255, 98./255))
        self.__kitMay.append(ROOT.TColor(1702, 178./255, 225./255, 137./255))
        self.__kitMay.append(ROOT.TColor(1703, 209./255, 237./255, 180./255))
        self.__kitMay.append(ROOT.TColor(1704, 232./255, 246./255, 217./255))

        self.__kitCyan.append(ROOT.TColor(1800, 28./255, 174./255, 236./255))
        self.__kitCyan.append(ROOT.TColor(1801, 95./255, 197./255, 241./255))
        self.__kitCyan.append(ROOT.TColor(1802, 140./255, 213./255, 245./255))
        self.__kitCyan.append(ROOT.TColor(1803, 186./255, 229./255, 249./255))
        self.__kitCyan.append(ROOT.TColor(1804, 221./255, 242./255, 252./255))

        # yellow removed because it looks shitty

        KITPlot.__init = True

        return True


    def getColor(self, index):

        KITPlot.__color = index + 1
        KITPlot.__color %= 8

        return int(self.colorSet[KITPlot.__color-1])


    def getShadeList(self):

        self.ShadeList = []
        shade_counter = 0
        j = 0

        for File in self.__files:
            if File.getName()[:5] == self.getGroupList()[j]:
                self.ShadeList.append(int(self.colorSet[j])+shade_counter)
                shade_counter += 1
            if File.getName()[:5] != self.getGroupList()[j]:
                shade_counter = 0
                if j <= len(self.getGroupList())-1:
                    j += 1
                self.ShadeList.append(int(self.colorSet[j])+shade_counter)
                shade_counter += 1

        return True

    def getColorShades(self, index):
        self.getShadeList()
        return self.ShadeList[index]


###################
### Get methods ###
###################

    def getGraph(self, graph=None):

        if len(self.__graphs) == 1:
            return self.__graphs[0]
        elif (len(self.__graphs) != 1) and (graph is None):
            return self._graphs
        else:
            if isinstance(graph,str):
                if (len(self.__graphs) != 1) and (graph.isdigit()):
                    return self.__graphs[int(graph)]
                else:
                    return False
            elif isinstance(graph,int):
                if (len(self.__graphs) != 1):
                    return self.__graphs[graph]
                else:
                    return False

    def getFile(self, KITFile=None):

        if len(self.__files) == 1:
            return self.__files[0]
        elif (len(self.__files) != 1) and (KITFile is None):
            return self._file
        else:
            if isinstance(KITFile,str):
                if (len(self.__files) != 1) and (KITFile.isdigit()):
                    return self.__files[int(KITFile)]
                else:
                    return False
            elif isinstance(KITFile,int):
                if (len(self.__files) != 1):
                    return self.__files[KITFile]
                else:
                    return False


    def getCanvas(self):
        return self.canvas

    def getX(self):
        X = []
        for List in self.__files:
            X.append(List.getX())
        return X

    def getY(self):
        Y = []
        for List in self.__files:
            Y.append(List.getY())
        return Y

if __name__ == '__main__':
    plot = KITPlot(38268)
    plot.draw('APL')
