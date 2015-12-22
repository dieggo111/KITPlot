import numpy as np
import ROOT
import os
import ConfigParser
import KITDataFile

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
    AbsVal = True

    def __init__(self, input=None, cfgFile=None):
     
        if self.__init == False:
            self.__initStyle()
            self.__initColor()
        else:
            pass
        
        self.__file = []

        if os.path.isdir(input):
            for file in os.listdir(input):
                if (os.path.splitext(filename)[1] == ".txt"):
                    with open(file) as inputFile:
                        self.__file.append(KITDataFile.KITDataFile(inputFile))
                        self.__initGraph(self.__file[i].getX(),self.__file[i].getY())
                else:
                    pass

        elif os.path.isfile(input):
            with open(input) as inputFile:
                for i, line in enumerate(inputFile):
                    entry = line.split()
                    if entry[0].isdigit():
                        self.__file.append(KITDataFile.KITDataFile(entry))
                        self.__initGraph(self.__file[i].getX(),self.__file[i].getY())

        elif input.isdigit():
            self.__file.append(KITDataFile.KITDataFile(input))
            self.__initGraph(np.absolute(self.__file[0].getX()),np.absolute(self.__file[0].getY()))
           
        elif isinstance(input, KITDataFile):
            self.__initGraph(input.getX(),input.getY())
      
        self.Draw("AP")
        self.autoScaling()
        self.plotStyles("px", "py", "Title")
        self.LegendParameters()
        self.setLegend()
        
    def __initGraph(self, x, y):
        
        self.__graphs = []
        self.__graphs.append(ROOT.TGraph(len(x),np.asarray(x),np.asarray(y)))
            
        return True
        
        
    def Draw(self, arg):

        self.c1 = ROOT.TCanvas("c1","c1",1280,768)
        self.c1.cd()
        
        for graph in self.__graphs:
            graph.Draw(arg)
        
        return True
        
    def plotStyles(self, XTitle, YTitle, Title):
    
        self.__graphs[0].GetXaxis().SetTitle(XTitle)
        self.__graphs[0].GetYaxis().SetTitle(YTitle)
        self.__graphs[0].SetTitle(Title)
        self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[1])
        self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[2],self.Scale[3])

        return True
        
        
    def autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]
        #self.xmax = 0
        #self.xmin = 0
        #self.ymax = 0
        #self.ymin = 0
        if self.AbsVal == True:
            ListX=np.absolute(self.__file[0].getX())
            ListY=np.absolute(self.__file[0].getY())
        else:
            ListX=self.__file[0].getX()
            ListY=self.__file[0].getY()   
        self.Scale = []
        #for graph in graphs:
            #if max(line) > self.xmax:
        self.xmax = max(ListX)
           # if min(line) < self.xmin:
        self.xmin = min(ListX)
        self.ymax = max(ListY)
           # if min(line) < self.xmin:
        self.ymin = min(ListY)
        
        self.Scale.append(self.xmin)
        self.Scale.append(self.xmax)
        self.Scale.append(self.ymin)
        self.Scale.append(self.ymax)

        return True
        
        
    def setLegend(self):
    
        self.c1.Update()
        self.legend = ROOT.TLegend(self.LParaX,self.LParaY,0.95,0.95)
        self.legend.SetFillColor(0)
        self.legend.SetTextSize(.02)
        for i,graph in enumerate(self.__graphs):
            self.legend.AddEntry(self.__graphs[i], self.__file[0].getName(), "p")
        self.legend.Draw()
        
        
    def LegendParameters(self):
        
        para=0
        if len(self.__file[0].getName())>para:
            para=len(self.__file[0].getName())
        self.LParaX = (1-1.3*para/100.)
        self.LParaY = (1-12*len(self.__graphs)/100.)
   
   
    def __initStyle(self):

        # Title Options
        ROOT.gStyle.SetTitleX(0.5)
        ROOT.gStyle.SetTitleY(0.97)
        ROOT.gStyle.SetTitleH(0.05)

        # Axis Options
        ROOT.gStyle.SetTitleSize(0.05,"X")
        ROOT.gStyle.SetTitleSize(0.05,"Y")
        ROOT.gStyle.SetTitleOffset(1.3,"X")
        ROOT.gStyle.SetTitleOffset(1.3,"Y")
        
        ROOT.gStyle.SetLabelSize(0.04,"X")
        ROOT.gStyle.SetLabelSize(0.04,"Y")
        
        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(0.15)
        ROOT.gStyle.SetPadLeftMargin(0.15)
        
        # Marker Options
        ROOT.gStyle.SetMarkerSize(1.5)
        ROOT.gStyle.SetMarkerStyle(22)

        # Pad Options
        ROOT.gStyle.SetPadGridX(True)
        ROOT.gStyle.SetPadGridY(True)

        KITPlot.__init = True
        return True

    def setAxisTitleSize(self, size):

        ROOT.gStyle.SetTitleSize(size,"X")
        ROOT.gStyle.SetTitleSize(size,"Y")
        
        return True


    def setAxisTitleOffset(self, offset):

        ROOT.gStyle.SetTitleOffset(offset,"X")
        ROOT.gStyle.SetTitleOffset(offset,"Y")

        return True


    def getGraph(graph=None):
        
        if len(self.__graphs) == 1:
            return self.__graphs[0]
        elif (len(self.__graphs) != 1) & (graph is None):
            return self._graphs
        elif (len(self.__graphs) != 1) & (graph.isdigit()):
            return self.__graphs[graph]
        else:
            return False

    def getMarkerStyle(self):
        markerSet = [5,4,2,3,20,21,22,23,24,25,26]
        for marker in markerSet:
            yield marker
		
		
    def __initColor(self):

        self.__kitGreen.append(ROOT.TColor(1100, 0./255, 169./255, 144./255))
        self.__kitGreen.append(ROOT.TColor(1101,75./255, 195./255, 165./255))
        self.__kitGreen.append(ROOT.TColor(1102,125./255, 210./255, 185./255))
        self.__kitGreen.append(ROOT.TColor(1103,180./255, 230./255, 210./255))
        self.__kitGreen.append(ROOT.TColor(1104,215./255, 240./255, 230./255))

        self.__kitBlue.append(ROOT.TColor(1200, 67./255, 115./255, 194./255))
        self.__kitBlue.append(ROOT.TColor(1201, 120./255, 145./255, 210./255))
        self.__kitBlue.append(ROOT.TColor(1202, 155./255, 170./255, 220./255))
        self.__kitBlue.append(ROOT.TColor(1203, 195./255, 200./255, 235./255))
        self.__kitBlue.append(ROOT.TColor(1204, 225./255, 225./255, 245./255))

        self.__kitMay.append(ROOT.TColor(1300, 102./255, 196./255, 48./255))

        self.__kitYellow.append(ROOT.TColor(1400, 254./255, 231./255, 2./255))

        self.__kitOrange.append(ROOT.TColor(1500, 247./255, 145./255, 16./255))

        self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))

        self.__kitRed.append(ROOT.TColor(1700, 191./255, 35./255, 41./255))
        self.__kitRed.append(ROOT.TColor(1701, 205./255, 85./255, 75./255))
        self.__kitRed.append(ROOT.TColor(1702, 220./255, 130./255, 110./255))
        self.__kitRed.append(ROOT.TColor(1703, 230./255, 175./255, 160./255))
        self.__kitRed.append(ROOT.TColor(1704, 245./255, 215./255, 200./255))

        self.__kitPurple.append(ROOT.TColor(1800, 188./255, 12./255, 141./255))

        self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))

        KITPlot.__init = True
        return True


