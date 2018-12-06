#!/usr/bin/env python3
#pylint: disable=C0103,W0201,W0702
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

    c) The ConfigHandler module writes/reads/edits a plot-specific .cfg file.
       Since KITPlot is console-based and has no graphical interface, the
       config file solution makes up for it.

    e) kitmatpoltlib handles all the drawing.

3) Installation:
    a) Create a main folder and give it a nice name (f.e. 'KITPlot')
    b) Inside this folder you ought to create a folder for cfg files named
       "cfg" and for output files named "output". Clone the KITPlot
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
    e) Plotting is based on matplotlib.
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
          of a file, folder or a run number from the database. It is also
          possible to pass a list with PIDs or a single PID.

        - Second argument: cfg file. If this is not given (None), then the
          script will search the cfg folder for a cfg file with the same name
          as the input. If you want to use a cfg file from another plot then
          this argument should be the path of this cfg file. Bottom line: names
          are important! Do not try to plot two folders that happen to have the
          same name. The former output will be overwritten with the new plot.

    A basic example of a main file could look like this:
####################################################
#!/usr/bin/env python3
# Mathtext doc: https://matplotlib.org/users/mathtext.html
import sys,os
from KITPlot import KITPlot

if len(sys.argv) > 2:
    kPlot1 = KITPlot(sys.argv[2])
else:
    kPlot1 = KITPlot(defaultCfg=os.path.join("KITPlot", "Utils", "default.cfg"))

# x_data = kPlot1.getX()
# y_data = kPlot1.getY()
# for x_lst, y_lst in zip(x_data, y_data):
# f, t, err = kPlot1.get_fit([x_data[0], y_data[0]], data_opt="listwise",
#                       fit_opt="linear", residual=True, returns="result")

kPlot1.addFiles(sys.argv[1])
# kPlot1.addFiles([46359, 45947], name="test")
kPlot1.draw()
fig = kPlot1.getCanvas()

##### LODGERS #####
# draw horizontal line
# kPlot1.addLodger(fig,y=12000,style="-",color="r0",name="test",width=2,alpha=0.3)
# draw vertical line
# kPlot1.addLodger(fig, x=180, style="-", color="b0", name="test", width=6)
# draw xy-graph
# kPlot1.addLodger(fig,x=t,y=f,style=2,color="r0",name="test",width=2)
# draw text
# kPlot1.addLodger(fig,x=1,y=10,text="Test",fontsize=20)
####################################################
kPlot1.showCanvas(save=True)
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

6) Lodgers:
    You can add graphs, lines and texts to your canvas by using lodgers.
    Examples of how to use them are given in the suggested main.

7) Fits:
    You can also use the fit function for analysis. The results can be added to
    your canvas via lodgers.
