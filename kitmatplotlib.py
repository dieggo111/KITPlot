#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from .KITConfig import KITConfig
from .kitdata import KITData
from .kitlodger import KITLodger
from collections import OrderedDict
from . import kitutils
import itertools



class KITMatplotlib(object):

    def __init__(self, cfg):

        self.__graphs = []
        self.__lodgers = []

        # load style parameters from cfg file
        self.__initStyle(cfg)

        # check if there is a lodgers dict in cfg file
        try:
            cfgLodgers = KITLodger().readCfg(self.__cfg['Lodgers'])
            for obj in cfgLodgers:
                self.__lodgers.append(obj)
        except:
            pass


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

        #Line options
        self.colorPalette = cfg['Line','ColorPalette']
        self.colorSet = kitutils.extractList(cfg['Line','Color'])
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


    def addGraph(self, arg):
        """ Converts data of KITData objects or lists into a respective formate
        and writes them into .__graphs.

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
            # if i in [0,1]:
                # markerface = 'white'
            # else:
                # markerface = self.getColor(i)
            ax.plot(table[0],                           # x-axis
                    table[1],                           # y-axis
                    color=self.getColor(i),             # line color
                    marker=self.getMarker(i),           # marker style
                    markersize=self.markerSize,
                    # markerfacecolor=markerface,
                    linewidth=self.lineWidth,
                    linestyle=self.getLineStyle(i),
                    label=self.getLabel(i))

        # set error bars
        for i, table in enumerate(self.__graphs):
            if len(table) == 4:
                ax.errorbar(table[0],table[1],xerr=table[2],yerr=table[3],
                            color=self.getColor(i),
                            elinewidth=1)

        # add lodgers to party
        for lodger in self.__lodgers:
            if lodger.vline() != None:
                ax.axvline(x=lodger.vline(),color=self.getColor(lodger.color()),
                linewidth=lodger.width(),label=lodger.name())
            elif lodger.hline() != None:
                ax.axvline(y=lodger.hline(),color=self.getColor(lodger.color()),
                linewidth=lodger.width(),label=lodger.name())
            if lodger.vgraph() != None:
                ax.axvline(x=lodger.vgraph(),color=self.getColor(lodger.color()),linewidth=lodger.width(),
                label=lodger.name(),linestyle=self.lines[lodger.style()])
            elif lodger.hgraph() != None:
                ax.axvline(y=lodger.hgraph(),color=self.getColor(lodger.color()),linewidth=lodger.width(),
                label=lodger.name(),linestyle=self.lines[lodger.style()])
            elif lodger.func() != None:
                print("func", lodger.x(), lodger.y())
                # ax.plot()
            elif lodger.x() != None and lodger.y() != None:
                ax.plot(lodger.x(),lodger.y(),color=self.getColor(lodger.color()),
                linewidth=lodger.width(),linestyle=self.lines[lodger.style()],label=lodger.name())


        # set titles
        # weights = ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
        ax.set_title(self.title,
                     fontsize=self.titleFontSize,
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

        # ax.xaxis.get_children()[1].set_size(13)

        self.setLegend(ax)

        # ax.xaxis.get_children()[1].set_size(14)
        # ax.xaxis.get_children()[1].set_weight("bold")
        # ax.set_xticklabels

        return fig, len(self.__lodgers)


    def setLegend(self, obj):

        # get names from cfg and lodger labels
        graphEntries = [items[1] for items in list(self.__entryDict.items())]
        lodgerEntries = [entry.name() for entry in self.__lodgers if entry.name() != None]
        total_len = len(self.__graphs+self.__lodgers)
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
            obj.legend(handles,labels,loc='bottom left')
        elif self.legPosition == "TR":
            obj.legend(handles,labels,loc='top right')
        elif self.legPosition == "BR":
            obj.legend(handles,labels,loc='bottom right')
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


    # def adjustOrder(self, List):
    #     """ Adjusts order of list according to the changes made in 'EntryList'.
    #         This will order the legend entrys.
    #
    #         Args:
    #             List (list): list that you want to reorder (original list of
    #                          graph names)
    #     """
    #
    #     # extract desired order from 'EntryList'
    #     userOrder = [int(item[0]) for item in list(self.__entryDict.items())]
    #
    #     # adjust length of userOrder to not loose lodgers while zipping
    #     while len(userOrder)<len(self.__graphs+self.__lodgers):
    #         # appended elements must be higher then the max value to avoide doublings
    #         if len(userOrder)<max(userOrder):
    #             userOrder.append(max(userOrder)+1)
    #         else:
    #             userOrder.append(len(userOrder))
    #     # reorder the list
    #     List = [y for (x,y) in sorted(zip(userOrder, List))]
    #
    #     return List


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
                        # self.KITcolor[self.colors[0]][0][1])
                        # color = self.color_gen()
                        return color

            # if colors in 'ColorSet' are defined by strings then they dont need to be cycled
            elif all(isinstance(item, str) for item in self.colorSet) \
                        and isinstance(self.colorSet, list):
                print(self.colorSet)
                for i, item in enumerate(itertools.cycle(self.colorSet)):
                    if item not in self.colors:
                        raise ValueError
                    else:
                        return item
        except:
            print("Warning:::Invalid input in 'ColorSet'. Using default instead.")
            for i, color in enumerate(itertools.cycle(self.colors)):
                if i == index:
                    return self.KITcolor[color][0][1]

        # else:
        #     sub = [sub for sub in self.graphGroup if index in sub][0]
        #
        #     print(sub_counter)
        #     # if self.sub_current == None:
        #     # self.sub_current = sub_index
        #     shade_iter = iter(self.shade_keys)
        #
        #     color = self.color_gen(sub_index)


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


    def __initColor(self):

        mpl_std = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        self.KITcolor = OrderedDict()

        self.KITcolor = {  "KITred" :   [
                                        ("r0" , (191./255, 35./255, 41./255)),
                                        ("r1" , (205./255, 85./255, 75./255)),
                                        ("r2" , (220./255, 130./255, 110./255)),
                                        ("r3" , (230./255, 175./255, 160./255)),
                                        ("r4" , (245./255, 215./255, 200./255))
                                        ],
                           "KITgreen"  :[
                                        ("g0" ,  (0./255, 169./255, 144./255)),
                                        ("g1" ,  (75./255, 195./255, 165./255)),
                                        ("g2" ,  (125./255, 210./255, 185./255)),
                                        ("g3" ,  (180./255, 230./255, 210./255)),
                                        ("g4" ,  (215./255, 240./255, 230./255))
                                        ],
                           "KITorange": [
                                        ("o0" ,  (247./255, 145./255, 16./255)),
                                        ("o1" ,  (249./255, 174./255, 73./255)),
                                        ("o2" ,  (251./255, 195./255, 118./255)),
                                        ("o3" ,  (252./255, 218./255, 168./255)),
                                        ("o4" ,  (254./255, 236./255, 211./255))
                                        ],
                           "KITblue" :  [
                                        ("b0" ,  (67./255, 115./255, 194./255)),
                                        ("b1" ,  (120./255, 145./255, 210./255)),
                                        ("b2" ,  (155./255, 170./255, 220./255)),
                                        ("b3" ,  (195./255, 200./255, 235./255)),
                                        ("b4" ,  (225./255, 225./255, 245./255))
                                        ],
                           "KITpurple": [
                                        ("p0" ,  (188./255, 12./255, 141./255)),
                                        ("p1" ,  (205./255, 78./255, 174./255)),
                                        ("p2" ,  (218./255, 125./255, 197./255)),
                                        ("p3" ,  (232./255, 175./255, 220./255)),
                                        ("p4" ,  (243./255, 215./255, 237./255))
                                        ],
                           "KITbrown" : [
                                        ("b0" ,  (170./255, 127./255, 36./255)),
                                        ("b1" ,  (193./255, 157./255, 82./255)),
                                        ("b2" ,  (208./255, 181./255, 122./255)),
                                        ("b3" ,  (226./255, 208./255, 169./255)),
                                        ("b4" ,  (241./255, 231./255, 210./255))
                                        ],
                           "KITmay" :   [
                                        ("m0" ,  (102./255, 196./255, 48./255)),
                                        ("m1" ,  (148./255, 213./255, 98./255)),
                                        ("m2" ,  (178./255, 225./255, 137./255)),
                                        ("m3" ,  (209./255, 237./255, 180./255)),
                                        ("m4" ,  (232./255, 246./255, 217./255))
                                        ],
                          "KITcyan" :   [
                                        ("c0" , (28./255, 174./255, 236./255)),
                                        ("c1" , (95./255, 197./255, 241./255)),
                                        ("c2" , (140./255, 213./255, 245./255)),
                                        ("c3" , (186./255, 229./255, 249./255)),
                                        ("c4" , (221./255, 242./255, 252./255))
                                        ]
                    }

        if self.colorPalette == "std":
            mpl_std_sorted = [item for (i,item) in sorted(zip(self.colorSet, mpl_std))]
            # print(mpl_std_sorted)
            return mpl_std_sorted
            # return mpl_std
        elif self.colorPalette == "KIT":
            keys = list(self.KITcolor.keys())
            color_keys_ordered = [item for (i,item) in sorted(zip(self.colorSet, keys))]
            # print("color_keys_ordered", color_keys_ordered)
            # self.shade_keys = iter([0,1,2,3,4])
            return color_keys_ordered
        else:
            print("Warning:::Invalid 'ColorPalette' value. Using default")
            return mpl_std
