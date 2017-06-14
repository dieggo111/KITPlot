import numpy as np
# try to load plot engines
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
            print("Use default cfg")
        elif isinstance(cfg, KITConfig):
            # try:
            self.__initStyle(cfg)
            # except:
                # raise ValueError("cfg-file does not look like expected.")
        else:
            raise ValueError("Unexpected argument. KITMatplotlib needs "
                             "dictionary from cfg file.")


    def __initStyle(self, cfg):
        """ Loads and sets various parameters from cfg file which are then used
            to create the desired plot.

        """

        # Title options
        # ROOT.gStyle.SetTitleX(cfg.get('Title','X0')
        # ROOT.gStyle.SetTitleY(cfg.get('Title','Y0'))
        # ROOT.gStyle.SetTitleH(cfg.get('Title','H'))
        # ROOT.gStyle.SetTitleFont(cfg.get('Title','Font'), "")

        # Axis Options
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
        # ROOT.gStyle.SetMarkerSize(cfg.get('Marker','Size'))
        self.markerSet = self.extractList(cfg['Marker','Set'])

        #Line options
        self.noLine = cfg['Line','NoLine']
        self.colorSet = self.extractList(cfg['Line','Color'])
        self.lineWidth = cfg['Line','Width']
        self.lineStyle = cfg['Line','Style']

        # Pad Options
        # ROOT.gStyle.SetPadGridX(True)
        # ROOT.gStyle.SetPadGridY(True)
        # ROOT.gStyle.SetGridColor(17)

        # KITPlot specific options
        self.ColorShades = cfg['Misc','ColorShades']
        self.absX = cfg['XAxis','Abs']
        self.absY = cfg['YAxis','Abs']
        self.logX = cfg['XAxis','Log']
        self.logY = cfg['YAxis','Log']
        self.norm = self.extractList(cfg['Misc','Normalization'])


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
        # print("args", args[0], type(args[0]))
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
            self.__graphs.append((x, y))
        elif dx != [] and dy != []:
            self.__graphs.append((x, y, dx, dy))
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

        for dtup in self.__graphs:
            print(dtup)
            ax.plot(dtup[0], dtup[1])

        # this is required to re-display the figure
        fig.show()

        return True


    def getGraphList(self):
        return self.__graphs


    def manipulate(self, graphList):

        facList = []
        tempGraphs = graphList

        # normalization for CV plots
        if self.norm == "1/C^{2}":
            for graph in graphList:
                for y in graph[1]:
                    tempList = []
                    for val in y:
                        tempList.append(1/(val*val))
                    y = tempList

        # no normalization
        elif self.norm == 'off':
            pass

        # normalization via list of factors
        else:
            for fac in self.extractList(self.norm):
                facList.append(float(fac))

            if len(self.__files) != len(FacList):
                raise ValueError("Invalid normalization input! Number of "
                                 "factors differs from the number of graphs.")
            for i, graph in enumerate(graphList):
                for y in graph:
                    tempList = []
                    for val in y:
                        tempList.append(val/facList[i])
                    y = tempList

        return graphList


    def extractList(self, string):

        if string[0] == '[' and string[-1] == ']':
            return string.replace("[","").replace("]","").split(",")
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
