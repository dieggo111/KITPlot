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

    __color = 0

    def __init__(self, input=None, cfgFile=None):

        # init colors and default values
        if self.__init == False:
            self.__initColor()            
        else:
            pass

        # load cfg if present
        if cfgFile is not None:
            if os.path.isfile(cfgFile):
                self.__initDefaultValues()
                self.__initCfg(cfgFile)
            else:
                self.__initDefaultValues()
                print "cfg not found! Use default values instead"
        else:
            self.__initDefaultValues()
            print "Use default values"

        self.__initStyle()
        self.__file = []
        self.__graphs = []

        # Load multiple data files in a folder
        if os.path.isdir(input):
            for file in os.listdir(input):
                if (os.path.splitext(filename)[1] == ".txt"):
                    with open(file) as inputFile:
                        self.__file.append(KITDataFile.KITDataFile(inputFile))
                        self.__initGraph(self.__file[i].getX(),self.__file[i].getY())
                else:
                    pass

        # Load file with multiple PIDs
        elif os.path.isfile(input):
            with open(input) as inputFile:
                for i, line in enumerate(inputFile):
                    entry = line.split()
                    if entry[0].isdigit():
                        self.__file.append(KITDataFile.KITDataFile(entry[0]))
                        self.__initGraph(self.__file[i].getX(),self.__file[i].getY())

        # Load single PID
        elif input.isdigit():
            self.__file.append(KITDataFile.KITDataFile(input))
            self.__initGraph(np.absolute(self.__file[0].getX()),np.absolute(self.__file[0].getY()))
           
        # Load KITDataFile
        elif isinstance(input, KITDataFile):
            self.__initGraph(input.getX(),input.getY())

        # TODO: Should not be part of the init method
        self.autoScaling()
        self.plotStyles("px", "py", "Title")
        self.Draw("AP")
        self.LegendParameters()
        self.setLegend()
        self.__writeCfg(cfgFile)

    def __initGraph(self, x, y):
        
        if self.AbsVal:
            self.__graphs.append(ROOT.TGraph(len(x),np.absolute(np.asarray(x)),np.absolute(np.asarray(y))))
        else:
            self.__graphs.append(ROOT.TGraph(len(x),np.asarray(x),np.asarray(y)))

        return True
        
    def __writeCfg(self, fileName):
        
        cfgPrs = ConfigParser.ConfigParser()
        
        if fileName is None:
            fileName = "plot.cfg"
        else:
            pass

        with open(fileName,'w') as cfgFile:
            cfgPrs.add_section('Global')

            cfgPrs.add_section('Title')
            cfgPrs.set('Title', 'Title', 'PlotTitle')
            cfgPrs.set('Title', 'X', self.titleX)
            cfgPrs.set('Title', 'Y', self.titleY)
            cfgPrs.set('Title', 'Height', self.titleH)

            cfgPrs.add_section('XAxis')
            cfgPrs.set('XAxis', 'TitleOffset', self.titleOffsetX)
            cfgPrs.set('XAxis', 'TitleSize', self.titleSizeX)
            cfgPrs.set('XAxis', 'Labelsize', self.labelSizeX)
            cfgPrs.set('XAxis', 'Absolute', self.absX)
            
            cfgPrs.add_section('YAxis')
            cfgPrs.set('YAxis', 'TitleOffset', self.titleOffsetY)
            cfgPrs.set('YAxis', 'TitleSize', self.titleSizeY)
            cfgPrs.set('YAxis', 'Labelsize', self.labelSizeY)
            cfgPrs.set('YAxis', 'Absolute', self.absY)

            cfgPrs.write(cfgFile)

        print "Wrote plot.cfg"

    def __initCfg(self, fileName):
        
        cfgPrs = ConfigParser.ConfigParser()

        cfgPrs.read(fileName)
            
        self.titleX = cfgPrs.getfloat('Title', 'x')
        self.titleY = cfgPrs.getfloat('Title', 'Y')
        self.titleH = cfgPrs.getfloat('Title', 'height')
        
        self.titleSizeX = cfgPrs.getfloat('XAxis', 'titleSize')
        self.titleOffsetX = cfgPrs.getfloat('XAxis', 'titleOffset')
        self.labelSizeX = cfgPrs.getfloat('XAxis', 'labelsize')
        self.absX = cfgPrs.getboolean('XAxis', 'absolute')
        
        self.titleSizeY = cfgPrs.getfloat('YAxis', 'titleSize')
        self.titleOffsetY = cfgPrs.getfloat('YAxis', 'titleOffset')
        self.labelSizeY = cfgPrs.getfloat('YAxis', 'labelsize')
        self.absY = cfgPrs.getboolean('YAxis', 'absolute')
            
                        
    def Draw(self, arg):

        self.c1 = ROOT.TCanvas("c1","c1",1280,768)
        self.c1.cd()

        for n,graph in enumerate(self.__graphs):
            if n==0:
                graph.Draw(arg)
            else:
                graph.Draw(arg.replace("A","") + "SAME")

        return True
        
    def plotStyles(self, XTitle, YTitle, Title):
    
        self.__graphs[0].GetXaxis().SetTitle(XTitle)
        self.__graphs[0].GetYaxis().SetTitle(YTitle)
        self.__graphs[0].SetTitle(Title)
        self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[1])
        self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[2],self.Scale[3])

        for graph in self.__graphs:
            graph.SetMarkerColor(self.getColor())

        return True
        
    def setColor(self):
        for graph in self.__graphs:
            graph.SetMarkerColor(self.getColor())
        return True

    def autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]

        ListX = [0]
        ListY = [0]

        for file in self.__file:
            ListX += file.getX()
            ListY += file.getY()

        if self.AbsVal:
            ListX = np.absolute(ListX)
            ListY = np.absolute(ListY)
        else:
            pass

        self.Scale = []

        self.xmax = max(ListX)
           # if min(line) < self.xmin:
        self.xmin = min(ListX)
        self.ymax = max(ListY)
           # if min(line) < self.xmin:
        self.ymin = min(ListY)
        
        self.Scale.append(self.xmin*0.9)
        self.Scale.append(self.xmax*1.1)
        self.Scale.append(self.ymin*0.9)
        self.Scale.append(self.ymax*1.1)

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
   
    def __initDefaultValues(self):
        
        # Title options 
        self.titleX = 0.5
        self.titleY = 0.97
        self.titleH = 0.05

        # XAxis
        self.titleSizeX = 0.05
        self.titleOffsetX = 1.3
        self.labelSizeX = 0.04
        self.absX = False

        # YAxis
        self.titleSizeY = 0.05
        self.titleOffsetY = 1.3
        self.labelSizeY = 0.04
        self.absY = False

        self.padBottomMargin = 0.15
        self.padLeftMargin = 0.15

        self.markerSize = 1.5
        self.markerStyle = 22
        self.markerColor = 1100


    def __initStyle(self):

        # Title options
        ROOT.gStyle.SetTitleX(self.titleX)
        ROOT.gStyle.SetTitleY(self.titleY)
        ROOT.gStyle.SetTitleH(self.titleH)

        # Axis Options
        ROOT.gStyle.SetTitleSize(self.titleSizeX,"X")
        ROOT.gStyle.SetTitleSize(self.titleSizeY,"Y")
        ROOT.gStyle.SetTitleOffset(self.titleOffsetX,"X")
        ROOT.gStyle.SetTitleOffset(self.titleOffsetY,"Y")
        
        ROOT.gStyle.SetLabelSize(self.labelSizeX,"X")
        ROOT.gStyle.SetLabelSize(self.labelSizeY,"Y")
        
        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(self.padBottomMargin)
        ROOT.gStyle.SetPadLeftMargin(self.padLeftMargin)
        
        # Marker Options
        ROOT.gStyle.SetMarkerSize(self.markerSize)
        ROOT.gStyle.SetMarkerStyle(self.markerStyle)
        ROOT.gStyle.SetMarkerColor(self.markerColor)

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
            yield int(marker)

    def getColor(self,clr=0):
        colorSet = [1100,1200,1300,1400,1500,1600,1700,1800,1900]
        KITPlot.__color += 1
        KITPlot.__color %= 9
        print KITPlot.__color
        return colorSet[KITPlot.__color]
		
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


