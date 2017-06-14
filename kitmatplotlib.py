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

        # process additional graph that is not in self.__files?
        if isinstance(args[0], KITData):
            if KITData.getRPunchDict() == None:
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
                raise ValueError("Dictinary error")

        # process data from self.__files
        elif len(args) == 2 and not isinstance(args[0], KITData):

            if self.absX:
                x = np.absolute(args[0])
            else:
                x = args[0]

            if self.absY:
                y = np.absolute(args[1])
            else:
                y = args[1]

        # process data from self.__files + error bars
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
            raise ValueError("Cant add graph")

        # create graph list
        if len(args) == 2:
            self.__graphs.append((np.asarray(x),np.asarray(y)))
        elif len(args) == 4:
            self.__graphs.append((np.asarray(x),np.asarray(y),np.asarray(dx),np.asarray(dy)))

        return True


    def draw(self, fileList):
        """
        doc

        """


        # create an empty canvas
        fig = plt.figure()
        # specify (nrows, ncols, axnum)
        ax = fig.add_subplot(1, 1, 1)

        for dtup in self.__graphs:
            ax.plot(dtup[0], dtup[1])


        display(fig)  # this is required to re-display the figure

        return True


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
