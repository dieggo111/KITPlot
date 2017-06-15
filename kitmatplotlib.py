#!/usr/bin/env python3
import numpy as np
try:
    import matplotlib.pyplot as plt
except:
    raise ImportError("Failed to import matplotlib.")
from .KITConfig import KITConfig
from .KITLegend import KITLegend
from .kitdata import KITData
from collections import OrderedDict


class KITMatplotlib(object):

    def __init__(self, cfg=None):

        self.__graphs = []

        if cfg == None:
            pass
        elif isinstance(cfg, KITConfig):
            try:
                self.__initStyle(cfg)
            except:
                raise ValueError("cfg-file does not look like expected.")
        else:
            raise ValueError("Unexpected argument. KITMatplotlib needs "
                             "dictionary from cfg file.")


    def __initStyle(self, cfg):
        """ Loads and sets various parameters from cfg file which are then used
            to create the desired plot.

        """

        # Title options
        self.title = cfg.get('Title','Title')
        self.titleX0 = cfg.get('Title','X0')
        self.titleY0 = cfg.get('Title','Y0')
        self.titleH = cfg.get('Title','H')
        self.titleFont = cfg.get('Title','Font')

        # Axis Options
        self.labelX = cfg.get('XAxis','Title')
        self.labelY = cfg.get('YAxis','Title')
        self.rangeX = self.extractList(cfg.get('XAxis','Range'), "float")
        self.rangeY = self.extractList(cfg.get('YAxis','Range'), "float")
        # ROOT.gStyle.SetTitleSize(cfg.get('XAxis','Size'), "X")
        # ROOT.gStyle.SetTitleSize(cfg.get('YAxis','Size'), "Y")
        # ROOT.gStyle.SetTitleOffset(cfg.get('XAxis','Offset'), "X")
        # ROOT.gStyle.SetTitleOffset(cfg.get('YAxis','Offset'), "Y")
        # ROOT.gStyle.SetTitleFont(cfg.get('XAxis','Font'), "X")
        # ROOT.gStyle.SetTitleFont(cfg.get('YAxis','Font'), "Y")
        # ROOT.gStyle.SetLabelFont(cfg.get('XAxis','Font'),"X")
        # ROOT.gStyle.SetLabelFont(cfg.get('YAxis','Font'),"Y")
        # ROOT.gStyle.SetLabelSize(cfg.get('XAxis','Size'),"X")
        # ROOT.gStyle.SetLabelSize(cfg.get('YAxis','Size'),"Y")
        # ROOT.TGaxis.SetMaxDigits(cfg.get('Canvas','MaxDigits'))

        # Canvas Options
        # ROOT.gStyle.SetPadBottomMargin(cfg.get('Canvas','PadBMargin'))
        # ROOT.gStyle.SetPadLeftMargin(cfg.get('Canvas','PadLMargin'))

        # Marker Options
        self.markerSize = cfg.get('Marker','Size')
        self.markerSet = self.extractList(cfg['Marker','Set'])

        #Line options
        self.colorSet = self.extractList(cfg['Line','Color'])
        self.lineWidth = cfg['Line','Width']
        self.lineStyle = cfg['Line','Style']

        # Pad Options
        self.grid = True
        self.gridOptions = ('w', '-', '0.5')

        # KITPlot specific options
        self.ColorShades = cfg['Misc','ColorShades']
        self.absX = cfg['XAxis','Abs']
        self.absY = cfg['YAxis','Abs']
        self.logX = cfg['XAxis','Log']
        self.logY = cfg['YAxis','Log']
        self.norm = self.extractList(cfg['Misc','Normalization'])

        # legend options
        self.entryDict = cfg['Legend','EntryList']

        # KITPlot.__init = True

        return True


    def addGraph(self, *args):
        """
        Args: x, y or KITData

        """

        x = []
        y = []
        dx = []
        dy = []
        if isinstance(args[0], KITData):
            if KITData().getRPunchDict() == None:
                # self.__files.append(args[0])
                # toggle absolute mode
                if self.absX:
                    x = list(np.absolute(args[0].getX()))
                else:
                    x = args[0].getX()
                if self.absY:
                    y = list(np.absolute(args[0].getY()))
                else:
                    y = args[0].getY()
                # get error bars if present
                if args[0].getdX() != [] and args[0].getdY() != []:
                    dx = args[0].getdX()
                    dy = args[0].getdY()
                elif args[0].getdX() == [] and args[0].getdY() == []:
                    pass
                else:
                    raise ValueError("Check data table. Only 2 (x,y) or "
                                     "4 (x,y,dx,dy) coordinates are allowed.")
            # Rpunch
            else:
                raise ValueError("Dictinary error")

        elif len(args) in [2,4] and isinstance(args[0], list):
            if self.absX:
                x = list(np.absolute(args[0]))
            else:
                x = args[0]
            if self.absY:
                y = list(np.absolute(args[1]))
            else:
                y = args[1]
            if len(args) == 4:
                dx = args[2]
                dy = args[3]

        else:
            raise ValueError("Cant add graph. Check data table. Only 2 (x,y) or"
                             "4 (x,y,dx,dy) coordinates are allowed."   )

        # create graph list
        if dx == [] and dy == []:
            self.__graphs.append([x, y])
        elif dx != [] and dy != []:
            self.__graphs.append([x, y, dx, dy])
        else:
            raise ValueError("z-error not implemented yet")

        return True


    def draw(self, fileList):
        """
        doc

        """

        # create self.__graphs list
        for i, dset in enumerate(fileList):
            self.addGraph(dset)
        # apply user defined normalization or manipulation of y values of each graph
        self.manipulate(self.__graphs)

        # apply user order
        #TODO

        # create an empty canvas
        fig = plt.figure()
        # specify (nrows, ncols, axnum)
        ax = fig.add_subplot(1, 1, 1)

        # plot graph from __.graphs: (x, y, str(color+marker), ... )
        for i, table in enumerate(self.__graphs):
            ax.plot(table[0],                           # x-axis
                    table[1],                           # y-axis
                    color=self.getColor(i),             # line color
                    marker=self.getMarker(i),           # marker style
                    markersize=self.markerSize,
                    linewidth=self.lineWidth,
                    linestyle=self.getLineStyle(i)
                    )


        # set titles
        ax.set_title(self.title)
        ax.set_xlabel(self.labelX)
        ax.set_ylabel(self.labelY)

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

        # set Legend
        ax.legend([items[1] for items in list(self.entryDict.items())])

        return fig


    def getMarker(self, index):
        """

            Args:
                index (int): represents an iterator marking a certain graph in
                             .__graphs
        """

        markers = {'s': 'square', 'v': 'triangle_down', '^': 'triangle_up',
                   '<': 'triangle_left', '>': 'triangle_right',
                   '8': 'octagon', 'p': 'pentagon', '*': 'star',
                   'h': 'hexagon1', 'H': 'hexagon2',
                   'D': 'diamond', 'd': 'thin_diamond', 'P': 'plus_filled', 'X': 'x_filled'}

        counter = self.counter_loop(self.markerSet, index)

        if isinstance(counter, int):
            return list(markers.keys())[counter]
        elif isinstance(counter, str):
            return markers[counter]
        else:
            raise ValueError("Unkown 'marker set' input.")


    def getColor(self, index):

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        # if colors in .colorset are defined by integers
        if isinstance(self.colorSet[0], int):
            counter = self.counter_loop(self.colorSet, index)
            return colors[counter]
        # if colors in .colorset are defined by strings they dont need to be looped
        elif isinstance(counter, str) and counter in colors:
            return counter
        else:
            raise ValueError("Unkown color.")


    def getLineStyle(self, index):

        lines = ['None', '-', '--', '-.', ':']

        if isinstance(self.lineStyle, int):
            return lines[self.lineStyle]
        elif isinstance(self.lineStyle, str):
            counter = self.counter_loop(self.extractList(self.lineStyle), index)
            if counter >= len(lines):
                raise ValueError("Unkown line style.")
            return lines[counter]


    def counter_loop(self, List, index):

        if index >= len(List):
            counter = List[index%len(List)]
        else:
            counter = List[index]

        return counter


    def getGraphList(self):
        return self.__graphs


    def manipulate(self, graphList):

        facList = []
        tempGraphs = graphList

        # normalization for CV plots
        if self.norm in ["1/C^{2}", "CV"]:
            for i, graph in enumerate(graphList):
                for y in graph:
                    tempList = []
                    for val in y:
                        tempList.append(1/(val*val))
                graph[1] = tempList

        # no normalization
        elif self.norm == 'off':
            pass

        # normalization via list of factors
        else:
            for fac in self.extractList(self.norm):
                facList.append(fac)
            if len(graphList) != len(facList):
                raise ValueError("Invalid normalization input! Number of "
                                 "factors differs from the number of graphs.")
            for i, graph in enumerate(graphList):
                for y in graph:
                    tempList = []
                    for val in y:
                        tempList.append(val/facList[i])
                graph[1] = tempList

        return graphList


    def extractList(self, string, output="int"):
        """ Turns a 'string(list)' into a list. Converts its elements into
            floats if possible. Real input strings are just returned as they
            are.

            Args:
                string (str): original value of respective key in cfg dict
                output (str): determines the output type of the list elements
        """

        if output not in ["int", "float"]:
            raise ValueError("Unexpected argument.")

        if string[0] == '[' and string[-1] == ']':
            if ':' in string:
                string_list = string.replace("[","").replace("]","").split(":")
            elif ',' in string:
                string_list = string.replace("[","").replace("]","").split(",")
            else:
                raise ValueError("Unkown input. Cfg parameter needs to be a"
                                 " string. Accepted seperations are ',' and "
                                 "':'. ")
            try:
                if output == "int":
                    new_list = [int(string) for string in string_list]
                elif output == "float":
                    new_list = [float(string) for string in string_list]
                return new_list
            except:
                return string_list
        else:
            return string





    def test(self, x, y):

        plot = plt.plot(x, y)
        plt.setp(plot, color='r', linewidth='2.')
        plt.show()

        return True




if __name__ == '__main__':

    x = [0,2,5,8]
    y = [1,3,4,5]
    k1 = KITMatplotlib(x,y)
    k1.test()


    input()
