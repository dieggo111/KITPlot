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
        
        self.fileInput = False
        self.cfgFile = cfgFile
        self.cfg_exists = False
                    
        # init colors and markers
        if self.__init == False:
            self.__initColor()
            self.__markerSet = [21,20,22,23,25,24,26,32,34] 
        else:
            pass

        # Load parameters         
        self.__initDefaultValues()
        
        if cfgFile is not None:
            self.loadCfg(cfgFile)
        elif self.__load_defaultCfg(input):
            print("Initialized default cfg file %s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(input)))[0]))
        else:
            self.__writeCfg(input)


        self.__initStyle()

        # load input
        self.__file = []
        self.__graphs = []
        
        # Load KITDataFile
        if isinstance(input, KITDataFile.KITDataFile):
            self.__file.append(input)
            self.addGraph(input.getX(),input.getY())

        # Load single PID
        elif isinstance(input, int):
            self.__file.append(KITDataFile.KITDataFile(input))
            self.addGraph(self.__file[-1].getX(), self.__file[-1].getY())
          
        elif isinstance(input, str):

            # Load single PID
            if input.isdigit():
                self.__file.append(KITDataFile.KITDataFile(input))
                self.addGraph(self.__file[-1].getX(), self.__file[-1].getY())
            
            # Load multiple data files in a folder
            elif os.path.isdir(input):
                self.fileInput = True
                for inputFile in os.listdir(input):
                    if (os.path.splitext(inputFile)[1] == ".txt"):
                        self.__file.append(KITDataFile.KITDataFile(input + inputFile))
                    else:
                        pass
                for i, File in enumerate(self.__file):
                    self.arrangeFileList()
                    self.addGraph(self.__file[i].getX(),self.__file[i].getY())

                        # If you open the file the data type changes from str to file 
                        # with open(input + file) as inputFile:
                        #     self.__file.append(KITDataFile.KITDataFile(inputFile))
                        #     self.addGraph(self.__file[-1].getX(),self.__file[-1].getY())
            


            # Load file with multiple PIDs
            elif os.path.isfile(input):
                if self.__checkPID(input) == True:
                    with open(input) as inputFile:
                        for line in inputFile:
                            entry = line.split()
                            if entry[0].isdigit():
                                self.__file.append(KITDataFile.KITDataFile(entry[0]))
                    for i, File in enumerate(self.__file):
                        self.arrangeFileList()
                        self.addGraph(self.__file[i].getX(),self.__file[i].getY())
                else:
                    self.__file.append(KITDataFile.KITDataFile(input))
                    self.addGraph(self.__file[-1].getX(),self.__file[-1].getY())
        

        
    ######################
    ### Default values ###
    ######################

    def __initDefaultValues(self):
    
        # Title options 
        self.title = "auto"
        self.titleX0 = 0.5
        self.titleY0 = 0.97
        self.titleH = 0.05

        # XAxis
        self.titleX = "auto"
        self.titleSizeX = 0.05
        self.titleOffsetX = 1.1
        self.labelSizeX = 0.04
        self.absX = True
        self.logX = False
        self.rangeX = "auto"

        # YAxis
        self.titleY = "auto"
        self.titleSizeY = 0.05
        self.titleOffsetY = 1.1
        self.labelSizeY = 0.04
        self.absY = True
        self.logY = False
        self.rangeY = "auto"
        
        # Legend
        self.legendEntry = "name" # name / id
        self.legendPosition = "auto"
        self.legendTextSize = 0.02
        
        # Misc
        self.padBottomMargin = 0.15
        self.padLeftMargin = 0.15
        self.markerSize = 1.5
        self.markerStyle = 22
        self.markerColor = 1100

        # More plot options
        self.GraphGroup = "off"
        
        
        
    ###################
    ### cfg methods ###
    ###################

    def loadCfg(self, cfgFile=None):
    
        # if cfg path is given, check if correct
        if cfgFile is not None:
            if os.path.exists(cfgFile):
                self.__initCfg(cfgFile)
                print("Initialized %s!" %(cfgFile))
            else:
                self.cfgFile = None
                print "No cfg found! Need valid path! Use default values!"
            

    def __load_defaultCfg(self, fileName="plot"):
        
        file_path = os.getcwd() + "/cfg"
        if os.path.exists(file_path) == False:
            print "No default cfg folder"
            return False
        else:
            if os.listdir(file_path) == []:
                print "Default cfg folder empty"
                return False
            for cfg in os.listdir(file_path):
                if cfg == ("%s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(fileName)))[0])):
                    #print("cfg/%s" %(cfg))
                    self.__initCfg("cfg/%s" %(cfg))
                    return True
            else:
                return False
                
        
    def __initCfg(self, fileName):
        
        cfgPrs = ConfigParser.ConfigParser()

        cfgPrs.read(fileName)
            
        self.title = cfgPrs.get('Title', 'title')
        self.titleX0 = cfgPrs.getfloat('Title', 'x0')
        self.titleY0 = cfgPrs.getfloat('Title', 'Y0')
        self.titleH = cfgPrs.getfloat('Title', 'height')

        self.titleX = cfgPrs.get('XAxis', 'title')
        self.titleSizeX = cfgPrs.getfloat('XAxis', 'titleSize')
        self.titleOffsetX = cfgPrs.getfloat('XAxis', 'titleOffset')
        self.labelSizeX = cfgPrs.getfloat('XAxis', 'labelsize')
        self.absX = cfgPrs.getboolean('XAxis', 'absolute')
        self.logX = cfgPrs.getboolean('XAxis', 'log')
        self.rangeX = cfgPrs.get('XAxis', 'xrange')

        self.titleY = cfgPrs.get('YAxis', 'title')
        self.titleSizeY = cfgPrs.getfloat('YAxis', 'titleSize')
        self.titleOffsetY = cfgPrs.getfloat('YAxis', 'titleOffset')
        self.labelSizeY = cfgPrs.getfloat('YAxis', 'labelsize')
        self.absY = cfgPrs.getboolean('YAxis', 'absolute')
        self.logY = cfgPrs.getboolean('YAxis', 'log')
        self.rangeY = cfgPrs.get('YAxis', 'yrange')

        self.legendEntry = cfgPrs.get('Legend', 'entry')
        self.legendPosition = cfgPrs.get('Legend', 'legend position')
        self.legendTextSize = cfgPrs.getfloat('Legend', 'textSize')

        self.padBottomMargin = cfgPrs.getfloat('Misc', 'pad bottom margin')
        self.padLeftMargin = cfgPrs.getfloat('Misc', 'pad left margin')
        self.markerSize = cfgPrs.getfloat('Misc', 'marker size')
        self.markerStyle = cfgPrs.getint('Misc', 'marker style')
        self.markerColor = cfgPrs.getint('Misc', 'marker color')

        self.GraphGroup = cfgPrs.get('More plot options', 'graph group')

    def __writeCfg(self, fileName="plot"):
        
        cfgPrs = ConfigParser.ConfigParser()

        if not os.path.exists("cfg"):
            os.makedirs("cfg")

        #if os.path.isdir(fileName):
        #    fileName = "cfg/%s.cfg" %(os.path.basename(os.path.normpath(fileName)))
        #else:
        #    fileName = "cfg/%s.cfg" %(os.path.splitext(os.path.basename(fileName))[0])

        fileName = "cfg/%s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(fileName)))[0])

        print fileName

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
            cfgPrs.set('XAxis', 'xRange', self.rangeX)

            cfgPrs.add_section('YAxis')
            cfgPrs.set('YAxis', 'Title', self.titleY)
            cfgPrs.set('YAxis', 'TitleOffset', self.titleOffsetY)
            cfgPrs.set('YAxis', 'TitleSize', self.titleSizeY)
            cfgPrs.set('YAxis', 'Labelsize', self.labelSizeY)
            cfgPrs.set('YAxis', 'Absolute', self.absY)
            cfgPrs.set('YAxis', 'Log', self.logY)
            cfgPrs.set('YAxis', 'yrange', self.rangeY)

            cfgPrs.add_section('Legend')
            cfgPrs.set('Legend', 'Entry', self.legendEntry)
            cfgPrs.set('Legend', 'legend position', self.legendPosition)
            cfgPrs.set('Legend', 'TextSize', self.legendTextSize)

            cfgPrs.add_section('Misc')
            cfgPrs.set('Misc', 'pad bottom margin', self.padBottomMargin)
            cfgPrs.set('Misc', 'pad left margin', self.padLeftMargin)
            cfgPrs.set('Misc', 'marker size', self.markerSize)
            cfgPrs.set('Misc', 'marker style', self.markerStyle)
            cfgPrs.set('Misc', 'marker color', self.markerColor)
            
            cfgPrs.add_section('More plot options')
            cfgPrs.set('More plot options', 'graph group', self.GraphGroup)

            cfgPrs.write(cfgFile)

        print ("Wrote %s" %(fileName))
        

##############
### Checks ###
##############

    def MeasurementType(self):
    
        self.MT = self.__file[0].getParaY()
        if self.MT == "I_tot":
            self.autotitle = "Current Voltage Characteristics" 
            self.autotitleY = "Current (A)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "Pinhole":
            self.autotitle = "Pinhole Leakage" 
            self.autotitleY = "Current (A)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "I_leak_dc":
            self.autotitle = "Interstrip Current Leakage" 
            self.autotitleY = "Current (A)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "C_tot":
            self.autotitle = "Capacitance Voltage Characteristics" 
            self.autotitleY = "Capacitance (F)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "C_int":
            self.autotitle = "Interstrip Capacitance Measurement" 
            self.autotitleY = "Capacitance (F)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "CC":
            self.autotitle = "Coupling Capacitance Measurement" 
            self.autotitleY = "Capacitance (F)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "R_int":
            self.autotitle = "Interstrip Resistance Measurement" 
            self.autotitleY = "Resistance (#Omega)"
            self.autotitleX = "Voltage (V)"
        if self.MT == "R_poly":
            self.autotitle = "Strip Resistance Measurement" 
            self.autotitleY = "Resistance (#Omega)"
            self.autotitleX = "Voltage (V)"
            
        if len(self.__file) >= 2 and self.fileInput == False:
            if self.__file[0].getParaY() != self.__file[1].getParaY():
                sys.exit("Measurement types are not equal!")
        
        if self.fileInput == True:
            self.autotitle = "Title" 
            self.autotitleY = "Y Value"
            self.autotitleX = "X Value"

    def __checkPID(self, input):
        
        if os.path.isfile(input):
            with open(input) as inputFile:
                if len(inputFile.readline().split()) == 1:
                    return True
                else:
                    return False

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


    def addGraph(self, *args):
        
        # args: x, y or KITDataFile

        if isinstance(args[0], KITDataFile.KITDataFile):

            self.__file.append(args[0])
            
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
                
        elif len(args) == 2 and not isinstance(args[0], KITDataFile.KITDataFile):
            
            if self.absX:
                x = np.absolute(args[0])
            else:
                x = args[0]
            
            if self.absY:
                y = np.absolute(args[1])
            else:
                y = args[1]
        else:
            sys.exit("Cant add graph")
        
        self.__graphs.append(ROOT.TGraph(len(x),np.asarray(x),np.asarray(y)))

        return True
            
                        
    def Draw(self, arg="AP"):

        # init canvas
        self.canvas = ROOT.TCanvas("c1","c1",1280,768)
        self.canvas.cd()

        # apply scaling and auto title
        self.__autoScaling()
        self.MeasurementType()
        
        self.plotStyles(self.titleX, self.titleY, self.title)    
        
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
        

        # Set legend
        self.setLegendParameters()
        self.setLegend()

        self.canvas.Update()
        
        if self.cfg_exists == True and self.cfgFile is not None:
            self.canvas.SaveAs(self.cfgFile.split(".")[0].split("/")[1] + ".png")
        else:
            self.saveAs("plot")
            
        return True


    def saveAs(self, fileName="plot"):

        if not os.path.exists("output"):
            os.makedirs("output")
        
        self.canvas.SaveAs("output/%s.png" %(fileName))        
                

    def update(self):
        
        try:
            self.canvas.Update()
        except:
            pass
        

    def plotStyles(self, XTitle, YTitle, Title):
        
        self.__graphs[0].GetXaxis().SetTitle(XTitle)
        self.__graphs[0].GetYaxis().SetTitle(YTitle)
        self.__graphs[0].SetTitle(Title)
        
        if self.titleX == "auto":
            self.__graphs[0].GetXaxis().SetTitle(self.autotitleX)
        if self.titleY == "auto":
            self.__graphs[0].GetYaxis().SetTitle(self.autotitleY)
        if self.title == "auto":
            self.__graphs[0].SetTitle(self.autotitle)
        
        if self.rangeX == "auto":
            self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[1])
        elif ":" in self.rangeX:
            RangeListX = self.rangeX.split(":")
            self.__graphs[0].GetXaxis().SetLimits(float(RangeListX[0]),float(RangeListX[1]))
        else:
            sys.exit("Invalid X-axis range! Try 'auto' or 'float:float'!")
       
        if self.rangeY == "auto":
            self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[2],self.Scale[3])
        elif ":" in self.rangeY:
            RangeListY = self.rangeY.split(":")
            self.__graphs[0].GetYaxis().SetRangeUser(float(RangeListY[0]),float(RangeListY[1]))
        else:
            sys.exit("Invalid X-axis range! Try 'auto' or 'float:float'!")
                
                
        self.counter = 0
        
        # need to work on getFluenceP() method
        if self.fileInput == True and self.GraphGroup == "fluence":
            sys.exit("Fluence groups only work with ID inputs right now!")
        
        for i, graph in enumerate(self.__graphs):
            graph.SetMarkerColor(self.getColor())
            if self.GraphGroup == "off":
                graph.SetMarkerStyle(self.getMarkerStyle(i))
            if self.GraphGroup == "name" or self.GraphGroup == "fluence":
                for j, Element in enumerate(self.getGroupList()):
                    if self.GraphGroup == "name" and self.__file[i].getName()[:5] == Element:
                        graph.SetMarkerStyle(self.__markerSet[0+j])
                    if self.GraphGroup == "fluence" and self.__file[i].getFluenceP() == Element:
                        graph.SetMarkerStyle(self.__markerSet[0+j])
            if self.GraphGroup != "off" and self.GraphGroup != "name" and self.GraphGroup != "fluence":
                sys.exit("Invalid group parameter! Try 'off', 'name' or 'fluence'!")
            
        return True
        
    def arrangeFileList(self):

        TempList1 = []
        TempList2 = []
        IndexList = []
        for i, temp in enumerate(self.__file):
            TempList1.append(temp.getName()[:5])
        for i, temp in enumerate(TempList1):
            if temp not in TempList2:
                TempList2.append(temp)
                
        for i, temp1 in enumerate(TempList1):
            for j, temp2 in enumerate(TempList2):
                if temp1 == temp2:
                    IndexList.append(j)

        TempList1[:] = []
        max_index = 0
        for Index in IndexList:
            if Index > max_index:
                max_index = Index
        for Index in range(max_index+1):
            for i, File in enumerate(self.__file):
                if Index == IndexList[i]:
                    TempList1.append(File)
        self.__file = TempList1

