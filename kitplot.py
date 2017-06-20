#!/usr/bin/env python3

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
    c) Download and install python 3 on your system
       (https://www.python.org/downloads/).
    d) The most recent version of python 3 contains 'pip3', a download
       manager/installer for python modules, which should be used to download
       the following modules:
       - numpy: 'pip3 install numpy'
       - pymysql: 'pip3 install mysqlclient'
       - json: 'pip3 install simplejson'
       (the rest should be standard python modules... there's nothing fancy
        here.').
    e) There are 2 'plot engines' you can use: ROOT or matplotlib.
       - ROOT: Download and build ROOT v5.34/36 or 6 on your system. When
               building ROOT, make sure you enable the use of pyROOT. This is
               easy on Linux. However,doing this on Windows or Mac is a
               different story... although it's generally possible to do this
               on every system.
       - matplotlib: 'pip3 install matplotlib'
    f) Lastly, you need login informations to access the database, which are
       stored in the 'db.cfg'. For security reasons the login file can not be
       downloaded, but must be requested from Daniel or Marius.

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
    from .kitdata import KITData
    from .kitplot import KITPlot

    if len(sys.argv) > 2:
        kPlot1 = KITPlot(sys.argv[1],sys.argv[2])
    else:
        kPlot1 = KITPlot(sys.argv[1])


    kPlot1.draw("APL")

    input()

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
    - 'Log = false': This needs to be a boolean value. Remember that having a 0
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
    - 'ColorShades = false': This needs to be a boolean value. If you use
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
                          might wanna adjust this by using
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

    - 'Line' -> 'Style' = '[1,7]': This feature enables drawing different lines
                                   in different styles. In this example, the
                                   first line is continuous while the second
                                   line is dashed. You can also just write
                                   something like 'Style' = 1 (integer) to draw
                                   all lines in the same style.

    - 'Line' -> 'NoLine' = false: If you want happy with just drawing markers
                                  and no lines then set this option to 'false'.

    - 'Marker' -> 'Set' = "[21,20,...]": KITPlot will iterate through this list
                                         when drawing graphs to determine
                                         the marker style. This list is just a
                                         suggestion. Feel free to edit the
                                         number of marker styles in this list.
                                         See ROOT documention for the respective
                                         marker styles.

    - 'Line' -> 'Color' = "[1100,1200,...]": KITPlot will iterate through this
                                             list when drawing graphs to
                                             determine the line color. KITPlot
                                             uses its own color palette, but can
                                             also use the ROOT palette, although
                                             some options might not work then.
                                             The 'self.__initColor' function
                                             incorporates our self-made color
                                             palette.

