#!/usr/bin/env python3
#pylint: disable=C0103,W0201,W0702,R1710,R1702
"""A matplotlib based python plot framework"""
import os
import warnings
import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from .kitdata import KITData
from .KITConfig import KITConfig
from .kitmatplotlib import KITMatplotlib
from .kitlodger import KITLodger

class KITPlot():
    """The framework's main class that handles the data input and top level
       organization of the plotting.

       Args:
        - cfg (str): Path to existing cfg file that contains plot parameters
        - defaultCfg (str): Path to existing cfg file that is used as a
                            blueprint for creating a new cfg file
    """
    def __init__(self, **kwargs):
        self.log = logging.getLogger(__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        if self.log.hasHandlers() is False:
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

        # Load parameters from cfg file or load default cfg
        cfg = kwargs.get('cfg', None)
        defaultCfg = kwargs.get('defaultCfg', None)
        self.auto_labeling = kwargs.get('auto_labeling', True)
        self.opt_reset = kwargs.get('reset_legend', None)
        self.opt_split = kwargs.get('split_graph', None)
        self.base_name = kwargs.get('name', None)

        if cfg is not None:
            self.__cfg = KITConfig(cfg)
        else:
            self.__cfg = KITConfig()
        self.__cfg.Dir("cfg")
        if defaultCfg is None:
            self.__cfg.Default()
        else:
            self.__cfg.Default(defaultCfg)
        self.__inputName = None
        self.name_lst = None
        self.cavas = None

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
        if self.base_name is True:
            self.__inputName = dataInput
            self.base_name = None
            return True
        # extract name from data input
        if name is None and self.__inputName is None:
            self.__inputName = self.getDataName(dataInput)
        if name is not None and self.__inputName is None:
            self.__inputName = name
        if name_lst is not None:
            self.name_lst = name_lst
        if self.opt_split:
            self.name_lst, dataInput = split_data(dataInput)

        # load dict with plot parameters or create one if not present
        self.__cfg.load(self.__inputName)

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
                        if os.path.splitext(inputFile)[1] == ".txt" \
                                or os.path.splitext(inputFile)[1] == ".yml":
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
                    if checkPID(dataInput) is True:
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
        """Searches for cfg file, load plot parameters, creates canvas, graphs
        and lodgers.
        """
        # if data is downloaded then apply axis titles according to measurement type
        # if self.new_cfg is True:
        #     self.MeasurementType()
        #     print(self.new_cfg, self.autotitle)

        # create graphs and canvas
        if dataInput is None:
            self.canvas = KITMatplotlib(
                self.__cfg,
                self.check_if_new_cfg(
                    self.__cfg.getDir(), self.__inputName)).draw(
                        self.__files, reset=self.opt_reset)
        else:
            self.canvas = KITMatplotlib(
                self.__cfg,
                self.check_if_new_cfg(
                    self.__cfg.getDir(), self.__inputName)).draw(
                        dataInput, reset=self.opt_reset)

        # check if there are lodgers in cfg and if so, add them to plot
        self.getLodgers()

        return True

    def showCanvas(self, save=None):
        """Make canvas pop up """
        if self.canvas:
            if save is True:
                self.saveCanvas()
            plt.draw()
            plt.waitforbuttonpress(0)
            plt.close()
        else:
            self.log.info("There is no canvas to show")
        return True

    def saveCanvas(self):
        """Saves output as png and pdf file"""
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
            'Lodgers'."""
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
                opt_dict = paraDict.get('opt_dict', dict())


                self.addLodger(self.canvas, x=x, y=y, name=name, color=color,
                               style=style, width=width, text=text,
                               fontsize=fontsize, alpha=alpha,
                               opt_dict=opt_dict)
        except:
            pass


    def addLodger(self, fig, **kwargs):
        """Create new Lodger object and add it to canvas"""
        newLodger = KITLodger(fig, **kwargs)
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
            t = np.arange(min(x), max(x)*1.1, min(x)/2)
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

    def check_if_new_cfg(self, path, name):
        """If cfg is new (no cfg present yet) return True, else False"""
        if self.auto_labeling is False:
            return False
        if os.path.isfile(os.path.join(path, name + ".cfg")) is True:
            return False
        return True

def checkPID(dataInput):
    """Checks if PIDs are listed in the file"""
    if os.path.isfile(dataInput):
        with open(dataInput) as inputFile:
            if len(inputFile.readline().split()) == 1:
                return True
            return False
    else:
        raise ValueError("Input is not a file.")

def split_data(data_input):
    name_lst = []
    line_data = []
    with open(data_input, "r") as data:
        for line in data:
            splitted = line.split()
            name_lst.append(splitted[0])
            try:
                line_data.append(([float(splitted[1])], [float(splitted[2])],
                                  [float(splitted[3])], [float(splitted[4])]))
            except IndexError:
                line_data.append(([float(splitted[1])], [float(splitted[2])],
                                  [0], [0]))

    return name_lst, line_data