"""

import os
import sys
import warnings
import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from .kitdata import KITData
from .KITConfig import KITConfig
from .kitmatplotlib import KITMatplotlib
from .kitlodger import KITLodger

class KITPlot(object):

    # deprecated?
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

    def __init__(self, defaultCfg=None):

        self.log = logging.getLogger(__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        format_string = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        formatter = logging.Formatter(format_string)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.log.addHandler(console_handler)
        self.log.info("KITPlot initialized...")

        # ignore warning that is raised because of back-end bug while using 'waitforbuttonpress'
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")

        self.iter = iter(["lodger1", "lodger2", "lodger3"])

        # init lists
        self.__files = []
        self.__graphs = []

        # Load parameters and apply default style
        self.__cfg = KITConfig()
        self.__cfg.Dir("cfg")
        if defaultCfg is None:
            self.__cfg.Default("default.cfg")
        else:
            self.__cfg.Default(defaultCfg)

        self.__inputName = None
        self.name_lst = None
        self.cavas = None

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

    def addFiles(self, dataInput=None, name=None, name_lst=None):
        """ Depending on the type, the 'self.__files' list is filled with
        KITData objects. An integer represents a single probe ID. A string
        represents a .txt file or a folder path.
        A RPunch measurement, however, origionaly consist of one KITData file
        that needs to be split up into several KITData objects since one bias
        value (x value) represents one graph.

        Args:
            dataInput(None|int|str): Determines the way the 'self.__files'
                is filled.
            measurement(str): probe station and ALiBaVa measurements must be
                handled differently due to different database paramters
            name (str): specified name of the measured item for plot legend
            name_lst (list): if there are multiple items that need to be named
        """
        # extract name from data input
        if name is None and self.__inputName is None:
            self.__inputName = self.getDataName(dataInput)
        if name is not None and self.__inputName is None:
            self.__inputName = name
        if name_lst is not None:
            self.name_lst = name_lst

        # load dict with plot parameters or create one if not present
        self.__cfg.load(self.__inputName)

        #TODO: handle multiple KITPlot objects to create canvas with multiple subplots
        # if isinstance(dataInput, KITPlot):
        if self.__cfg['General', 'Measurement'] == "probe":
            # Load KITData
            if isinstance(dataInput, KITData):
                self.log.info("Input interpreted as KITData object")
                self.__files.append(dataInput)
                # self.addGraph(dataInput.getX(),dataInput.getY())

            # Load list/tuple with raw data or list with PIDs
            elif isinstance(dataInput, (list, tuple)):
                if all([isinstance(elem, int) for elem in dataInput]):
                    self.log.info("Input interpreted as list with multiple PIDs")
                else:
                    self.log.info("Input interpreted as raw data")
                for i, tup in enumerate(dataInput):
                    self.__files.append(KITData(tup))
                    try:
                        self.__files[-1].setName(self.name_lst[i])
                    except:
                        pass
            # Load single integer PID
            elif isinstance(dataInput, int):
                self.__files.append(KITData(dataInput))
            elif isinstance(dataInput, str):
                # Load single string PID
                if dataInput.isdigit():
                    kdata = KITData(dataInput)
                    # PID represents a Rpunch measurement
                    if "Ramp" in kdata.getParaY():
                        self.log.info("Input interpreted as ramp measurement")
                # split data so that each ramp step becomes a KITData object
                        kdict = self.get_r_dict(kdata)
                        kdata_lst = self.handle_ramp(kdict)
                        self.__files = kdata_lst

                    else:
                        self.log.info("Input interpreted as single PID")
                        self.__files.append(kdata)

                # Load multiple data files in a folder
                elif os.path.isdir(dataInput):
                    self.log.info("Input interpreted as folder with files")
                    for i, inputFile in enumerate(os.listdir(dataInput)):
                        if os.path.splitext(inputFile)[1] == ".txt":
                            self.__files.append(KITData(dataInput + inputFile))
                            try:
                                self.__files[-1].setName(self.name_lst[i])
                            except:
                                pass
                        else:
                            pass

                # Load file
                elif os.path.isfile(dataInput):
                    # multiple PIDs
                    if self.checkPID(dataInput) is True:
                        self.log.info("Input interpreted as multiple PIDs")
                        with open(dataInput) as inputFile:
                            fileList = []
                            for i, line in enumerate(inputFile):
                                entry = line.split()
                                if entry[0].isdigit():
                                    fileList.append(\
                    KITData(entry[0], self.__cfg['General', 'Measurement']))
                                    try:
                                        fileList[-1].setName(self.name_lst[i])
                                    except:
                                        pass
                            # if measurement == "probe":
                            self.__files = fileList
                            # elif measurement == "alibava":
                            #     self.__files.append(KITData(fileList))

                    # singel file
                    else:
                        self.log.info("Input interpreted as single file")
                        self.__files.append(KITData(dataInput))
                        try:
                            self.__files[-1].setName(self.name_lst[0])
                        except:
                            pass
                # new feature: multiple PIDs in argument
                elif any(n in inputFile for n in ["[", "]", "(", ")"]):
                    entry = inputFile.replace("[", "").replace("]", "")\
                            .replace("(", "").replace(")", "").split(",")
                    if all([n.isdigit() for n in entry]):
                        self.log.info("Input interpreted as argument with"
                                      "multiple PIDs ")



        if "Rpunch" in self.__cfg['General', 'Measurement'] and os.path.isfile(dataInput):
            self.log.info("Input interpreted as multiple PIDs of Ramp measurements")
            with open(dataInput) as inputFile:
                val_lst = []
                res_lst = []
                fileList = []
                # loop through file and create KITData object for every PID
                for i, line in enumerate(inputFile):
                    entry = line.split()
                    if entry[0].isdigit():
                        self.__files.append(KITData(entry[0]))
                    else:
                        raise ValueError
                    kdict = self.get_r_dict(self.__files[-1])
                    # plot graph for every single PID
                    if "@" not in self.__cfg['General', 'Measurement']:
                        x_lst = []
                        y_lst = []
                        kdata_lst = self.handle_ramp(kdict)
                        for kdata in kdata_lst:
                            x = [abs(x) for x in kdata.getX()]
                            y = [abs(y) for y in kdata.getY()]
                            m = self.get_fit([x, y], data_opt="listwise",
                                             name=kdata.getName(),
                                             returns="result")[0]
                            y_lst.append(1/m)
                            # y_lst.append(1/m*0.46/0.02)
                            x_lst.append(kdata.getZ())

                        kdata_new = KITData()
                        kdata_new.setX(x_lst)
                        kdata_new.setY(y_lst)
                        try:
                            kdata_new.setName(self.name_lst[i])
                        except:
                            kdata_new.setName(str(i))
                        kdata_new.setPX("Voltage")
                        kdata_new.setPY("Resistance")
                        self.__files[-1] = kdata_new
                    # plot only values at given bias voltage of all PIDs
                    else:
                        bias_aim = self.__cfg['General', 'Measurement'].split("@")[1] #pylint: disable=E1101
                        x, y = self.handle_ramp(kdict, bias_aim=int(bias_aim))
                        x = [abs(xi) for xi in x]
                        y = [abs(yi) for yi in y]
                        m, _, res = self.get_fit([x, y], data_opt="listwise",
                                                 name=entry[0],
                                                 returns="result",
                                                 residual=True)
                        # val_lst.append(1/m)
                        val_lst.append(1/m*0.46/0.02)
                        res_lst.append(res/((m + res)*(m + res)))
                if "@" in self.__cfg['General', 'Measurement']:
                    kdata_new = KITData()
                    kdata_new.setX(range(0, len(val_lst)))
                    # kdata_new.setX([2, 3.8, 5.5, 7, 8.6, 10.25, 11.9, 13.5,
                    #                 16.8, 20.3, 28, 37, 48])
                    kdata_new.setX([10, 20, 30, 40, 50, 60, 70, 80,
                                    100, 120, 160, 200, 240])
                    # kdata_new.setX([0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 1.7, 1.9,
                    #                 2.4, 2.9, 4.0, 5.3, 6.9])

                    kdata_new.setY(val_lst)
                    self.__files = []
                    self.__files.append(kdata_new)


        return True


    def draw(self, dataInput=None):
        """Searches for cfg file, load plot parameters, creates canvas graphs
        and lodgers.
        """
        cfg_path = os.path.join(os.getcwd(), "cfg", self.__inputName) + ".cfg"
        cfg_present = os.path.isfile(cfg_path)

        # if data is downloaded then apply axis titles according to measurement type
        # if cfg_present is False:
        #     self.MeasurementType()

        # create graphs and canvas
        if dataInput is None:
            self.canvas = KITMatplotlib(self.__cfg, cfg_present).draw(self.__files)
        else:
            self.canvas = KITMatplotlib(self.__cfg, cfg_present).draw(dataInput)

        # check if there are lodgers in cfg and if so, add them to plot
        self.getLodgers()

        return True

    def showCanvas(self, save=None):
        try:
            self.canvas.show()
            if save is True:
                self.saveCanvas()
            # this will wait for indefinite time
            try:
                plt.waitforbuttonpress(0)
            except:
                pass
            plt.close(self.canvas)
        except AttributeError:
            self.log.info("There is no canvas to show")
        return True

    def saveCanvas(self):
        png_out = os.path.join("output", self.__inputName) + ".png"
        pdf_out = os.path.join("output", self.__inputName) + ".pdf"
        self.canvas.savefig(png_out)
        self.canvas.savefig(pdf_out)
        return True

######################
### Lodger methods ###
######################

    def getLodgers(self):
        """ Read the cfg and create a lodger object for every entry in
            'Lodgers'.
        """
        try:
            for lodger in self.__cfg['Lodgers']:
                paraDict = dict(self.__cfg['Lodgers'][lodger])
                x = paraDict.get('x', None)
                y = paraDict.get('y', None)
                name = paraDict.get('name', None)
                color = paraDict.get('color', None)
                width = paraDict.get('width', None)
                style = paraDict.get('style', None)
                text = paraDict.get('text', None)
                fontsize = paraDict.get('fontsize', None)
                alpha = paraDict.get('alpha', None)


                self.addLodger(self.canvas, x=x, y=y, name=name, color=color,
                               style=style, width=width, text=text,
                               fontsize=fontsize, alpha=alpha)
        except:
            pass


    def addLodger(self, fig, x=None, y=None, name=None, color=None, style=None,
                  width=None, text=None, fontsize=None, alpha=None):

        newLodger = KITLodger(fig, x=x, y=y, name=name, color=color,
                              style=style, width=width, text=text,
                              fontsize=fontsize, alpha=alpha)

        self.canvas = newLodger.add_to_plot()
        newLodger.add_to_cfg(self.__cfg)

        return True

    def get_fit(self, data_lst, data_opt="pointwise", fit_opt="linear",
                returns="fit", residual=False, name=None):
        """Fits data points. 'data_lst' is expected to a list containing list
        elements with list(x) and list(y) values.
        Args:
            - data_lst = [[[x1], [y1]], [[x2], [y2]], [[x3], [y3]], ...]
        Returns:
            Data points (x-list, y-list) for fit graph
        """
        if data_opt == "pointwise":
            x = [tup[0][0] for tup in data_lst]
            y = [tup[1][0] for tup in data_lst]
        if data_opt == "listwise":
            x = data_lst[0]
            y = data_lst[1]
        if fit_opt == "linear":
            m, b, _, _, err = stats.linregress(x, y)
            if name is None and residual is False:
                self.log.info("Fit result:::(m = %s, y0 = %s)", str(m), str(b))
            if name is None and residual is True:
                self.log.info("Fit result:::(m = %s, y0 = %s, res = %s)",
                              str(m), str(b), str(err))
            if name is not None and residual is False:
                self.log.info("Fit result[%s]:::(m = %s, y0 = %s)",
                              name, str(m), str(b))
            if name is not None and residual is True:
                self.log.info("Fit result[%s]:::(m = %s, y0 = %s, res = %s)",
                              name, str(m), str(b), str(err))
            t = np.arange(min(x), max(x)*1.1, (min(x) + max(x)/5))
            f = m * t + b
        if returns == "fit":
            return (f, t)
        if returns == "result":
            try:
                return (m, b, err)
            except:
                return (m, b)


    def handle_ramp(self, kdict, bias_aim=None):
        x = []
        y = []
        kdata_lst = []
        for bias in kdict.keys():
            # create an empty KITData object
            kdata = KITData()
            # extract each single bias value from the dictionary
            # and create KITData files for every value
            if bias_aim is None:
                x, y = zip(*kdict[bias])
                kdata.setX(list(x))
                kdata.setY(list(y))
                kdata.setZ(bias)
                kdata.setName(str(bias) + " V")
                kdata.setPX("Voltage")
                kdata.setPY("Rpunch")
                kdata_lst.append(kdata)
            else:
                if int(bias) == bias_aim:
                    return zip(*kdict[bias])
        return kdata_lst

###################
### Get methods ###
###################


    def get_r_dict(self, kdata):
        """Get the values from the KITData file and convert it into
        a dictionary: {V_bias_0 = (V_edge, I_edge),
                       V_bias_0 = (V_edge, I_edge), ...,
                       V_bias_1 = (V_edge, I_edge), ...}
        """
        ramp = []
        dic = {}
        for x in kdata.getX():
            if x not in ramp:
                ramp.append(int(round(x)))
        for bias in ramp:
            ix = []
            iy = []
            # Rpunch Ramps: x = V_bias, y = V_edge, z = I_edge
            for (valX, valY, valZ) in zip(kdata.getX(), kdata.getY(), kdata.getZ()):
                if bias == valX:
                    ix.append(valY)
                    iy.append(valZ)
                    dic[bias] = zip(ix, iy)
        return dic

    def getGraph(self, graph=None):

        if len(self.__graphs) == 1:
            return self.__graphs[0]
        elif (len(self.__graphs) != 1) and (graph is None):
            return self.__graphs
        else:
            if isinstance(graph, str):
                if len(self.__graphs) != 1 and graph.isdigit():
                    return self.__graphs[int(graph)]
                else:
                    return False
            elif isinstance(graph, int):
                if len(self.__graphs) != 1:
                    return self.__graphs[graph]
                else:
                    return False

    def getFile(self, KITFile=None):

        if len(self.__files) == 1:
            return self.__files[0]
        elif len(self.__files) != 1 and KITFile is None:
            return self.__files
        else:
            if isinstance(KITFile, str):
                if len(self.__files) != 1 and KITFile.isdigit():
                    return self.__files[int(KITFile)]
                else:
                    return False
            elif isinstance(KITFile, int):
                if len(self.__files) != 1:
                    return self.__files[KITFile]
                else:
                    return False

    def getCanvas(self):
        if self.canvas is None:
            return None
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
        """Check data input and try to extract the name for legend, cfg and
        outputfile"""
        if dataInput is None:
            self.log.info("No data input. Name not extractable.")
            return None
        if isinstance(dataInput, str):
            name = os.path.splitext(os.path.basename(os.path.normpath(str(dataInput))))[0]
            self.log.info("Extracted name from data input: %s", name)
            return name
        elif isinstance(dataInput, int):
            self.log.info("Data input interpreted as PID. Name is PID.")
            return str(dataInput)
        else:
            raise ValueError("Unkonwn case in 'getDataName' function")