#######################
### Automatizations ###
#######################

    def __autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]

        self.perc = 0.05
        ListX = [0]
        ListY = [0]

        for inputFile in self.__file:
            ListX += inputFile.getX()
            ListY += inputFile.getY()

        if self.absX:
            ListX = np.absolute(ListX)
        if self.absY:
            ListY = np.absolute(ListY)

        self.Scale = []
        self.xmax = max(ListX)
        self.xmin = min(ListX)
        self.ymax = max(ListY)
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
        
        # same marker for as many graphs as possible
        #if index%9 == 0 and index > 0:
        #    self.counter += 1
        #if index == 30:
        #    sys.exit("Overflow. Reduce number of graphs!")
        
        #return self.__markerSet[self.counter]
        
        if index >= 9:
            index -= 9
        if index >= 15:
            sys.exit("Overflow. Reduce number of graphs!")
        else:
            return self.__markerSet[index]
            
            
    def getGroupList(self):
    
        self.GroupList = []
        TempList = []
        for i, Element in enumerate(self.__file):
            if self.GraphGroup == "name":
                TempList.append(self.__file[i].getName()[:5])
            if self.GraphGroup == "fluence":
                TempList.append(self.__file[i].getFluenceP())

        for i, TempElement in enumerate(TempList):
            if TempElement not in self.GroupList:
                  self.GroupList.append(TempList[i])

        return self.GroupList

