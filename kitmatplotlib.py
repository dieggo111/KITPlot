#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from .KITConfig import KITConfig
from .kitdata import KITData
from .kitlodger import KITLodger
from collections import OrderedDict
from .Utils import kitutils
import itertools
import logging


class KITMatplotlib(object):

    def __init__(self, cfg=None):

        self.__graphs = []
        self.__lodgers = []

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # load style parameters from cfg file
        self.__initStyle(cfg)


    def __initStyle(self, cfg):
        """ Loads and sets various parameters from cfg file which are then used
            to create the desired plot.

        """
        self.cfg = cfg
        # Canvas Options
        self.canvasSize = kitutils.extractList(cfg['Canvas','CanvasSize'], 'float')

        # Pad Options
        self.grid = True
        self.gridOptions = ('w', '-', '0.5')
        self.padSize = kitutils.extractList(cfg['Canvas','PadSize'], 'float')

        # Title options
        self.title = cfg['Title','Title']
        self.titleFont = cfg['Title','Font']
        self.titleFontSize = cfg['Title','FontSize']
        self.titleFontStyle = cfg['Title','FontStyle']
        self.titleOffset = 1 + cfg['Title','Offset']/100.

        # Axis Options
        self.labelX = cfg['XAxis','Title']
        self.labelY = cfg['YAxis','Title']
        self.rangeX = kitutils.extractList(cfg['XAxis','Range'], "float")
        self.rangeY = kitutils.extractList(cfg['YAxis','Range'], "float")
        self.fontX = cfg['XAxis','Font']
        self.fontY = cfg['YAxis','Font']
        self.fontSizeX = cfg['XAxis','FontSize']
        self.fontSizeY = cfg['YAxis','FontSize']
        self.fontStyleX = cfg['XAxis','FontStyle']
        self.fontStyleY = cfg['YAxis','FontStyle']
        self.absX = cfg['XAxis','Abs']
        self.absY = cfg['YAxis','Abs']
        self.logX = cfg['XAxis','Log']
        self.logY = cfg['YAxis','Log']
        self.tickX = cfg['XAxis','SciTick']
        self.tickY = cfg['YAxis','SciTick']

        # Marker Options
        self.markerSize = cfg['Marker','Size']
        self.markerSet = kitutils.extractList(cfg['Marker','Set'])
        self.hollowMarker = kitutils.extractList(cfg['Marker','HollowMarker'])

        #Line options
        self.colorPalette = cfg['Line','ColorPalette']
        self.colorSet = kitutils.extractList(cfg['Line','Color'])
        # print("colorSet", self.colorSet)
        # self.logger.info("HALLO")
        self.lineWidth = cfg['Line','Width']
        self.lineStyle = kitutils.extractList(cfg['Line','Style'])

        # KITPlot specific options
        self.graphGroup = cfg['Misc','GraphGroup']
        self.norm = kitutils.extractList(cfg['Misc','Normalization'])
        self.splitGraph = cfg['Misc','SplitGraph']

        # legend options
        self.__entryDict = cfg['Legend','EntryList']
        self.legPosition = cfg['Legend','Position']

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

        mpl_std = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

        self.KITcolor = kitutils.get_KITcolor()

        if self.colorPalette == "std":
            mpl_std_sorted = [item for (i,item) in sorted(zip(self.colorSet, mpl_std))]
            return mpl_std_sorted
        elif self.colorPalette == "KIT":
            return list(self.KITcolor.keys())
        else:
            print("Warning:::Invalid 'ColorPalette' value. Using KITcolor as default")
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
            if KITData().getRPunchDict() == None:
                # self.__files.append(arg)
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
            if len(args) == 4:
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
        """
        doc

        """

        # create self.__graphs list
        for i, dset in enumerate(fileList):
            self.addGraph(dset)
        # print(self.__graphs, self.__lodgers)
        # if self.splitGraph is True:
        #     self.__graphs = [list(item) for item in zip(self.__graphs[0][0],self.__graphs[0][1])]
        #     print(len(self.__graphs))


        # apply user defined normalization or manipulation of y values of each graph
        kitutils.manipulate(self.__graphs, self.norm)

        # create an empty canvas with canvas size in [inch]: 1 inch = 2.54 cm
        fig = plt.figure(figsize=list(map(lambda x: x/2.54, self.canvasSize)))

        # specify (nrows, ncols, axnum)
        ax = fig.add_subplot(1, 1, 1)

        # adjust pad size: [left, bottom, width, height]
        ax.set_position(self.padSize)

        # adjust axis tick
        if self.tickX:
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        if self.tickY:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        # check GraphGroup
        self.graphGroup = self.getGG(self.graphGroup)

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
            if len(table) == 4:
                ax.errorbar(table[0],table[1],xerr=table[2],yerr=table[3],
                            color=self.getColor(i),
                            elinewidth=1)


        # set titles
        # weights = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
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

        # x = [graph[0][0] for graph in self.__graphs]
        # y = [graph[1][0] for graph in self.__graphs]
        # x = self.__graphs[0][0]
        # y = self.__graphs[0][1]
        # y = [y for y in self.__graphs[0][1]]
        # y2 = [y for y in self.__graphs[1][1] if y > 0.3e-12]
        # y3 = [y for y in self.__graphs[1][1] if y > 0.3e-12]
        # y = y1+y2+y3
        # print(y)
        # print(np.mean(y), np.std(y))
        # m,b = np.polyfit(x,y,1)
        # print(1/m,b)
        # t = np.arange(0,0.018,0.001)
        # f = m*t+b
        # ax.plot(t, f, color='black')
        # # ax.xaxis.get_children()[1].set_size(14)
        # ax.xaxis.get_children()[1].set_weight("bold")
        # ax.set_xticklabels
        # ax.axhline(y=12000,color=self.KITcolor['KITred'][3][1],linewidth=10,linestyle='-',zorder=0)
        # ax.axhline(y=8400,color=self.KITcolor['KITred'][3][1],linewidth=10,linestyle='-',zorder=0)
        # ax.axhline(y=2100,color=self.KITcolor['KITred'][3][1],linewidth=10,linestyle='-',zorder=0)
        return fig


    def setLegend(self, obj):

        # get names from cfg and lodger labels
        graphEntries = [items[1] for items in list(self.__entryDict.items())]
        # lodgerEntries = [entry.name() for entry in self.__lodgers if entry.name() != None]
        # total_len = len(self.__graphs+self.__lodgers)
        total_len = len(self.__graphs)

        # check if there are already entries for lodgers in cfg
        if len(graphEntries) == total_len:
            obj.legend(graphEntries)
        else:
            obj.legend(graphEntries+lodgerEntries)

        # reorder legend items according to 'EntryList'
        handles,labels = obj.get_legend_handles_labels()
        # handles = self.adjustOrder(handles)
        # labels = self.adjustOrder(labels)
        handles = kitutils.adjustOrder(handles, self.__entryDict, total_len)
        labels = kitutils.adjustOrder(labels, self.__entryDict, total_len)


        if self.legPosition == "auto":
            obj.legend(handles,labels)
        elif self.legPosition == "TL":
            obj.legend(handles,labels,loc='upper left')
        elif self.legPosition == "BL":
            obj.legend(handles,labels,loc='lower left')
        elif self.legPosition == "TR":
            obj.legend(handles,labels,loc='upper right')
        elif self.legPosition == "BR":
            obj.legend(handles,labels,loc='lower right')
        elif self.legPosition == "test2":
            obj.legend(handles,labels,bbox_to_anchor=(0., 1.17, 1., .102),
                       loc='upper right',ncol=3, mode="expand", borderaxespad=0.)
        elif self.legPosition == "test":
            obj.legend(handles,labels,bbox_to_anchor=(0., 0.,1.,1.),
                       loc='lower left',ncol=3, mode="expand", borderaxespad=0.)
        elif self.legPosition == "below":
            obj.legend(handles,labels,bbox_to_anchor=(0., -0.32, 1., .102),
                       loc='lower center',ncol=3, mode="expand", borderaxespad=0.)
        return True


    def getGG(self, arg):

        if arg != "off":
            # extract sub groups and convert them into list of lists
            gg = arg[1:-1].split("],[")
            try:
                gg = [list(x.split(",")) for x in gg]
                # convert items of sub lists into integers
                gg = [[int(x) for x in sub] for sub in gg]
            except:
                raise ValueError("Invalid 'GraphGroup' input.")

            # check if number of elements in gg is equal to number of graphs
            l = sum([len(x) for x in gg])

            if l > len(self.__graphs):
                raise ValueError("Number of graphs ("+str(len(self.__graphs))+
                                 ") and elements in 'GraphGroup' ("+str(l)+")"
                                 " must be equal.")
            return gg
        else:
            return arg

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
            print("Warning:::Invalid value in 'MarkerSet'. Using default instead.")
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
                color = self.colorSet[index]
                for colorDict in list(self.KITcolor.values()):
                    try:
                        return colorDict[color]
                    except:
                        pass
                raise Exception
                # for i, item in enumerate(itertools.cycle(self.colorSet)):
                #     if item not in self.colors:
                #         raise ValueError
                #     else:
                #         return item
        except:
            print("Warning:::Invalid input in 'ColorSet'. Using default instead.")
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
            print("Warning:::Invalid value in 'LineStyle'. Using default instead.")
            return self.lines[1]


    def getGraphList(self):
        return self.__graphs
