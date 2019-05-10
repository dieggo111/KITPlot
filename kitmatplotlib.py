#!/usr/bin/env python3
#pylint: disable=C0103,R0902,R0912,R0915,R0914,W0201
import numpy as np
import matplotlib.pyplot as plt
from .kitdata import KITData
from .kitlodger import KITLodger
from collections import OrderedDict
from .Utils import kitutils
import itertools
import logging


class KITMatplotlib(object):
    """Matplotlib based automated plotting class for KITPlot"""
    def __init__(self, cfg=None, new_cfg=None):

        self.__graphs = []
        self.__lodgers = []

        # KITcolor dictionary
        self.KITcolor = kitutils.get_KITcolor()

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        if self.log.hasHandlers is False:
            format_string = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            formatter = logging.Formatter(format_string)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.log.addHandler(console_handler)

        # load style parameters from cfg file
        self.__initStyle(cfg)
        self.__new_cfg = new_cfg


    def __initStyle(self, cfg):
        """ Loads and sets various parameters from cfg file which are then used
            to create the desired plot.

        """
        self.cfg = cfg
        # Canvas Options
        self.canvasSize = kitutils.extractList(cfg['Canvas', 'CanvasSize'], 'float')

        # Pad Options
        self.grid = True
        self.gridOptions = ('w', '-', '0.5')
        self.padSize = kitutils.extractList(cfg['Canvas', 'PadSize'], 'float')

        # Title options
        self.title = cfg['Title', 'Title']
        self.titleFont = cfg['Title', 'Font']
        self.titleFontSize = cfg['Title', 'FontSize']
        self.titleFontStyle = cfg['Title', 'FontStyle']
        self.titleOffset = 1 + cfg['Title', 'Offset']/100.

        # Axis Options
        self.labelX = cfg['XAxis', 'Title']
        self.labelY = cfg['YAxis', 'Title']
        self.rangeX = kitutils.extractList(cfg['XAxis', 'Range'], "float")
        self.rangeY = kitutils.extractList(cfg['YAxis', 'Range'], "float")
        self.fontX = cfg['XAxis', 'Font']
        self.fontY = cfg['YAxis', 'Font']
        self.fontSizeX = cfg['XAxis', 'FontSize']
        self.fontSizeY = cfg['YAxis', 'FontSize']
        self.fontStyleX = cfg['XAxis', 'FontStyle']
        self.fontStyleY = cfg['YAxis', 'FontStyle']
        self.absX = cfg['XAxis', 'Abs']
        self.absY = cfg['YAxis', 'Abs']
        self.logX = cfg['XAxis', 'Log']
        self.logY = cfg['YAxis', 'Log']
        self.tickX = cfg['XAxis', 'SciTick']
        self.tickY = cfg['YAxis', 'SciTick']

        # Marker Options
        self.markerSize = cfg['Marker', 'Size']
        self.markerSet = kitutils.extractList(cfg['Marker', 'Set'])
        self.hollowMarker = kitutils.extractList(cfg['Marker', 'HollowMarker'])

        #Line options
        self.colorPalette = cfg['Line', 'ColorPalette']
        self.colorSet = kitutils.extractList(cfg['Line', 'Color'])
        self.lineWidth = cfg['Line', 'Width']
        self.lineStyle = kitutils.extractList(cfg['Line', 'Style'])
        self.err = cfg['Line', 'ErrorBars']

        # KITPlot specific options
        self.norm = kitutils.extractList(cfg['Misc', 'Normalization'])
        self.splitGraph = cfg['Misc', 'SplitGraph']
        # try:
        #     self.

        # legend options
        self.__entryDict = cfg['Legend', 'EntryList']
        self.legPosition = cfg['Legend', 'Position']
        self.show_pid = cfg['Legend', 'ShowPID']
        self.leg_col = cfg['Legend', 'Columns']

        # sets
        self.markers = {'s': 'square', 'v': 'triangle_down', '^': 'triangle_up',
                        '<': 'triangle_left', '>': 'triangle_right',
                        '8': 'octagon', 'p': 'pentagon', '*': 'star',
                        'h': 'hexagon1', 'H': 'hexagon2',
                        'D': 'diamond', 'd': 'thin_diamond', 'P': 'plus_filled',
                        'X': 'x_filled'}
        self.lines = ['None', '-', '--', '-.', ':']
        self.colors = self.__initColor()

        return True

    def __initColor(self):

        # standard mpl colorSet
        mpl_std = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

        if self.colorPalette == "std":
            mpl_std_sorted = [item for (i, item) in sorted(zip(self.colorSet, mpl_std))]
            return mpl_std_sorted
        elif self.colorPalette == "KIT":
            return list(self.KITcolor.keys())
        self.log.warning("Invalid 'ColorPalette' value. Using KITcolor as default")
        return list(self.KITcolor.keys())

    def addGraph(self, arg):
        """ Converts data of KITData objects or lists into a respective formate
        and writes them into .__graphs. Lodgers are seperated and written into
        .__lodgers.

        Args: x, y or KITData

        """

        x = []
        y = []
        dx = []
        dy = []
        if isinstance(arg, KITData):
            if KITData().getRPunchDict() is None:
                # toggle absolute mode
                if self.absX:
                    x = list(np.absolute(arg.getX()))
                else:
                    x = arg.getX()
                if self.absY:
                    y = list(np.absolute(arg.getY()))
                else:
                    y = arg.getY()
                # get error bars if present
                if arg.getdX() != [] and arg.getdY() != []:
                    dx = arg.getdX()
                    dy = arg.getdY()
                elif arg.getdX() == [] and arg.getdY() == []:
                    pass
                else:
                    raise ValueError("Check data table. Only 2 (x,y) or "
                                     "4 (x,y,dx,dy) coordinates are allowed.")
                # create graph list
                if dx == [] and dy == []:
                    self.__graphs.append([x, y])
                elif dx != [] and dy != []:
                    self.__graphs.append([x, y, dx, dy])
                else:
                    raise ValueError("z-error not implemented yet")
            # Rpunch
            else:
                raise ValueError("Dictionary error")

        elif isinstance(arg, list) and len(arg) in [2,4]:
            if self.absX:
                x = list(np.absolute(arg[0]))
            else:
                x = arg
            if self.absY:
                y = list(np.absolute(arg[1]))
            else:
                y = arg[1]
            if len(arg) == 4:
                dx = arg[2]
                dy = arg[3]

            # create graph list
            if dx == [] and dy == []:
                self.__graphs.append([x, y])
            elif dx != [] and dy != []:
                self.__graphs.append([x, y, dx, dy])
            else:
                raise ValueError("z-error not implemented yet")

        # add lodger
        elif isinstance(arg, KITLodger):
            self.__lodgers.append(arg)

        else:
            raise ValueError("Cant add following graph: " + str(arg))

        return True


    def draw(self, fileList):
        """Extracts data sets from fileList, extracts plot parameters from cfg
        (plot options, legend information, plot dimensions, axis labeling,
        marker and graph options, ...) and applies them"""
        # create self.__graphs list
        for dset in fileList:
            self.addGraph(dset)

        # read and adjsut .__entryDict before drawing
        self.readEntryDict(len(self.__graphs), self.getDefaultEntryDict(fileList))

        # interpret all entries in single file as graphs instead of a singel graph
        if self.splitGraph is True and len(self.__graphs) == 1:
            self.__graphs = [list(item) for item in zip(*self.__graphs[0])]

            # adjust entryDict
            newLength = len(self.__graphs)
            if len(self.__entryDict) != newLength:
                self.__entryDict = OrderedDict([])
                for i in range(0, newLength):
                    self.__entryDict.update({str(i) : "Data"+str(i)})
                self.cfg["Legend", "EntryList"] = self.__entryDict

        elif self.splitGraph is True and len(self.__graphs) != 1:
            self.log.warning("Can only split single graph. Request rejected")

        # apply user defined normalization or manipulation of y values of each graph
        self.__graphs = kitutils.manipulate(self.__graphs, self.norm)

        # create an empty canvas with canvas size in [inch]: 1 inch = 2.54 cm
        fig = plt.figure(figsize=list(map(lambda x: x/2.54, self.canvasSize)))
        # specify (nrows, ncols, axnum)
        ax = fig.add_subplot(1, 1, 1)
        # adjust pad size: [left, bottom, width, height]
        ax.set_position(self.padSize)

        # adjust axis tick
        if self.tickX:
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        if self.tickY:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        for i, table in enumerate(self.__graphs):
            if isinstance(self.hollowMarker, list) and i in self.hollowMarker:
                markerface = 'white'
            else:
                markerface = self.getColor(i)
            ax.plot(table[0],                           # x-axis
                    table[1],                           # y-axis
                    color=self.getColor(i),             # line color
                    marker=self.getMarker(i),           # marker style
                    markersize=self.markerSize,
                    markerfacecolor=markerface,
                    linewidth=self.lineWidth,
                    linestyle=self.getLineStyle(i),
                    label=self.getLabel(i))

        # set error bars
        for i, table in enumerate(self.__graphs):
            if len(table) == 4 and self.err is True:
                ax.errorbar(table[0], table[1], xerr=table[2], yerr=table[3],
                            color=self.getColor(i),
                            elinewidth=1)
            elif len(table) == 4 and self.err == "filled":
                y1 = []
                y2 = []
                if all(table[2]) == 0:
                    for y, err in zip(table[1], table[3]):
                        y1.append(y - err)
                        y2.append(y + err)
                else:
                    for y, min, max in zip(table[1], table[2], table[3]):
                        y1.append(y - min)
                        y2.append(y + max)

                ax.fill_between(table[0], y1, y2, alpha=0.3, lineWidth=0, color=self.getColor(i))
            elif len(table) != 4 and self.err in [True, "filled"]:
                self.log.warning("Can't find x- and y-errors in file. Request "
                                 "rejected.")

        # set titles
        # weights = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
        if self.__new_cfg is True:
            self.title, self.labelX, self.labelY = \
                auto_axis_labeling(fileList)
            self.cfg['XAxis', 'Title'] = self.labelX
            self.cfg['YAxis', 'Title'] = self.labelY
            self.cfg['Title', 'Title'] = self.title

        ax.set_title(self.title,
                     fontsize=self.titleFontSize,
                     y=self.titleOffset,
                     fontweight=self.titleFontStyle)
        ax.set_xlabel(self.labelX,
                      fontsize=self.fontSizeX,
                      fontweight=self.fontStyleX)
        ax.set_ylabel(self.labelY,
                      fontsize=self.fontSizeY,
                      fontweight=self.fontStyleY)

        # set log styles
        if self.logX:
            ax.semilogx()
        if self.logY:
            ax.semilogy()

        # set grid
        if self.grid == True:
            # *args = [color,linstyle,linewidth]
            ax.grid()

        # set axis range manually
        if self.rangeX != 'auto':
            ax.set_xlim(self.rangeX)
        if self.rangeY != 'auto':
            ax.set_ylim(self.rangeY)

        self.setLegend(ax)

        return fig


    def setLegend(self, obj):

        # get names from cfg and lodger labels
        graphEntries = [items[1] for items in list(self.__entryDict.items())]

        total_len = len(self.__graphs)

        # reorder legend items according to 'EntryList'
        handles, labels = obj.get_legend_handles_labels()
        # handles = self.adjustOrder(handles)
        # labels = self.adjustOrder(labels)
        handles = kitutils.adjustOrder(handles, self.__entryDict, total_len)
        labels = kitutils.adjustOrder(labels, self.__entryDict, total_len)

        if self.legPosition == "auto":
            obj.legend(handles, labels)
        elif self.legPosition == "TL":
            obj.legend(handles, labels, loc='upper left')
        elif self.legPosition == "BL":
            obj.legend(handles, labels, loc='lower left')
        elif self.legPosition == "TR":
            obj.legend(handles, labels, loc='upper right')
        elif self.legPosition == "BR":
            obj.legend(handles, labels, loc='lower right')
        elif self.legPosition == "test2":
            obj.legend(handles, labels, bbox_to_anchor=(0., 1.17, 1., .102),
                       loc='upper right', ncol=self.leg_col, mode="expand", borderaxespad=0.)
        elif self.legPosition == "test":
            obj.legend(handles, labels, bbox_to_anchor=(0., 0.,1.,1.),
                       loc='lower left', ncol=self.leg_col, mode="expand", borderaxespad=0.)
        elif self.legPosition == "below":
            obj.legend(handles, labels, bbox_to_anchor=(0., -0.25, 1., .102),
                       loc='lower center', ncol=self.leg_col, mode="expand", borderaxespad=0.)
        elif self.legPosition == "outside":
            if total_len > 8:
                ncol = 2
            else:
                ncol = 1
            obj.legend(handles, labels, bbox_to_anchor=(1, 1.01),
                       loc='upper left', ncol=self.leg_col)
        return True


    def getLabel(self, index):
        label = [items[1] for items in list(self.__entryDict.items())]
        return label[index]


    def getMarker(self, index):
        """ Returns a valid marker value for matplotlib's plot() function. If
        'MarkerSet' is a list, the method will cycle the list's items until all
        graphs are taken care of.

            Args:
                index (int): represents an iterator marking a certain graph in
                             .__graphs
        """

        try:
            # assign same marker to all graphs
            if isinstance(self.markerSet, int):
                return list(self.markers.keys())[self.markerSet]
            # cycle list of strings
            elif all(isinstance(item, str) for item in self.markerSet):
                for i, item in enumerate(itertools.cycle(self.markerSet)):
                    if index == i:
                        return item
            # cycle list of integers
            elif all(isinstance(item, int) for item in self.markerSet):
                for i, item in enumerate(itertools.cycle(self.markerSet)):
                    if index == i:
                        return list(self.markers.keys())[item]
        except:
            self.log.warning("Invalid value in 'MarkerSet'. Using default instead.")
            return list(self.markers.keys())[index]


    def getColor(self, index):

        try:
            # self.colors represents color_keys in KITcolor
            if all(isinstance(item, int) for item in self.colorSet) \
                        and isinstance(self.colorSet, list):
                for i, item in enumerate(itertools.cycle(self.colorSet)):
                    if i == index:
                        color = self.KITcolor[self.colors[item]][0][1]
                        return color

            # if colors in 'ColorSet' are strings and correspond to entries
            # in KITcolor dict
            elif all(isinstance(item, str) for item in self.colorSet) \
                        and isinstance(self.colorSet, list):
                # in case there are less entries in colorSet than needed we n
                # eed to cycle that list
                for i, cycled in enumerate(itertools.cycle(self.colorSet)):
                    if i == index:
                        color = cycled
                        break
                # search for RGB values in KITcolor dict for given color key
                for colorDict in list(self.KITcolor.values()):
                    try:
                        return colorDict[color]
                    except:
                        pass

        except:
            self.log.warning("Invalid input in 'ColorSet'. Using default instead.")
            for i, color in enumerate(itertools.cycle(self.colors)):
                if i == index:
                    return list(self.KITcolor[color].values())[0]


    def getLineStyle(self, index):
        try:
            if isinstance(self.lineStyle, int):
                return self.lines[self.lineStyle]
            elif all(isinstance(item, str) for item in self.lineStyle) \
                    and isinstance(self.lineStyle, list):
                for i, item in enumerate(itertools.cycle(self.lineStyle)):
                    if item not in self.lines:
                        raise ValueError
                    if index == i:
                        return item
            elif all(isinstance(item, int) for item in self.lineStyle) \
                    and isinstance(self.lineStyle, list):
                for i, item in enumerate(itertools.cycle(self.lineStyle)):
                    if index == i:
                        return self.lines[item]
        except:
            self.log.warning("Invalid value in 'LineStyle'. Using default instead.")
            return self.lines[1]


    def getGraphList(self):
        return self.__graphs


    def readEntryDict(self, exp_len, def_list):
        """'EntryList' makes the names and order of all graphs accessible. This
        subsection is read every time KITPlot is executed. An empty value ("")
        can be used to reset the entry to its default value (the original order
        and names given by .__files).
        """
        # writes entry dict to cfg and sets it back to default if value is ""
        if self.cfg['Legend','EntryList'] == "":
            self.cfg['Legend','EntryList'] = def_list
            self.__entryDict = def_list
            if self.__new_cfg is False:
                self.log.info("EntryDict was set back to default!")
        # calculate expected number of entries in 'EntryList'
        if len(self.__entryDict) != exp_len and self.splitGraph == False:
            raise KeyError("Unexpected 'EntryList' value! Number of graphs and "
                           "entries does not match or a key is used more than"
                           "once. Adjust or reset 'EntryList'.")
        return True

    def fixEntryDict(self):

        # get key list from 'EntryList'
        keys = [int(key) for key in self.__entryDict.keys()]

        # key list should start at 0 and should have a length of len(keys)
        straight_list = list(range(len(keys)))

        # get reference list in respect to the original order of key list
        ref_list = [y for (x, y) in sorted(zip(keys, straight_list))]

        # reorder reference list so that values stay in the same order as before
        fixed_order = [y for (x, y) in sorted(zip(ref_list, straight_list))]

        values = list(self.__entryDict.values())
        new = OrderedDict(zip(fixed_order, values))
        self.cfg['Legend', 'EntryList'] = new


    def getDefaultEntryDict(self, List):
        """ Loads default names and order in respect to the KITData objects
        in 'file_lst' list. Both keys and values of the dictionary must be
        strings.
        """
        i = 0
        entryDict = OrderedDict()
        # write legend entries in a dict
        for i, graph in enumerate(List):
            if graph.getName() == None:
                entryDict[i] = "graph" + str(i)
                i += 1
            else:
                if self.show_pid is True:
                    entryDict[i] = str(graph.getID()) + " - " + graph.getName()
                else:
                    entryDict[i] = graph.getName()

        return entryDict

