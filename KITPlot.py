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

    def __init__(self, dataInput=None, cfgFile=None):

        
        # init lists
        self.__files = []
        self.__graphs = []

        # TODO: Can we get rid of these two?
        self.cfgFile = cfgFile
        self.cfg_exists = False
                    
        # init colors and markers
        if self.__init == False:
            self.__initColor()
            self.__markerSet = [21,20,22,23,25,24,26,32,34] 
        else:
            pass

        # Load parameters and apply deault style        
        self.__initDefaultValues()


        if cfgFile is not None:
            self.loadCfg(cfgFile)
        elif dataInput is None and self.__load_defaultCfg("plot"):
            print("Initialized default cfg file plot.cfg")
        elif dataInput is None and self.__load_defaultCfg("plot") is not True:
            self.__writeCfg("plot.cfg")
        elif self.__load_defaultCfg(dataInput):
            print("Initialized default cfg file %s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(dataInput)))[0]))
        else:
            self.__writeCfg(dataInput)

        self.__initStyle()

        
        # add files
        if dataInput is not None:
            self.add(dataInput)
        else:
            pass
        

    ######################
    ### Default values ###
    ######################

    def __initDefaultValues(self):
        """Initialize default values for all parameters

        Args:
            No arguments
        Returns:
            True
         
        """

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
        self.legendEntry = "name" 
        self.legendPosition = "auto"
        self.legendTextSize = 0.02
        self.legendBoxPara = 1
         
        # Misc
        self.padBottomMargin = 0.15
        self.padLeftMargin = 0.15
        self.markerSize = 1.5
        self.markerStyle = 22
        self.markerColor = 1100

        # More plot options
        self.GraphGroup = "off"
        self.ColorShades = False
        
        return True
        
        
    ###################
    ### cfg methods ###
    ###################

    def loadCfg(self, cfgFile=None):
        """Load cfg file or default values if no file is given

        Args:
            cfgFile: cfg file name
        Returns:
            True or False whether file was found or not
        """
        
        if cfgFile is not None:
            if os.path.exists(cfgFile):
                self.__initCfg(cfgFile)
                print("Initialized %s!" %(cfgFile))
                return True
            else:
                self.cfgFile = None
                print "No cfg found! Need valid path! Use default values!"
                return False

    def __load_defaultCfg(self, fileName="plot"):
        """Search for default cfg of given plot
        
        Args:
            fileName: name of plot (fileName, pid)
        Return:
            True or False whether file was found or not
        """
        
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
        """Initialize cfg for plot
        
        Args:
            fileName: name of cfg file
        Returns:
            True
        """

        cfgPrs = ConfigParser.ConfigParser()

        cfgPrs.read(fileName)
            
        self.title = cfgPrs.get('Title', 'title')
        self.titleX0 = cfgPrs.getfloat('Title', 'x0')
        self.titleY0 = cfgPrs.getfloat('Title', 'Y0')
        self.titleH = cfgPrs.getfloat('Title', 'height')

        self.titleX = cfgPrs.get('XAxis', 'title')
        self.titleSizeX = cfgPrs.getfloat('XAxis', 'title Size')
        self.titleOffsetX = cfgPrs.getfloat('XAxis', 'title Offset')
        self.labelSizeX = cfgPrs.getfloat('XAxis', 'label size')
        self.absX = cfgPrs.getboolean('XAxis', 'absolute')
        self.logX = cfgPrs.getboolean('XAxis', 'log')
        self.rangeX = cfgPrs.get('XAxis', 'xrange')

        self.titleY = cfgPrs.get('YAxis', 'title')
        self.titleSizeY = cfgPrs.getfloat('YAxis', 'title Size')
        self.titleOffsetY = cfgPrs.getfloat('YAxis', 'title Offset')
        self.labelSizeY = cfgPrs.getfloat('YAxis', 'label size')
        self.absY = cfgPrs.getboolean('YAxis', 'absolute')
        self.logY = cfgPrs.getboolean('YAxis', 'log')
        self.rangeY = cfgPrs.get('YAxis', 'yrange')

        self.legendEntry = cfgPrs.get('Legend', 'entry')
        self.legendPosition = cfgPrs.get('Legend', 'legend position')
        self.legendTextSize = cfgPrs.getfloat('Legend', 'text Size')
        self.legendBoxPara = cfgPrs.getfloat('Legend', 'box parameter')
        
        self.padBottomMargin = cfgPrs.getfloat('Misc', 'pad bottom margin')
        self.padLeftMargin = cfgPrs.getfloat('Misc', 'pad left margin')
        self.markerSize = cfgPrs.getfloat('Misc', 'marker size')
        self.markerStyle = cfgPrs.getint('Misc', 'marker style')
        self.markerColor = cfgPrs.getint('Misc', 'marker color')

        self.GraphGroup = cfgPrs.get('More plot options', 'graph group')
        self.ColorShades = cfgPrs.getboolean('More plot options', 'color shades')

        return True

    def __writeCfg(self, fileName="plot"):
        """Write new cfg file

        Args:
            fileName: name of cfg file
        Return:
            True
        """
        
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
            cfgPrs.set('XAxis', 'Title Offset', self.titleOffsetX)
            cfgPrs.set('XAxis', 'Title Size', self.titleSizeX)
            cfgPrs.set('XAxis', 'Label Size', self.labelSizeX)
            cfgPrs.set('XAxis', 'Absolute', self.absX)
            cfgPrs.set('XAxis', 'Log', self.logX)
            cfgPrs.set('XAxis', 'xRange', self.rangeX)

            cfgPrs.add_section('YAxis')
            cfgPrs.set('YAxis', 'Title', self.titleY)
            cfgPrs.set('YAxis', 'Title Offset', self.titleOffsetY)
            cfgPrs.set('YAxis', 'Title Size', self.titleSizeY)
            cfgPrs.set('YAxis', 'Label Size', self.labelSizeY)
            cfgPrs.set('YAxis', 'Absolute', self.absY)
            cfgPrs.set('YAxis', 'Log', self.logY)
            cfgPrs.set('YAxis', 'yrange', self.rangeY)

            cfgPrs.add_section('Legend')
            cfgPrs.set('Legend', 'Entry', self.legendEntry)
            cfgPrs.set('Legend', 'legend position', self.legendPosition)
            cfgPrs.set('Legend', 'Text Size', self.legendTextSize)
            cfgPrs.set('Legend', 'box parameter', self.legendBoxPara)

            cfgPrs.add_section('Misc')
            cfgPrs.set('Misc', 'pad bottom margin', self.padBottomMargin)
            cfgPrs.set('Misc', 'pad left margin', self.padLeftMargin)
            cfgPrs.set('Misc', 'marker size', self.markerSize)
            cfgPrs.set('Misc', 'marker style', self.markerStyle)
            cfgPrs.set('Misc', 'marker color', self.markerColor)
            
            cfgPrs.add_section('More plot options')
            cfgPrs.set('More plot options', 'graph group', self.GraphGroup)
            cfgPrs.set('More plot options', 'color shades', self.ColorShades)

            cfgPrs.write(cfgFile)

        print ("Wrote %s" %(fileName))
        return True


    ##############
    ### Checks ###
    ##############

    def MeasurementType(self):

        if self.__files[0].getParaY() == None:
            self.autotitle = "Title" 
            self.autotitleY = "Y Value"
            self.autotitleX = "X Value"
            
        if self.__files[0].getParaY() != None:
            self.MT = self.__files[0].getParaY()
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
            
        if len(self.__files) >= 2 and self.__files[0].getParaY() != None:
            if self.__files[0].getParaY() != self.__files[1].getParaY():
                sys.exit("Measurement types are not equal!")

    def __checkPID(self, dataInput):
        
        if os.path.isfile(dataInput):
            with open(dataInput) as inputFile:
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


    def add(self, dataInput=None):
        
        # Load KITDataFile
        if isinstance(dataInput, KITDataFile.KITDataFile):
            self.__filess.append(dataInput)
            self.addGraph(dataInput.getX(),dataInput.getY())

        # Load single PID
        elif isinstance(dataInput, int):
            self.__files.append(KITDataFile.KITDataFile(dataInput))
            self.addGraph(self.__files[-1].getX(), self.__files[-1].getY())
          
        elif isinstance(dataInput, str):

            # Load single PID
            if dataInput.isdigit():
                self.__files.append(KITDataFile.KITDataFile(dataInput))
                self.addGraph(self.__files[-1].getX(), self.__files[-1].getY())
            
            # Load multiple data files in a folder
            elif os.path.isdir(dataInput):
                for inputFile in os.listdir(dataInput):
                    if (os.path.splitext(inputFile)[1] == ".txt"):
                        self.__files.append(KITDataFile.KITDataFile(dataInput + inputFile))
                    else:
                        pass
                for i, File in enumerate(self.__files):
                    self.arrangeFileList()
                    self.addGraph(self.__files[i].getX(),self.__files[i].getY())

                        # If you open the file the data type changes from str to file 
                        # with open(dataInput + file) as inputFile:
                        #     self.__files.append(KITDataFile.KITDataFile(inputFile))
                        #     self.addGraph(self.__files[-1].getX(),self.__files[-1].getY())
            

            # Load single file or file with multiple PIDs
            elif os.path.isfile(dataInput):
                if self.__checkPID(dataInput) == True:
                    with open(dataInput) as inputFile:
                        for line in inputFile:
                            entry = line.split()
                            if entry[0].isdigit():
                                self.__files.append(KITDataFile.KITDataFile(entry[0]))
                    for i, File in enumerate(self.__files):
                        self.arrangeFileList()
                        self.addGraph(self.__files[i].getX(),self.__files[i].getY())
                else:
                    self.__files.append(KITDataFile.KITDataFile(dataInput))
                    self.addGraph(self.__files[-1].getX(),self.__files[-1].getY())



    def addGraph(self, *args):
        
        # args: x, y or KITDataFile

        if isinstance(args[0], KITDataFile.KITDataFile):

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
            
                        
    def draw(self, arg="AP"):

        if len(self.__graphs) == 0:
            print "No graphs to draw"
            return False

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
        if self.__files[0].getParaY() == None and self.GraphGroup == "fluence":
            sys.exit("Fluence group only works with ID inputs right now!")
        
        
        # assign marker style
        for i, graph in enumerate(self.__graphs):
            if self.GraphGroup == "off":
                graph.SetMarkerStyle(self.getMarkerStyle(i))
            elif self.GraphGroup == "name" and self.ColorShades == True:
                graph.SetMarkerStyle(self.getMarkerShade(i))
            elif self.GraphGroup != "off" and self.GraphGroup != "name" and self.GraphGroup != "fluence":
                sys.exit("Invalid group parameter! Try 'off', 'name' or 'fluence'!")
            elif self.GraphGroup == "name" and self.ColorShades == False:
                for j, Element in enumerate(self.getGroupList()):
                    if self.GraphGroup == "name" and self.__files[i].getName()[:5] == Element:
                        graph.SetMarkerStyle(self.__markerSet[0+j])
                    if self.GraphGroup == "fluence" and self.__files[i].getFluenceP() == Element:
                        graph.SetMarkerStyle(self.__markerSet[0+j])

                
                
        # assign color
        for i, graph in enumerate(self.__graphs):
            if self.GraphGroup == "off" :
                graph.SetMarkerColor(self.getColor())
            elif self.GraphGroup == "name" and self.ColorShades == False:
                graph.SetMarkerColor(self.getColor())
            elif self.GraphGroup == "name" and self.ColorShades == True:
                graph.SetMarkerColor(self.getColorShades(i))
            if self.GraphGroup == "off" and self.ColorShades == True:
                sys.exit("Need graph groups for applying shades!")
        return True
        
        
    def arrangeFileList(self):

        TempList1 = []
        TempList2 = []
        IndexList = []
        for i, temp in enumerate(self.__files):
            TempList1.append(temp.getName()[:5])
        for i, temp in enumerate(TempList1):
            if temp not in TempList2:
                TempList2.append(temp)
        TempList2.sort()
                
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
            for i, File in enumerate(self.__files):
                if Index == IndexList[i]:
                    TempList1.append(File)
        self.__files = TempList1

#######################
### Automatizations ###
#######################

    def __autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]

        self.perc = 0.05
        ListX = [0]
        ListY = [0]

        for inputFile in self.__files:
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
            
    def getMarkerShade(self, index):
        
        self.getShadeList()
        MarkerShade = []
        color_num = self.ShadeList[0]
        
        for i, shade in enumerate(self.ShadeList):
            if not self.ShadeList[i]-color_num > 10:
                MarkerShade.append(self.ShadeList[i]-color_num)
            if self.ShadeList[i]-color_num > 10:
                color_num += 100
                MarkerShade.append(self.ShadeList[i]-color_num)
        
        return self.__markerSet[MarkerShade[index]]
         
    def getGroupList(self):
    
        self.GroupList = []
        TempList = []
        for i, Element in enumerate(self.__files):
            if self.GraphGroup == "name":
                TempList.append(self.__files[i].getName()[:5])
            if self.GraphGroup == "fluence":
                TempList.append(self.__files[i].getFluenceP())

        for i, TempElement in enumerate(TempList):
            if TempElement not in self.GroupList:
                  self.GroupList.append(TempList[i])

        return self.GroupList