######################
### Legend methods ###
######################

    def setLegend(self):

        self.legend = ROOT.TLegend(self.LegendParameters[0],self.LegendParameters[1],self.LegendParameters[2],self.LegendParameters[3])
        self.legend.SetFillColor(0)
        self.legend.SetTextSize(self.legendTextSize)

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
        self.TopRight = self.TopLeft = self.BottomRight = True
        
        for i in range(len(self.__file)):
            if len(self.__file[i].getName()) > para:
                para=len(self.__file[i].getName())

        if self.legendPosition != "auto" and self.legendPosition != "TR" and self.legendPosition != "TL" and self.legendPosition != "BR":
            sys.exit("Invalid legend position! Try 'auto', 'TR', 'TL' or 'BR'!")
        
        # Top right corner is the default/starting position for the legend box
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-para/100.
        Lymin = Lymax-len(self.__graphs)*0.03
            
            
        # Check if elements are in the top right corner. 
        for i in range(len(self.__file)):
            for j in range(len(self.__file[i].getX())):
                if abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc)))-0.1 > Lxmin and self.legendPosition == "auto":
                    if abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin:
                        self.TopRight = False
        
        if self.TopRight == False or self.legendPosition == "TL":
            Lxmin = 0.18
            Lymax = 0.88
            Lymin = Lymax-len(self.__graphs)*0.03
            Lxmax = Lxmin+para/100.

        # Check if elements are in the top left corner.
        for i in range(len(self.__file)):
            for j in range(len(self.__file[i].getX())):
                if Lxmin-0.1 < abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))) < Lxmax+0.05:
                    if abs(self.__file[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin+0.08 and self.legendPosition == "auto":
                        self.TopLeft = False
                
        if self.TopLeft == self.TopRight == False or self.legendPosition == "BR":
            Lxmax = 0.89
            Lymin = 0.18
            Lxmin = Lxmax-para/100.
            Lymax = Lymin+len(self.__graphs)*0.03
        
        # If the plot is too crowded, create more space on the right.
        for i in range(len(self.__file)):
            for j in range(len(self.__file[i].getX())):
                if abs(self.__file[i].getX()[j]/(self.xmax*(1.+self.perc))) > Lxmin:
                    if abs(self.__file[i].getY()[len(self.__file[i].getY())-1]/(self.ymax*(1.+self.perc))) < Lymax and self.legendPosition == "auto":
                        self.BottomRight = False

        if self.BottomRight == self.TopLeft == self.TopRight == False:
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-para/100.
            Lymin = Lymax-len(self.__graphs)*0.03
            print "Couldn't find sufficient space!"
            
        if self.legendPosition == "TR":
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-para/100.
            Lymin = Lymax-len(self.__graphs)*0.03

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
        
        self.__kitRed.append(ROOT.TColor(1200, 191./255, 35./255, 41./255))
        self.__kitRed.append(ROOT.TColor(1201, 205./255, 85./255, 75./255))
        self.__kitRed.append(ROOT.TColor(1202, 220./255, 130./255, 110./255))
        self.__kitRed.append(ROOT.TColor(1203, 230./255, 175./255, 160./255))
        self.__kitRed.append(ROOT.TColor(1204, 245./255, 215./255, 200./255))
        
        self.__kitOrange.append(ROOT.TColor(1300, 247./255, 145./255, 16./255))
        
        self.__kitBlue.append(ROOT.TColor(1400, 67./255, 115./255, 194./255))
        self.__kitBlue.append(ROOT.TColor(1401, 120./255, 145./255, 210./255))
        self.__kitBlue.append(ROOT.TColor(1402, 155./255, 170./255, 220./255))
        self.__kitBlue.append(ROOT.TColor(1403, 195./255, 200./255, 235./255))
        self.__kitBlue.append(ROOT.TColor(1404, 225./255, 225./255, 245./255))

        self.__kitPurple.append(ROOT.TColor(1500, 188./255, 12./255, 141./255))

        self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))

        self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))

        self.__kitYellow.append(ROOT.TColor(1800, 254./255, 231./255, 2./255))

        self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))

        KITPlot.__init = True
        
        return True

    def getColor(self,clr=0):
        self.colorSet = [1100,1200,1300,1400,1500,1600,1700,1800,1900]
        KITPlot.__color += 1
        KITPlot.__color %= 9

        return self.colorSet[KITPlot.__color-1]

    def setColor(self):
        for graph in self.__graphs:
            graph.SetMarkerColor(self.getColor())
            
        return True

    def getShade(self):
        i = 0
        self.shadeSet = []
        print self.colorSet
        print len(self.colorSet)
        #if i<range(self.colorSet):
        #    for j in range(4):
        #        self.shadeSet.append(self.colorSet[i]+j)
        #    i +=1
        #else:
        #    print self.shadeSet
        #     return True


###################
### Get methods ###
###################

    def getGraph(self, graph=None):
        
        if len(self.__graphs) == 1:
            return self.__graphs[0]
        elif (len(self.__graphs) != 1) and (graph is None):
            return self._graphs
        else:
            if isinstance(graph,str):
                if (len(self.__graphs) != 1) and (graph.isdigit()):
                    return self.__graphs[int(graph)]
                else:
                    return False
            elif isinstance(graph,int):
                if (len(self.__graphs) != 1):
                    return self.__graphs[graph]
                else:
                    return False


    def getCanvas(self):
        return self.canvas
        
        