def auto_axis_labeling(file_lst):
    """ If KITPlot is initialized with probe IDs it is able to determine the
    measurement type by checking database information. The default axis
    labels and titles are then set according to this information as soon as
    the respective cfg file is created.
    """

    if file_lst[0].getParaY() is None:
        autotitle = "Title"
        autotitleY = "Y Value"
        autotitleX = "X Value"
    else:
        MT = file_lst[0].getParaY()
        if MT == "I_tot":
            autotitle = "Current Voltage Characteristics"
            autotitleY = "Current (A)"
            autotitleX = "Voltage (V)"
        elif MT == "Pinhole":
            autotitle = "Pinhole Leakage"
            autotitleY = "Current (A)"
            autotitleX = "Strip No"
        elif MT == "I_leak_dc":
            autotitle = "Strip Leakage Current"
            autotitleY = "Current (A)"
            autotitleX = "Strip No"
        elif MT == "C_tot":
            autotitle = "Capacitance Voltage Characteristics"
            autotitleY = "Capacitance (F)"
            autotitleX = "Voltage (V)"
        elif MT == "C_int":
            autotitle = "Interstrip Capacitance Measurement"
            autotitleY = "Capacitance (F)"
            autotitleX = "Strip No"
        elif MT == "CC":
            autotitle = "Coupling Capacitance Measurement"
            autotitleY = "Capacitance (F)"
            autotitleX = "Strip No"
        elif MT == "R_int":
            autotitle = "Interstrip Resistance Measurement"
            autotitleY = "Resistance (#Omega)"
            autotitleX = "Strip No"
        elif MT == "R_poly_dc":
            autotitle = "Strip Resistance Measurement"
            autotitleY = "Resistance (#Omega)"
            autotitleX = "Strip No"
        elif MT == "C_int_Ramp":
            autotitle = "Interstrip Capacitance Measurement"
            autotitleY = "Capacitance (F)"
            autotitleX = "Voltage (V)"
        elif MT == "R_int_Ramp":
            autotitle = "Strip Resistance Measurement"
            autotitleY = "Resistance (#Omega)"
            autotitleX = "Voltage (V)"
        elif MT == "I_leak_dc_Ramp":
            autotitle = "Interstrip Current Leakage"
            autotitleY = "Current (A)"
            autotitleX = "Voltage (V)"
        elif MT == "V_Ramp":
            autotitle = "R_{Edge} Measurement"
            autotitleY = "Current (A)"
            autotitleX = "Voltage (V)"
        else:
            autotitle = "Title"
            autotitleY = "Y Value"
            autotitleX = "X Value"

    return autotitle, autotitleX, autotitleY
