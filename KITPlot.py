import numpy as np
import ROOT
import os, sys
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
    __color = 0

    def __init__(self, input=None, cfgFile=None):

        # init colors
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


        # Load KITDataFile
        if isinstance(input, KITDataFile.KITDataFile):
            self.__file.append(input)
            self.addGraph(input.getX(),input.getY())

        # Load single PID
        elif isinstance(input, int):
            self.__file.append(KITDataFile.KITDataFile(input))
            self.addGraph(self.__file[0].getX(), self.__file[0].getY())
          
        elif isinstance(input, str):

            # Load single PID
            if input.isdigit():
                self.__file.append(KITDataFile.KITDataFile(input))
                self.addGraph(self.__file[0].getX(), self.__file[0].getY())
            
            # Load multiple data files in a folder
            elif os.path.isdir(input):
                for file in os.listdir(input):
                    if (os.path.splitext(file)[1] == ".txt"):
                        with open(file) as inputFile:
                            self.__file.append(KITDataFile.KITDataFile(inputFile))
                            self.addGraph(self.__file[i].getX(),self.__file[i].getY())
                    else:
                        pass

            # Load file with multiple PIDs
            elif os.path.isfile(input):
                with open(input) as inputFile:
                    for i, line in enumerate(inputFile):
                        entry = line.split()
                        if entry[0].isdigit():
                            self.__file.append(KITDataFile.KITDataFile(entry[0]))
                            self.addGraph(self.__file[i].getX(),self.__file[i].getY())

      

        self.__writeCfg(cfgFile)

######################
### Default values ###
######################
     
    def __initDefaultValues(self):
        
        # Title options 
        self.title = "Plot"
        self.titleX0 = 0.5
        self.titleY0 = 0.97
        self.titleH = 0.05

        # XAxis
        self.titleX = "px"
        self.titleSizeX = 0.05
        self.titleOffsetX = 1.1
        self.labelSizeX = 0.04
        self.absX = True
        self.logX = False

        # YAxis
        self.titleY = "py"
        self.titleSizeY = 0.05
        self.titleOffsetY = 1.1
        self.labelSizeY = 0.04
        self.absY = True
        self.logY = False

        # Legend
        self.legendEntry = "name" # name / id

        self.padBottomMargin = 0.15
        self.padLeftMargin = 0.15

        self.markerSize = 1.5
        self.markerStyle = 22
        self.markerColor = 1100
        
        self.TopRight = True
        self.TopLeft = False
        self.BottomRight = False
        
        