"""

import numpy as np
import os, sys
from .kitdata import KITData
from .KITConfig import KITConfig
from .KITLegend import KITLegend
from .kitmatplotlib import KITMatplotlib
from collections import OrderedDict
from matplotlib.patches import Rectangle
from .kitutils import Lodger

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

        # supported plot engines
        self.__engines = ['matplotlib', 'ROOT']

        # init lists
        self.__files = []
        self.__graphs = []

        # init colors
        if self.__init == False:
            self.cfg_initialized = False
        else:
            pass

        # Load parameters and apply default style
        self.__cfg = KITConfig()
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


#        a = self.__cfg['General','Measurement']
        a = "probe"
        # add files
        # TODO: 'probe' is hard-coded ??? wtf???
        if dataInput is not None:
            self.addFiles(dataInput, a)
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
                            #   'H'            : 0.05,
                              'FontSize'     : 14,
                              'FontStyle'    : 'bold',
                              'Font'         : 62,          },
                 'XAxis'   :{ 'Title'        : 'X Value',
                            #   'Size'         : 0.05,
                            #   'Offset'       : 1.1,
                            #   'LabelSize'    : 0.04,
                              'FontSize'     : 12,
                              'FontStyle'    : 'bold',
                              'Font'         : 62,
                              'Abs'          : True,
                              'Log'          : False,
                              'Range'        : 'auto',      },
                 'YAxis'   :{ 'Title'        : 'Y Value',
                            #   'Size'         : 0.05,
                            #   'Offset'       : 1.1,
                            #   'LabelSize'    : 0.04,
                              'FontSize'     : 12,
                              'FontStyle'    : 'bold',
                              'Font'         : 62,
                              'Abs'          : True,
                              'Log'          : False,
                              'Range'        : 'auto'       },
                #  'Legend'  :{ 'SortPara'     : 'list',
                 'Legend'  :{ 'SortPara'     : 'list',
                              'Position'     : 'auto',
                              'TextSize'     : 0.03,
                              'BoxPara'      : 1,
                              'EntryList'    : ''           },
                #  'Marker'  :{ 'Set'          : "[21,20,22,23,25,24,26,32,34]",
                 'Marker'  :{ 'Set'          : "[1,2,3,4,5,6,7]",
                            #   'Size'         : 1.5,         },
                              'Size'         : 6,         },
                #  'Line'    :{ 'Color'        : "[1400,1500,1700,1800,1100,1200,1300,1600]",
                 'Line'    :{ 'ColorPalette' : "KIT",
                              'Color'        : "[0,1,2,3,4,5,6,7]",
                              'Style'        : 1,
                              'Width'        : 2            },
                 'Canvas'  :{ 'CanvasSize'   : "[16.26,12.19]",
                              'PadSize'      : "[0.1,0.11,0.86,0.80]"},
                 'Misc'    :{ 'GraphGroup'   : 'off',
                            #   'ColorShades'  : False,
                              'Normalization': 'off',
                              "SplitGraph": "False"       }
        }

        self.__cfg.init(pDict)

        return True


    def __cfgPresent(self, fileName='default'):

        file_path = os.path.join(os.getcwd(), "cfg")
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
        """ If KITPlot is initialized with probe IDs it is able to determine the
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
            elif self.MT == "V_Ramp":
                self.autotitle = "R_{Edge} Measurement"
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




    def addFiles(self, dataInput=None, measurement="probe"):
        """ Depending on the type, the 'self.__files' list is filled with
        KITData objects. An integer represents a single probe ID. A string
        represents a .txt file or a folder path.
        A RPunch measurement, however, origionaly consist of one KITData file
        that needs to be split up into several KITData objects for one bias
        value (x value) represents one graph.

        Args:
            dataInput(None|int|str): Determines the way the 'self.__files'
                is filled.
            measurement(str): probe station and ALiBaVa measurements must be
                handled differently due to different database paramters
        """

        #TODO: handle multiple KITPlot objects to create canvas with multiple subplots
        # if isinstance(dataInput, KITPlot):


        # Load KITData
        if isinstance(dataInput, KITData):
            self.__files.append(dataInput)
            # self.addGraph(dataInput.getX(),dataInput.getY())

        # Load single PID
        # ???
        elif isinstance(dataInput, int):
            self.__files.append(KITData(dataInput))
            # if "Ramp" in self.__files[-1].getParaY():
            #     print("Ramp measurement")
            #     self.addGraph(self.__files[-1].getZ(), self.__files[-1].getY())
            # else:
            #     self.addGraph(self.__files[-1].getX(), self.__files[-1].getY())

        elif isinstance(dataInput, str):
            # Load single PID
            if dataInput.isdigit():
                self.__files.append(KITData(dataInput))
                if "Ramp" in self.__files[-1].getParaY():

                    x = []
                    y = []
                    labels = []

                    if len(self.__files) > 1:
                        raise ValueError("You can only print one RPunch ramp"
                                         " at once!")

                    # get the values from the KITData file and convert it into
                    # a dictionary: section=V_bias,key=(V_edge, I_edge) [tuple]
                    kdict = self.getRDict(self.__files[0])
                    self.__files = []
                    for i, bias in enumerate(kdict):
                        # create an empty KITData object
                        kdata = KITData()
                        # extract each single bias value from the dictionary
                        # and create KITData files for every value
                        x, y = zip(*kdict[bias])
                        kdata.setX(list(x))
                        kdata.setY(list(y))
                        kdata.setName(str(bias) + " V")
                        kdata.setPX("Voltage")
                        kdata.setPY("Rpunch")

                        self.__files.append(kdata)


                else:
                    pass


            # Load multiple data files in a folder
            elif os.path.isdir(dataInput):
                for inputFile in os.listdir(dataInput):
                    if (os.path.splitext(inputFile)[1] == ".txt"):
                        self.__files.append(KITData(dataInput + inputFile))
                    else:
                        pass

                # self.arrangeFileList()
                # self.addNorm()

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

                    # self.arrangeFileList()

                    # for i,File in enumerate(self.__files):
                    #     if "Ramp" in File.getParaY():
                    #         self.addGraph(File.getZ(), File.getY())
                    #     elif File.getParaY() is "Signal":
                    #         self.addGraph(File.getX(), File.getY())
                    #     else:
                    #         self.addNorm(False, i)



                # TODO Rpunch/REdge Ramp file
                # elif "REdge" in dataInput:
                #
                #     data = KITData(dataInput).getRPunchDict()
                #
                #     x = []
                #     y = []
                #     labels = []
                #
                #     for i, bias in enumerate(data):
                #         x, y = zip(*data[bias])
                #         kdata = KITData()
                #         kdata.setX(list(x))
                #         kdata.setY(list(y))
                #         kdata.setName(str(bias) + " V")
                #         kdata.setPX("Voltage")
                #         kdata.setPY("Rpunch")
                #         self.__files.append(kdata)
                #
                #     self.addNorm()
                #

                # singel file
                else:
                    print("single file")
                    self.__files.append(KITData(dataInput))


        if self.cfg_initialized == True:
            self.MeasurementType()
            self.setAutoTitles()
        else:
            pass

        self.readEntryList()

        return True


    def draw(self, engine=None, arg=None):
        """
        doc

        """

        # set engine
        if engine == None:
            engine = self.__engines[0]
        if engine not in self.__engines:
            raise ValueError("Unkown plot engine. Supported engines are: \n"
                             + self.__engines[0] + " and " + self.__engines[1])

        # create graphs and canvas
        if engine == self.__engines[0]:
            self.canvas = KITMatplotlib(self.__cfg).draw(self.__files)

            png_out = os.path.join("output", self.cfgPath.replace("cfg/","").replace(".cfg",".png"))
            pdf_out = os.path.join("output", self.cfgPath.replace("cfg/","").replace(".cfg",".pdf"))


            # self.canvas.add_subplot(1, 1, 1).plot(t,f,color='c',linewidth=3)
            # self.canvas.add_subplot(1, 1, 1).plot([0,400],[0,12000],color='c',linewidth=3)
            # self.canvas.add_subplot(1, 1, 1).axvline(y=12000)
            # self.canvas.add_subplot(1, 1, 1).axhline(y=1.5,color='c',linewidth=3)
            # handles, labels = self.canvas.add_subplot(1, 1, 1).get_legend_handles_labels()
            # handles.append(Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0))
            # labels.append("test")
            # self.canvas.add_subplot(1, 1, 1).legend(handles,labels)


            self.canvas.savefig(png_out)
            self.canvas.savefig(pdf_out)
        else:
            pass

        return True



