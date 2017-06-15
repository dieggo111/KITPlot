#!/usr/bin/env python3
import numpy as np
# try to load plot engines
try:
    import ROOT
except:
    raise ImportError("Failed to import ROOT.")
from .KITConfig import KITConfig
from .KITLegend import KITLegend
from .kitdata import KITData
from collections import OrderedDict


class KITroot(object):

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


    def __initStyle(self):
        """ Loads and sets various parameters from cfg file which are then used
            to create the desired plot.

        """

        # Title options
        ROOT.gStyle.SetTitleX(cfg.get('Title','X0'))
        ROOT.gStyle.SetTitleY(cfg.get('Title','Y0'))
        ROOT.gStyle.SetTitleH(cfg.get('Title','H'))
        ROOT.gStyle.SetTitleFont(cfg.get('Title','Font'), "")

        # Axis Options
        ROOT.gStyle.SetTitleSize(cfg.get('XAxis','Size'), "X")
        ROOT.gStyle.SetTitleSize(cfg.get('YAxis','Size'), "Y")
        ROOT.gStyle.SetTitleOffset(cfg.get('XAxis','Offset'), "X")
        ROOT.gStyle.SetTitleOffset(cfg.get('YAxis','Offset'), "Y")
        ROOT.gStyle.SetTitleFont(cfg.get('XAxis','Font'), "X")
        ROOT.gStyle.SetTitleFont(cfg.get('YAxis','Font'), "Y")
        ROOT.gStyle.SetLabelFont(cfg.get('XAxis','Font'),"X")
        ROOT.gStyle.SetLabelFont(cfg.get('YAxis','Font'),"Y")
        ROOT.gStyle.SetLabelSize(cfg.get('XAxis','Size'),"X")
        ROOT.gStyle.SetLabelSize(cfg.get('YAxis','Size'),"Y")
        ROOT.TGaxis.SetMaxDigits(cfg.get('Canvas','MaxDigits'))

        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(cfg.get('Canvas','PadBMargin'))
        ROOT.gStyle.SetPadLeftMargin(cfg.get('Canvas','PadLMargin'))

        # Marker Options
        ROOT.gStyle.SetMarkerSize(cfg.get('Marker','Size'))
        self.markerSet = self.extractList(cfg['Marker','Set'])

        #Line options
        self.colorSet = self.extractList(cfg['Line','Color'])
        self.lineWidth = cfg['Line','Width']
        self.lineStyle = cfg['Line','Style']

        # Pad Options
        ROOT.gStyle.SetPadGridX(True)
        ROOT.gStyle.SetPadGridY(True)
        ROOT.gStyle.SetGridColor(17)

        # KITPlot specific options
        self.ColorShades = cfg['Misc','ColorShades']
        self.absX = cfg['XAxis','Abs']
        self.absY = cfg['YAxis','Abs']
        self.logX = cfg['XAxis','Log']
        self.logY = cfg['YAxis','Log']
        self.norm = self.extractList(cfg['Misc','Normalization'])



        KITPlot.__init = True

        return True


    def addGraph(self, fileList):
        """ The KITData objects within the 'self.__files' list (containing
        the data tables) are now converted into ROOT objects. A ROOT object
        represents a single graph of the future plot. These ROOT objects are
        stored within the 'self.__graphs' list.

        Args: x, y or KITData

        """
        # TODO
        # args: x, y or KITData

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

        elif len(args) == 2 and not isinstance(args[0], KITData):

            if self.absX:
                x = np.absolute(args[0])
            else:
                x = args[0]

            if self.absY:
                y = np.absolute(args[1])
            else:
                y = args[1]

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
            sys.exit("Cant add graph")

        if len(args) == 2:
            self.__graphs.append(ROOT.TGraph(len(x),np.asarray(x),np.asarray(y)))
        elif len(args) == 4:
            self.__graphs.append(ROOT.TGraphErrors(len(x),np.asarray(x),np.asarray(y),np.asarray(dx),np.asarray(dy)))

        return True


    def draw(self, arg=None):
        """ Finally, a canvas needs to be created and all the ROOT objects
        within 'self.__graphs' need to be drawn. Different plot styles are set
        in respect of the cfg file and as a last step the legend is created and
        drawn on the canvas.

        Args:
            arg(str): This is a ROOT specific argument (TGraph  Draw):
                'A' -> draw axis
                'L' -> draw lines
                'P' -> draw markers
                'C' -> draw smooth curve
                See ROOT documentation for more details.

        """

        if arg == None:
            arg = "APL"
        else:
            pass

        #TODO if 0 -> no line
        # if cfg.get('Line','NoLine') == True and "L" in arg:
        #     arg = arg.replace("L","")
        # elif cfg.get('Line','NoLine') == False and "L" not in arg:
        #     arg = arg + "L"
        # else:
        #     pass

        if len(self.__graphs) == 0:
            print("No graphs to draw")
            return False

        # init canvas
        self.canvas = ROOT.TCanvas("c1","c1",
                                   int(cfg.get('Canvas','SizeX')),
                                   int(cfg.get('Canvas','SizeY')))
        self.canvas.cd()

        # apply plot styles
        self.plotStyles(cfg.get('XAxis','Title'),
                        cfg.get('YAxis','Title'),
                        cfg.get('Title','Title'))

        # set log scale if
        if self.logX:
            self.canvas.SetLogx()
        if self.logY:
            self.canvas.SetLogy()

        # Draw plots
        for n,graph in enumerate(self.__graphs):
            if n==0:
                graph.Draw(arg)
            else:
                graph.Draw(arg.replace("A","") + "SAME")

        # Set legend (always at the very end!)

        # LegH = LegHandler()
        # LegH.setKITLegend(cfg.get('Legend'),
        #                   self.__graphs,
        #                   self.__files,
        #                   cfg.get('Canvas','SizeX'),
        #                   cfg.get('Canvas','SizeY'),
        #                   self.Scale)
        # self.leg = LegH.getLegend()
        # # self.leg.SetHeader("n-in-p FZ, 240#mum")
        self.leg.Draw()
        self.canvas.Update()

        self.saveAs(self.cfgPath.replace("cfg/","").replace(".cfg",""))


        return True




    def __initColor(self):

        self.__kitGreen.append(ROOT.TColor(1100, 0./255, 169./255, 144./255))
        self.__kitGreen.append(ROOT.TColor(1101,75./255, 195./255, 165./255))
        self.__kitGreen.append(ROOT.TColor(1102,125./255, 210./255, 185./255))
        self.__kitGreen.append(ROOT.TColor(1103,180./255, 230./255, 210./255))
        self.__kitGreen.append(ROOT.TColor(1104,215./255, 240./255, 230./255))

        self.__kitRed.append(ROOT.TColor(1200, 191./255, 35./255, 41./255))
        self.__kitRed.append(ROOT.TColor(1201, 205./255, 85./255, 75./255))
        self.__kitRed.append(ROOT.TColor(1202, 220./255, 130./255, 110./255))
        self.__kitRed.append(ROOT.TColor(1203, 230./255, 175./255, 160./255))
        self.__kitRed.append(ROOT.TColor(1204, 245./255, 215./255, 200./255))

        self.__kitOrange.append(ROOT.TColor(1300, 247./255, 145./255, 16./255))
        self.__kitOrange.append(ROOT.TColor(1301, 249./255, 174./255, 73./255))
        self.__kitOrange.append(ROOT.TColor(1302, 251./255, 195./255, 118./255))
        self.__kitOrange.append(ROOT.TColor(1303, 252./255, 218./255, 168./255))
        self.__kitOrange.append(ROOT.TColor(1304, 254./255, 236./255, 211./255))

        self.__kitBlue.append(ROOT.TColor(1400, 67./255, 115./255, 194./255))
        self.__kitBlue.append(ROOT.TColor(1401, 120./255, 145./255, 210./255))
        self.__kitBlue.append(ROOT.TColor(1402, 155./255, 170./255, 220./255))
        self.__kitBlue.append(ROOT.TColor(1403, 195./255, 200./255, 235./255))
        self.__kitBlue.append(ROOT.TColor(1404, 225./255, 225./255, 245./255))

        self.__kitPurple.append(ROOT.TColor(1500, 188./255, 12./255, 141./255))
        self.__kitPurple.append(ROOT.TColor(1501, 205./255, 78./255, 174./255))
        self.__kitPurple.append(ROOT.TColor(1502, 218./255, 125./255, 197./255))
        self.__kitPurple.append(ROOT.TColor(1503, 232./255, 175./255, 220./255))
        self.__kitPurple.append(ROOT.TColor(1504, 243./255, 215./255, 237./255))

        self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))
        self.__kitBrown.append(ROOT.TColor(1601, 193./255, 157./255, 82./255))
        self.__kitBrown.append(ROOT.TColor(1602, 208./255, 181./255, 122./255))
        self.__kitBrown.append(ROOT.TColor(1603, 226./255, 208./255, 169./255))
        self.__kitBrown.append(ROOT.TColor(1604, 241./255, 231./255, 210./255))

        self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))
        self.__kitMay.append(ROOT.TColor(1701, 148./255, 213./255, 98./255))
        self.__kitMay.append(ROOT.TColor(1702, 178./255, 225./255, 137./255))
        self.__kitMay.append(ROOT.TColor(1703, 209./255, 237./255, 180./255))
        self.__kitMay.append(ROOT.TColor(1704, 232./255, 246./255, 217./255))

        self.__kitCyan.append(ROOT.TColor(1800, 28./255, 174./255, 236./255))
        self.__kitCyan.append(ROOT.TColor(1801, 95./255, 197./255, 241./255))
        self.__kitCyan.append(ROOT.TColor(1802, 140./255, 213./255, 245./255))
        self.__kitCyan.append(ROOT.TColor(1803, 186./255, 229./255, 249./255))
        self.__kitCyan.append(ROOT.TColor(1804, 221./255, 242./255, 252./255))

        # yellow removed because it looks shitty

        KITPlot.__init = True

        return True


    def getColor(self, index):

        KITPlot.__color = index + 1
        KITPlot.__color %= 8

        return int(self.colorSet[KITPlot.__color-1])


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


if __name__ == '__main__':

    KITroot().test()


    input()