###################
### cfg methods ###
###################


    def __initCfg(self, fileName):
        
        cfgPrs = ConfigParser.ConfigParser()

        cfgPrs.read(fileName)
            
        self.titleX0 = cfgPrs.getfloat('Title', 'x0')
        self.titleY0 = cfgPrs.getfloat('Title', 'Y0')
        self.titleH = cfgPrs.getfloat('Title', 'height')

        self.titleX = cfgPrs.get('XAxis', 'title')
        self.titleSizeX = cfgPrs.getfloat('XAxis', 'titleSize')
        self.titleOffsetX = cfgPrs.getfloat('XAxis', 'titleOffset')
        self.labelSizeX = cfgPrs.getfloat('XAxis', 'labelsize')
        self.absX = cfgPrs.getboolean('XAxis', 'absolute')
        self.logX = cfgPrs.getboolean('XAxis', 'log')

        self.titleY = cfgPrs.get('YAxis', 'title')
        self.titleSizeY = cfgPrs.getfloat('YAxis', 'titleSize')
        self.titleOffsetY = cfgPrs.getfloat('YAxis', 'titleOffset')
        self.labelSizeY = cfgPrs.getfloat('YAxis', 'labelsize')
        self.absY = cfgPrs.getboolean('YAxis', 'absolute')
        self.logY = cfgPrs.getboolean('YAxis', 'log')

        self.legendEntry = cfgPrs.get('Legend', 'entry')
        

    def __writeCfg(self, fileName):
        
        cfgPrs = ConfigParser.ConfigParser()

        if not os.path.exists("cfg"):
            os.makedirs("cfg")
        
        if fileName is None:
            if self.__file[0].getID() is not None:
                fileName = ("cfg/%s.cfg" %(self.__file[0].getID()))
            else:
                fileName = "cfg/plot.cfg"
        else:
            pass

        with open(fileName,'w') as cfgFile:
            cfgPrs.add_section('Global')

            cfgPrs.add_section('Title')
            cfgPrs.set('Title', 'Title', self.title)
            cfgPrs.set('Title', 'X0', self.titleX0)
            cfgPrs.set('Title', 'Y0', self.titleY0)
            cfgPrs.set('Title', 'Height', self.titleH)

            cfgPrs.add_section('XAxis')
            cfgPrs.set('XAxis', 'Title', self.titleX)
            cfgPrs.set('XAxis', 'TitleOffset', self.titleOffsetX)
            cfgPrs.set('XAxis', 'TitleSize', self.titleSizeX)
            cfgPrs.set('XAxis', 'Labelsize', self.labelSizeX)
            cfgPrs.set('XAxis', 'Absolute', self.absX)
            cfgPrs.set('XAxis', 'Log', self.logX)

            cfgPrs.add_section('YAxis')
            cfgPrs.set('YAxis', 'Title', self.titleY)
            cfgPrs.set('YAxis', 'TitleOffset', self.titleOffsetY)
            cfgPrs.set('YAxis', 'TitleSize', self.titleSizeY)
            cfgPrs.set('YAxis', 'Labelsize', self.labelSizeY)
            cfgPrs.set('YAxis', 'Absolute', self.absY)
            cfgPrs.set('YAxis', 'Log', self.logY)

            cfgPrs.add_section('Legend')
            cfgPrs.set('Legend', 'Entry', self.legendEntry)
            
            cfgPrs.write(cfgFile)

        print ("Wrote %s" %(fileName))
        

#########################
### Measurement Types ###
#########################

    def MeasurementType(self):
    
        self.MT = self.__file[0].getParaY()
        if self.MT == "I_tot":
            self.title = "Current Voltage characteristics" 
            self.titleY = "Current (A)"
            self.titleX = "Voltage (V)"
        if self.MT == "Pinhole":
            self.title = "Pinhole leakage" 
            self.titleY = "Current (A)"
            self.titleX = "Voltage (V)"
        if self.MT == "I_leak_dc":
            self.title = "Interstrip current leakage" 
            self.titleY = "Current (A)"
            self.titleX = "Voltage (V)"
        if self.MT == "C_tot":
            self.title = "Capacitance Voltage characteristics" 
            self.titleY = "Capacitance (F)"
            self.titleX = "Voltage (V)"
        if self.MT == "C_int":
            self.title = "Interstrip capacitance measurement" 
            self.titleY = "Capacitance (F)"
            self.titleX = "Voltage (V)"
        if self.MT == "CC":
            self.title = "Coupling capacitance measurement" 
            self.titleY = "Capacitance (F)"
            self.titleX = "Voltage (V)"
        if self.MT == "R_int":
            self.title = "Interstrip resistance measurement" 
            self.titleY = "Resistance (#Omega)"
            self.titleX = "Voltage (V)"
        if self.MT == "R_poly":
            self.title = "Strip resistance measurement" 
            self.titleY = "Resistance (#Omega)"
            self.titleX = "Voltage (V)"
            
        if len(self.__file) >= 2:
            if self.__file[0].getParaY() != self.__file[1].getParaY():
                sys.exit("Measurement types are not equal!")