#####################
### Fancy methods ###
#####################


    def addLodger(self, x=None, y=None, name=None):

        if x == None and y == None:
            print("Lodger arrived with an empty suitcase. Goodbye")
        elif y == None and isinstance(x, (int, float)):
            print("Draw vertical line at x = "+ str(x))
            self.__files.append(Lodger(hline=x,name="test"))
            self.draw()
        elif x == None and isinstance(x, (int, float)):
            print("Draw horizontal line at x = "+ str(y))
        elif isinstance(y, list) and isinstance(x, list):
            print("Draw graph.")
            self.__files.append(Lodger(x=x,y=y,name="test"))
            self.draw()
        return True


    def showCanvas(self):
        self.canvas.show()
        return True

    def arrangeFileList(self):
        """ The KITData files in .__files are somewhat arbitrarily
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


        def readEntryList(self):
            """'EntryList' makes the names and order of all graphs accessible. This
            subsection is read every time KITPlot is executed. An empty value ("")
            can be used to reset the entry to its default value (the original order
            and names given by the .__files).
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

    def makeFit(self, List, print_fit, draw_fit):

        x = []
        y = []

        print("Fit Results:")

        if isinstance(List, KITData):
            x = List.getX()
            y = List.getY()

            p0, p1 = abs(np.polyfit(x ,y, 1))


            print("{:>8} {:>8} {:>8}".format(List.getName(),
                                             " : m = " + str(round(p0,5)),
                                             " ; R = " + str(round(1./p0,5))))

        else:
            #TODO non-kitdata objects
            pass



#######################
### Set/get methods ###
#######################


    def getRDict(self, kdata):

        dic = OrderedDict()
        bias = kdata.getX()[0]
        ix = []
        iy = []

        # Rpunch Ramps: x = V_bias, y = V_edge, z = I_edge
        for (valX, valY, valZ) in zip(kdata.getX(), kdata.getY(), kdata.getZ()):
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

        self.__RDict = dic

        return self.__RDict

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

    def readEntryList(self):
        """'EntryList' makes the names and order of all graphs accessible. This
        subsection is read every time KITPlot is executed. An empty value ("")
        can be used to reset the entry to its default value (the original order
        and names given by the .__files).
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