######################
### Legend methods ###
######################

    def setLegendEntries(self):
    
        UserEntries = []
        EntryNumber = []
        EntryName = []
        UserEntries = self.legendEntry.replace("=",",").split(",")
        for element in UserEntries:
            if element.isdigit() == True:
                EntryNumber.append(element)
            else:
                EntryName.append(element)
        if len(EntryNumber) != len(EntryName):
            sys.exit("Invalid legend entries given! Try 'entry number=entry name, ...'!")
            
        self.LegendEntryList = []
        number=int(EntryNumber[0])
        j=0
        
        for i in range(len(self.__graphs)):
            if i == number:
                self.LegendEntryList.append(EntryName[j])
                if j < len(EntryNumber)-1:
                    j += 1
                number = int(EntryNumber[j])
            else:
                self.LegendEntryList.append(self.__files[i].getName())
        
        return True
            


    def setLegend(self):

        self.legend = ROOT.TLegend(self.LegendParameters[0],self.LegendParameters[1],self.LegendParameters[2],self.LegendParameters[3])
        self.legend.SetFillColor(0)
        
        if 0.02 <= self.legendTextSize <= 0.03:
            self.legend.SetTextSize(self.legendTextSize)
        else:
            sys.exit("Invalid legend text size! Need value between 0.02 and 0.03!")
        

        for i,graph in enumerate(self.__graphs):
            if self.legendEntry == "name":
                self.legend.AddEntry(self.__graphs[i], self.__files[i].getName(), "p")
            elif self.legendEntry == "ID":
                self.legend.AddEntry(self.__graphs[i], self.__files[i].getID(), "p")
            elif self.legendEntry[0].isdigit() == True and self.legendEntry[1] == "=":
                self.setLegendEntries()
                self.legend.AddEntry(self.__graphs[i], self.LegendEntryList[i], "p")
            else:
                print "Invalid entry! Using graph names"
                self.legend.AddEntry(self.__graphs[i], self.__files[i].getName(), "p")
                
 
        self.legend.Draw()
        self.canvas.Update()

        
    def setLegendParameters(self):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right or outside
        # Plot is arround 80% of canvas from (0.1,0.15) to (0.9,0.9). 
        
        self.LegendParameters = []
        para = 0
        self.TopRight = self.TopLeft = self.BottomRight = True
        
        for i in range(len(self.__files)):
            if len(self.__files[i].getName()) > para:
                para=len(self.__files[i].getName())
        
        if para > 29:
                sys.exit("Legend name too long! Reduce the number of characters!")
        if not 0.5 <= self.legendBoxPara <= 1.5:
            sys.exit("Invalid box parameter! Value must be between 0.5 and 1.5!")
        else:
            pass
        
        if self.legendTextSize == 0.02:
            magic_para = para/100.*self.legendBoxPara
        else: 
            magic_para = (para/100.+para*self.legendTextSize/50)*self.legendBoxPara
        
        
        if self.legendPosition != "auto" and self.legendPosition != "TR" and self.legendPosition != "TL" and self.legendPosition != "BR":
            sys.exit("Invalid legend position! Try 'auto', 'TR', 'TL' or 'BR'!")
        
        # Top right corner is the default/starting position for the legend box
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-magic_para
        Lymin = Lymax-len(self.__graphs)*0.03+self.legendTextSize
            
            
        # Check if elements are in the top right corner. 
        for i in range(len(self.__files)):
            for j in range(len(self.__files[i].getX())):
                if abs(self.__files[i].getX()[j]/(self.xmax*(1.+self.perc)))-0.1 > Lxmin and self.legendPosition == "auto":
                    if abs(self.__files[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin:
                        self.TopRight = False
        
        if self.TopRight == False or self.legendPosition == "TL":
            Lxmin = 0.18
            Lymax = 0.88
            Lymin = Lymax-len(self.__graphs)*0.03-self.legendTextSize
            Lxmax = Lxmin+magic_para

        # Check if elements are in the top left corner.
        for i in range(len(self.__files)):
            for j in range(len(self.__files[i].getX())):
                if Lxmin-0.1 < abs(self.__files[i].getX()[j]/(self.xmax*(1.+self.perc))) < Lxmax+0.05:
                    if abs(self.__files[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin+0.08 and self.legendPosition == "auto":
                        self.TopLeft = False
                
        if self.TopLeft == self.TopRight == False or self.legendPosition == "BR":
            Lxmax = 0.89
            Lymin = 0.18
            Lxmin = Lxmax-magic_para
            Lymax = Lymin+len(self.__graphs)*0.03+self.legendTextSize
            
        # If the plot is too crowded, create more space on the right.
        for i in range(len(self.__files)):
            for j in range(len(self.__files[i].getX())):
                if abs(self.__files[i].getX()[j]/(self.xmax*(1.+self.perc))) > Lxmin:
                    if abs(self.__files[i].getY()[len(self.__files[i].getY())-1]/(self.ymax*(1.+self.perc))) < Lymax and self.legendPosition == "auto":
                        self.BottomRight = False

        if self.BottomRight == self.TopLeft == self.TopRight == False:
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-magic_para
            Lymin = Lymax-len(self.__graphs)*0.03-self.legendTextSize
            print "Couldn't find sufficient space!"
            
        if self.legendPosition == "TR":
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-magic_para
            Lymin = Lymax-len(self.__graphs)*0.03-self.legendTextSize

        self.LegendParameters.append(Lxmin)
        self.LegendParameters.append(Lymin)
        self.LegendParameters.append(Lxmax)
        self.LegendParameters.append(Lymax)
        
       


#####################
### Color methods ###
#####################

    def __initColor(self):
    
        self.colorSet = [1100,1200,1300,1400,1500,1600,1700,1800,1900]

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
        #self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))
        #self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))
        #self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))
        #self.__kitBrown.append(ROOT.TColor(1600, 170./255, 127./255, 36./255))

        self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))
        #self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))
        #self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))
        #self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))
        #self.__kitMay.append(ROOT.TColor(1700, 102./255, 196./255, 48./255))
        
        self.__kitYellow.append(ROOT.TColor(1800, 254./255, 231./255, 2./255))
        #self.__kitYellow.append(ROOT.TColor(1800, 254./255, 231./255, 2./255))
        #self.__kitYellow.append(ROOT.TColor(1800, 254./255, 231./255, 2./255))
        #self.__kitYellow.append(ROOT.TColor(1800, 254./255, 231./255, 2./255))
        #self.__kitYellow.append(ROOT.TColor(1800, 254./255, 231./255, 2./255))

        self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))
        #self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))
        #self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))
        #self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))
        #self.__kitCyan.append(ROOT.TColor(1900, 28./255, 174./255, 236./255))
       

        KITPlot.__init = True
        
        return True

    def getColor(self,clr=0):
        KITPlot.__color += 1
        KITPlot.__color %= 9

        return self.colorSet[KITPlot.__color-1]


    def getShadeList(self):
    
        self.ShadeList = []
        shade_counter = 0
        j = 0
        
        for File in self.__files:
            if File.getName()[:5] == self.getGroupList()[j]:
                self.ShadeList.append(self.colorSet[j]+shade_counter)
                shade_counter += 1
            if File.getName()[:5] != self.getGroupList()[j]:
                shade_counter = 0
                if j <= len(self.getGroupList())-1:
                    j += 1
                self.ShadeList.append(self.colorSet[j]+shade_counter)
                shade_counter += 1
             
        return True
        
    def getColorShades(self, index):
        self.getShadeList()
        return self.ShadeList[index]
        
        



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
                    
    def getFile(self, KITFile=None):
        
        if len(self.__files) == 1:
            return self.__files[0]
        elif (len(self.__files) != 1) and (KITFile is None):
            return self._file
        else:
            if isinstance(KITFile,str):
                if (len(self.__files) != 1) and (KITFile.isdigit()):
                    return self.__files[int(KITFile)]
                else:
                    return False
            elif isinstance(KITFile,int):
                if (len(self.__files) != 1):
                    return self.__files[KITFile]
                else:
                    return False


    def getCanvas(self):
        return self.canvas
        