#####################
### Graph methods ###
#####################

    
    def __initStyle(self):

        # Title options
        ROOT.gStyle.SetTitleX(self.titleX0)
        ROOT.gStyle.SetTitleY(self.titleY0)
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


    def addGraph(self, x, y):
        
        if self.absX:
            x = np.absolute(x)
            
        if self.absY:
            y = np.absolute(y)
        
        self.__graphs.append(ROOT.TGraph(len(x),np.asarray(x),np.asarray(y)))

        return True
            
                        
    def Draw(self, arg="AP"):

        self.canvas = ROOT.TCanvas("c1","c1",1280,768)
        self.canvas.cd()

        self.__autoScaling()
        self.MeasurementType()
        self.plotStyles(self.titleX, self.titleY, self.title)

        if self.logX:
            self.canvas.SetLogx()
        if self.logY:
            self.canvas.SetLogy()

        for n,graph in enumerate(self.__graphs):
            if n==0:
                graph.Draw(arg)
            else:
                graph.Draw(arg.replace("A","") + "SAME")
        
        self.setLegendParameters()
        self.setLegend()

        self.canvas.Update()

        return True

    def update(self):
        
        try:
            self.canvas.Update()
        except:
            pass
        

    def plotStyles(self, XTitle, YTitle, Title):
    
        self.__graphs[0].GetXaxis().SetTitle(XTitle)
        self.__graphs[0].GetYaxis().SetTitle(YTitle)
        self.__graphs[0].SetTitle(Title)
        self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[1])
        self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[2],self.Scale[3])

        self.counter = 0
        
        for i, graph in enumerate(self.__graphs):
            graph.SetMarkerColor(self.getColor())
            graph.SetMarkerStyle(self.getMarkerStyle(i))

        return True
        

#######################
### Automatizations ###
#######################

    def __autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]

        self.perc = 0.05
        ListX = [0]
        ListY = [0]

        for file in self.__file:
            ListX += file.getX()
            ListY += file.getY()

        if self.absX:
            ListX = np.absolute(ListX)
            
        if self.absY:
            ListY = np.absolute(ListY)
        
        self.Scale = []

        self.xmax = max(ListX)
           # if min(line) < self.xmin:
        self.xmin = min(ListX)
        self.ymax = max(ListY)
           # if min(line) < self.xmin:
        self.ymin = min(ListY)
        
        self.Scale.append(self.xmin*(1.-self.perc))
        self.Scale.append(self.xmax*(1.+self.perc))
        self.Scale.append(self.ymin*(1.-self.perc))
        self.Scale.append(self.ymax*(1.+self.perc))
        
        if (self.Scale[2]/self.Scale[3]) > 1e-4:
            self.logY = True

        return True


###################
### Set methods ###
###################

    def setAxisTitleSize(self, size):

        ROOT.gStyle.SetTitleSize(size,"X")
        ROOT.gStyle.SetTitleSize(size,"Y")
        
        return True

    def setAxisTitleOffset(self, offset):

        ROOT.gStyle.SetTitleOffset(offset,"X")
        ROOT.gStyle.SetTitleOffset(offset,"Y")

        return True

    def getMarkerStyle(self, index):
        
        markerSet = [22,21,20,26,25,24]
        if index%9 == 0 and index > 0:
            self.counter += 1
        if index == 40:
            sys.exit("Overflow. Reduce number of graphs!")
        
        return markerSet[self.counter]
        #for marker in markerSet:
            #yield int(marker)


