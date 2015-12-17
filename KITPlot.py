#import numpy as np
import ROOT

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

    def __init__(self, plot=None, x=[], y=[]):
        
        print self.__init

        if self.__init == False:
            print "Initialize style and colors"
            self.__initStyle()
            self.__initColor()
        else:
            print "style and colors already initialized"

        #if plot == "TGraph":
        #    self.__graph = ROOT.TGraph(len(x), np.asarray(x),np.asarray(y))
        #else:
        #    pass
            

    def __initStyle(self):

        # Title Options
        ROOT.gStyle.SetTitleX(0.5)
        ROOT.gStyle.SetTitleY(0.97)
        ROOT.gStyle.SetTitleH(0.05)
        
        # Axis Options
        ROOT.gStyle.SetTitleSize(0.05,"X")
        ROOT.gStyle.SetTitleSize(0.05,"Y")
        ROOT.gStyle.SetTitleOffset(1.3,"X")
        ROOT.gStyle.SetTitleOffset(1.2,"Y")
        
        ROOT.gStyle.SetLabelSize(0.04,"X")
        ROOT.gStyle.SetLabelSize(0.04,"Y")
        
        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(0.15)
        ROOT.gStyle.SetPadLeftMargin(0.15)
        
        # Legend Options
        ROOT.gStyle.SetLegendTextSize(0.035)
        
        # Marker Options
        ROOT.gStyle.SetMarkerSize(1.5)
        ROOT.gStyle.SetMarkerStyle(22)

        # Pad Options
        ROOT.gStyle.SetPadGridX(True)
        ROOT.gStyle.SetPadGridY(True)

        itPlot.__init = True

        return True

    def __initColor(self):

        #self.__kitGreen.append(ROOT.TColor(1100, 0./255, 150./255, 130./255))
        self.__kitGreen.append(ROOT.TColor(1100, 0./255, 169./255, 144./255))
        self.__kitGreen.append(ROOT.TColor(1101,75./255, 195./255, 165./255))
        self.__kitGreen.append(ROOT.TColor(1102,125./255, 210./255, 185./255))
        self.__kitGreen.append(ROOT.TColor(1103,180./255, 230./255, 210./255))
        self.__kitGreen.append(ROOT.TColor(1104,215./255, 240./255, 230./255))

        #self.__kitBlue.append(ROOT.TColor(1200, 70./255, 100./255, 170./255))
        self.__kitBlue.append(ROOT.TColor(1200, 67./255, 115./255, 194./255))
        self.__kitBlue.append(ROOT.TColor(1201, 120./255, 145./255, 210./255))
        self.__kitBlue.append(ROOT.TColor(1202, 155./255, 170./255, 220./255))
        self.__kitBlue.append(ROOT.TColor(1203, 195./255, 200./255, 235./255))
        self.__kitBlue.append(ROOT.TColor(1204, 225./255, 225./255, 245./255))

        #self.__kitMay.append(ROOT.TColor(1300, 140./255, 182./255, 60./255))
        self.__kitMay.append(ROOT.TColor(1300, 102./255, 196./255, 48./255))

        #self.__kitYellow.append(ROOT.TColor(1400, 252./255, 229./255, 0./255))
        self.__kitYellow.append(ROOT.TColor(1400, 254./255, 231./255, 2./255))

        #self.__kitOrange.append(ROOT.TColor(1500, 223./255, 155./255, 27./255))
        self.__kitOrange.append(ROOT.TColor(1500, 247./255, 145./255, 16./255))

        #self.__kitBrown.append(ROOT.TColor(1600, 167./255, 130./255, 46./255))
        self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))

        #self.__kitRed.append(ROOT.TColor(1700, 162./255, 34./255, 35./255))
        self.__kitRed.append(ROOT.TColor(1700, 191./255, 35./255, 41./255))
        self.__kitRed.append(ROOT.TColor(1701, 205./255, 85./255, 75./255))
        self.__kitRed.append(ROOT.TColor(1702, 220./255, 130./255, 110./255))
        self.__kitRed.append(ROOT.TColor(1703, 230./255, 175./255, 160./255))
        self.__kitRed.append(ROOT.TColor(1704, 245./255, 215./255, 200./255))
        
        #self.__kitPurple.append(ROOT.TColor(1800, 163./255, 16./255, 124./255))
        self.__kitPurple.append(ROOT.TColor(1800, 188./255, 12./255, 141./255))

        #self.__kitCyan.append(ROOT.TColor(1900, 35./255, 161./255, 224./255))
        self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))

        self.__init = True

        return True

    def setAxisTitleSize(self, size):

        ROOT.gStyle.SetTitleSize(size,"X")
        ROOT.gStyle.SetTitleSize(size,"Y")
        
        return True

    def setAxisTitleOffset(self, offset):

        ROOT.gStyle.SetTitleOffset(offset,"X")
        ROOT.gStyle.SetTitleOffset(offset,"Y")

        return True

    def Draw(self, argument):
        self.__graph.Draw(argument)
        
        return True

    def getGraph():
        return self._graph


    def getMarkerStyle(self):
        markerSet = [5,4,2,3,20,21,22,23,24,25,26,]
        for marker in markerSet:
            yield marker

    
