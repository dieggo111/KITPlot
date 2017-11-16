#!/usr/bin/env python3

""" A simple ROOT based python plot script

1) Synopsis:
Hello World! Welcome to the KITPlot script. This script was created by
Daniel Schell (daniel.schell@kit.edu) and Marius Metzler
(marius.metzler@kit.edu). This script is about creating distinctive,
well-arranged plots especially for bachelor/master students at ETP, who find
common, commercially availible plotting software as lame and unconvinient
as we do. The greatest benifit of KITPlot is that it is able to directly
communicate with the ETP database. It also automatizes standard operations and
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
       KITData objects. It then calls a drawing function while using parameters
       from a .cfg file. Eventually, the output contains:
        - 2 plot graphics (.png and .pdf file) that will be automatically
          stored in your output folder (will be created in your main
          folder if necessary)
        - and a .cfg file that will be automatically stored in your cfg folder
          (will be created in your main folder if necessary)

    c) ##### obsolete for matplotlib #####
       The LegHandler module handles the arrangement, position and style of the
       legend box and its elements. It also uses a very rudimentary algorithm
       to search for the most convinient spot inside the canvas
       (one of the 4 corners), so that the legend doesn't cover any data points.

    d) The ConfigHandler module writes/reads/edits a plot-specific .cfg file.
       Since KITPlot is console-based and has no graphical interface, the
       config file solution makes up for it.

    e) kitmatpoltlib handles all the drawing.

3) Installation:
    a) Create a main folder and give it a nice name (f.e. 'KITPlot')
    b) Inside this folder you ought to create a folder for cfg files named
       "cfg" and for output files named "output" .Clone the KITPlot
       repository from 'https://github.com/dieggo111/KITPlot',
       put its content inside an extra folder within your main folder and name
       it 'KITPlot'.
    c) Download and install python 3 on your system
       (https://www.python.org/downloads/).
    d) The most recent version of python 3 contains 'pip3', a download
       manager/installer for python modules, which should be used to download
       the following modules:
       - numpy: 'pip3 install numpy'
       - json: 'pip3 install simplejson'
       - pymysql: Download download and unzip source file from
                  https://pypi.python.org/pypi/mysql-connector-python/2.0.4 or
                  use the one in the
                  repository. Open consol/terminal and go to PyMySQL-0.7.11
                  folder. Type "python setup.py build" and then
                  "python setup.py install".
    e) There are 2 'plot engines' you can use: ROOT or matplotlib.
       - matplotlib: 'pip3 install matplotlib'
       - ###### ROOT: ###### no longger supported ######
               Download and build ROOT v5.34/36 or 6 on your system. When
               building ROOT, make sure you enable the use of pyROOT. This is
               easy on Linux. However,doing this on Windows or Mac is a
               different story... although it's generally possible to do this
               on every system.
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
from KITPlot import KITPlot

if len(sys.argv) > 2:
    kPlot1 = KITPlot(sys.argv[1],sys.argv[2])
else:
    kPlot1 = KITPlot(sys.argv[1])


kPlot1.draw("matplotlib")


kPlot1.saveCanvas()
kPlot1.showCanvas()
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
from .kitmatplotlib import KITMatplotlib
from collections import OrderedDict
from matplotlib.patches import Rectangle
from .kitlodger import KITLodger
from . import kitutils

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
        self.iter = iter(["lodger1","lodger2","lodger3"])
        # supported plot engines
        self.__engines = ['matplotlib', 'ROOT']

        # init lists
        self.__files = []
        self.__graphs = []

        # Load parameters and apply default style
        self.__cfg = KITConfig()
        self.__cfg.Default("default.cfg")
        self.__cfg.Dir("cfg")

        # extract name from data input
        self.__inputName = self.getDataName(dataInput)

        # check if cfg is already there
        if os.path.isfile(os.path.join("cfg", self.__inputName) + ".cfg") == False:
            self.is_cfg_new = True
        else:
            self.is_cfg_new = False

        # load dict with parameters from cfg file
        self.__cfg.load(self.__inputName)

#        a = self.__cfg['General','Measurement']
        a = "probe"
        # add files
        # TODO: 'probe' is hard-coded ??? wtf???
        if dataInput is not None:
            self.addFiles(dataInput, a)
        else:
            pass


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
            print("Input interpreted as KITData object")
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
                    print("Input interpreted as ramp measurement")
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
                print("Input interpreted as folder with files")
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
                    print("Input interpreted as multiple PIDs")
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
                    print("Input interpreted as single file")
                    self.__files.append(KITData(dataInput))

        return True


    def draw(self, engine=None, add_lodger=False):
        """
        doc

        """

        # if dataInput comes from database then apply titles according to measurement type
        if self.is_cfg_new == True:
            self.MeasurementType()

        # read and adjsut .__entryDict before drawing
        if add_lodger == True:
            self.readEntryDict(add_lodger=True)
        else:
            self.readEntryDict()

        # get lodgers from cfg wenn KITPlot object is initialized
        if add_lodger == False:
            try:
                self.getLodgers()
            except:
                print("No lodgers in cfg.")

        # set engine
        if engine == None:
            engine = self.__engines[0]
        if engine not in self.__engines:
            raise ValueError("Unkown plot engine. Supported engines are: \n"
                             + self.__engines[0] + " and " + self.__engines[1])

        # create graphs and canvas
        if engine == self.__engines[0]:
            self.canvas = KITMatplotlib(self.__cfg).draw(self.__files)
            if add_lodger == True:
                self.addLodgerEntry()

        return True


######################
### Lodger methods ###
######################

    def getLodgers(self):
        """ Read the cfg and create a lodger object for every entry in
            'Lodgers'.
        """
        print("getLodger")

        cfgLodgers = []
        for lodger in self.__cfg['Lodgers']:
            paraDict = dict(self.__cfg['Lodgers'][lodger])
            # for paraDict in dict(self.__cfg['Lodgers'][lodger]):
            x = paraDict.get('x', None)
            y = paraDict.get('y', None)
            name = paraDict.get('name', None)
            color = paraDict.get('color', None)
            width = paraDict.get('width', None)
            style = paraDict.get('style', None)

            self.__files.append(KITLodger(x=x,y=y,name=name,color=color,
                                          style=style,width=width))
        return True

    def addLodger(self,x=None,y=None,name=None,color=None,style=None,width=None):
        print("addLodger")
        # add new lodger from main
        newLodger = KITLodger(x=x,y=y,name=name,color=color,style=style,
                              width=width)
        self.__files.append(newLodger)
        self.addLodgerEntry(newLodger)
        self.draw(add_lodger=True)
        return True

    def addLodgerEntry(self, newLodger):
        print("addLodgerEntry")
        key = next(self.iter)
        paraDict = newLodger.getDict()
        try:
            self.__cfg["Lodgers"].update({key : paraDict})
            self.__cfg["Legend"]["EntryList"].update({})
        except:
            self.__cfg["Lodgers"] = {key : paraDict}

        return True


#########################
### entryDict methods ###
#########################


    def readEntryDict(self, add_lodger=False):
        """'EntryList' makes the names and order of all graphs accessible. This
        subsection is read every time KITPlot is executed. An empty value ("")
        can be used to reset the entry to its default value (the original order
        and names given by the .__files).
        """

        # writes entry dict to cfg of sets it back to default if value is ""
        if self.__cfg['Legend','EntryList'] == "":
            self.__cfg['Legend','EntryList'] = self.getDefaultEntryDict()
            if self.is_cfg_new == False:
                print("EntryDict was set back to default!")
            self.__entryDict = self.getDefaultEntryDict()
        else:
            self.__entryDict = self.__cfg['Legend','EntryList']



        # calculate expected number of entries in 'EntryList'
        # new lodgers are already appended
        exp_len = len(self.__files)

        # check if there's a 'Lodgers' section and how many entries it has
        # try:
        #     # print("lodgers items", len(self.__cfg['Lodgers'].items()))
        #     amount_lodgers = len(self.__cfg['Lodgers'].items())
        # except:
        #     amount_lodgers = 0

        # TODO: check if lodger demands for entry
        # print("readEntry -> entryDict", self.__entryDict)

        # no new lodger added but there are lodgers in cfg
        print(add_lodger, len(self.__entryDict), exp_len, len(self.__files))
        if len(self.__entryDict) != exp_len:
            raise KeyError("Unexpected 'EntryList' value! Number of graphs and "
                           "entries does not match or a key is used more than"
                           "once. Adjust or reset 'EntryList'.")

        # correct entry keys in case they are messed up
        # self.fixEntryDict()

        return True

    def fixEntryDict(self):

        # get key list from 'EntryList'
        keys = [int(key) for key in self.__entryDict.keys()]
        # print("fix", keys)

        # key list should start at 0 and should have a length of len(keys)
        straight_list = list(range(len(keys)))
        # print("fix", straight_list)

        # get reference list in respect to the original order of key list
        ref_list = [y for (x,y) in sorted(zip(keys, straight_list))]

        # reorder reference list so that values stay in the same order as before
        fixed_order = [y for (x,y) in sorted(zip(ref_list, straight_list))]

        # print("fix", fixed_order)
        values = list(self.__entryDict.values())
        # print("fix", values)
        new = OrderedDict(zip(fixed_order, values))
        print(new)
        # test = self.__entryDict
        # print(test.update(newDict))
        self.__cfg['Legend','EntryList'] = new

    def getDefaultEntryDict(self):
        """ Loads default names and order in respect to the KITData objects
        in 'self.__files' list. Both keys and values of the dictionary must be
        strings.

        """

        entryDict = OrderedDict()

        # write legend entries in a dict
        for i, graph in enumerate(self.__files):
            entryDict[i] = str(graph.getName())

        # check if there's a 'Lodgers' section and how many entries it has
        try:
            lodgers = [name[0] for name in self.__cfg['Lodgers'].items()]
            for i, lodger in lodgers:
                entryDict.update({str(len(self.__files)+i) : lodger})
        except:
            pass

        return entryDict

    def showCanvas(self):
        self.canvas.show()
        return True

    def saveCanvas(self):
        png_out = os.path.join("output", self.__inputName) + ".png"
        pdf_out = os.path.join("output", self.__inputName) + ".pdf"
        self.canvas.savefig(png_out)
        self.canvas.savefig(pdf_out)
        return True


###################
### Get methods ###
###################


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

    def getDataName(self, dataInput):
        return os.path.splitext(os.path.basename(os.path.normpath(str(dataInput))))[0]


if __name__ == '__main__':
    plot = KITPlot(38268)
    plot.draw('APL')