######################
### Legend methods ###
######################

    def setLegend(self):
        
        self.legend = ROOT.TLegend(self.LegendParameters[0],self.LegendParameters[1],self.LegendParameters[2],self.LegendParameters[3])
        self.legend.SetFillColor(0)
        self.legend.SetTextSize(.02)
        
        for i,graph in enumerate(self.__graphs):

            try:
                if self.legendEntry == "name":
                    self.legend.AddEntry(self.__graphs[i], self.__file[i].getName(), "p")
                elif self.legendEntry == "id":
                    self.legend.AddEntry(self.__graphs[i], self.__file[i].getID(), "p")
                else:
                    print "Legend entry type not found. Use 'name' instead"
                    self.legend.AddEntry(self.__graphs[i], self.__file[i].getName(), "p")
            except:
                pass

        self.legend.Draw()
        self.canvas.Update()
        

        
    def setLegendParameters(self):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right or outside
        # Plot is arround 80% of canvas from (0.1,0.15) to (0.9,0.9). 
        
        self.LegendParameters = []
        para = 0
        
        if len(self.__file[0].getName()) > para:
            para=len(self.__file[0].getName())
        
        # Top right corner is the default/starting position for the legend box.
        self.TopRight = True
        self.TopLeft = self.BottomRight = False
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-para/100.
        Lymin = Lymax-len(self.__graphs)*0.03
        print Lxmin
        print Lymin
        
        # Check if last element of graph is in the top right corner. 
        for i in range(len(self.__file)):
            for j in range(len(self.__file[i].getX())):
                #print (abs(self.__file[i].getX()[j]),self.xmax*(1.+self.perc))
                if abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc)))-0.1 > Lxmin:
                    print (self.__file[i].getName(), abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))))
                    if abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin:
                        #print (self.__file[i].getName(), abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))))
                        Lxmin = 0.18
                        Lymax = 0.88
                        Lymin = Lymax-len(self.__graphs)*0.03
                        Lxmax = 2.2*para/100.
                        #print ("TR", self.__file[i].getName())
                        self.TopRight = False
            
        # Check if first elements are in the top left corner.
         
        for i, graph in enumerate(self.__file):
            for j, points in enumerate(self.__file[i].getX()):
                if Lxmin-0.1 < abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))) < Lxmax:
                    if self.TopRight == False and abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin+0.1:
                        Lxmax = 0.89
                        Lymin = 0.18
                        Lxmin = Lxmax-para/100.
                        Lymax = Lymin+len(self.__graphs)*0.03
                        self.TopLeft = False
                
        # If the plot is too crowded, create more space on the right.
        for i, graph in enumerate(self.__file):
             for j, points in enumerate(self.__file[i].getX()):
                if abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))) > Lxmin:
                    if self.TopLeft == False and self.TopRight == False and abs(self.__file[i].getY()[len(self.__file[i].getY())-1]/(self.ymax*(1.+self.perc))) < Lymax:
                        Lxmax = 0.98
                        Lymax = 0.93
                        Lxmin = Lxmax-para/100.
                        Lymin = Lymax-len(self.__graphs)*0.03
            
        # Force certain positions via cfg
        #if self.TopRight == False and self.TopLeft == True:
        #    Lxmin = 0.18
       #     Lymax = 0.88
       #     Lymin = Lymax-len(self.__graphs)*0.03
       #     Lxmax = 2.2*para/100.
                
     #   if self.TopRight == False and self.TopLeft == False and self.BottomRight == True:
      #      Lxmax = 0.89
      #      Lymin = 0.18
      #      Lxmin = Lxmax-para/100.
     #       Lymax = Lymin+len(self.__graphs)*0.03
        

        self.LegendParameters.append(Lxmin)
        self.LegendParameters.append(Lymin)
        self.LegendParameters.append(Lxmax)
        self.LegendParameters.append(Lymax)
        

        
       


#####################
### Color methods ###
#####################

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

    def getColor(self,clr=0):
        colorSet = [1100,1200,1300,1400,1500,1600,1700,1800,1900]
        KITPlot.__color += 1
        KITPlot.__color %= 9
        #print KITPlot.__color
        return colorSet[KITPlot.__color-1]

    def setColor(self):
        for graph in self.__graphs:
            graph.SetMarkerColor(self.getColor())
        return True



###################
### Get methods ###
###################

    def getGraph(self, graph=None):
        
        if len(self.__graphs) == 1:
            return self.__graphs[0]
        elif (len(self.__graphs) != 1) & (graph is None):
            return self._graphs
        elif (len(self.__graphs) != 1) & (graph.isdigit()):
            return self.__graphs[graph]
        else:
            return False

    def getCanvas(self):
        return self.canvas
