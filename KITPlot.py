import numpy as np
import ROOT
import os, sys
sys.path.append('modules/ConfigHandler/')
sys.path.append('modules/LegHandler/')
import KITData 
from ConfigHandler import ConfigHandler
from LegHandler import LegHandler

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
                    
        # init colors and markers
        if self.__init == False:
            self.__initColor()
            self.__markerSet = [21,20,22,23,25,24,26,32,34] 
            self.cfg_initialized = False
        else:
            pass

        # Load parameters and apply default style        
        self.__cfg = ConfigHandler()
        self.cfgPath = "cfg/" + self.__cfg.getCfgName(dataInput)

        if cfgFile is not None: #Load cfg file
            self.__cfg.load(cfgFile)
        elif dataInput is None and self.__cfgPresent(): # Empty KITPlot with existing default cfg
            self.__cfg.load('default.cfg')
            print ("Initialized default.cfg")
        elif dataInput is None and self.__cfgPresent() is not True: # Empty KITPlot / create new default cfg
            self.__initDefaultCfg()
            self.__cfg.write()
            print ("Created new default.cfg")
        elif dataInput is not None and self.__cfgPresent(dataInput): # Load default dataInput cfg
            self.__cfg.load(dataInput)
            print ("Initialized cfg file: %s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(dataInput)))[0]))
        else:
            print (self.__cfgPresent())
            # create new cfg for dataInput
            self.cfg_initialized = True
            self.__initDefaultCfg()
            self.__cfg.write(dataInput)
            print ("%s.cfg has been created" %dataInput)

        self.__initStyle()
        print self.__cfg.get('General','Measurement')
        # add files
        if dataInput is not None:
            self.add(dataInput, self.__cfg.get('General','Measurement'))
        else:
            pass
        
    #####################
    ### ConfigHandler ###
    #####################

    def __initDefaultCfg(self):
        
        pDict = {'General' :{ 'Measurement'  : 'probe'   },
                 'Title'   :{ 'Title'        : 'Title',
                              'X0'           : 0.5,
                              'Y0'           : 0.97,
                              'H'            : 0.05,
                              'Font'         : 62        },
                 'XAxis'   :{ 'Title'        : 'X Value',
                              'Size'         : 0.05,
                              'Offset'       : 1.1,
                              'LabelSize'    : 0.04,
                              'Font'         : 62,
                              'Abs'          : True,
                              'Log'          : False,
                              'Range'        : 'auto',   },
                 'YAxis'   :{ 'Title'        : 'Y Value',
                              'Size'         : 0.05,
                              'Offset'       : 1.1,
                              'LabelSize'    : 0.04,
                              'Font'         : 62,
                              'Abs'          : True,
                              'Log'          : False,
                              'Range'        : 'auto'    },
                 'Legend'  :{ 'SortPara'     : 'list',
                              'Position'     : 'auto',
                              'TextSize'     : 0.03,
                              'BoxPara'      : 1,
                              'EntryList'    : ''        },
                 'Marker'  :{ 'Size'         : 1.5,
                              'Style'        : 22,
                              'Color'        : 1100      }, 
                 'Canvas'  :{ 'SizeX'        : 1280,
                              'SizeY'        : 768,
                              'PadBMargin'   : 0.15,
                              'PadLMargin'   : 0.15,
                              'MaxDigits'    : 4         },
                         
                 'Misc'    :{ 'GraphGroup'   : 'off',
                              'ColorShades'  : False,
                              'Normalization': 'off',
}

        }
        
        self.__cfg.init(pDict)    

        return True

            
    def __cfgPresent(self, fileName='default'):
        
        file_path = os.getcwd() + "/cfg"
        if os.path.exists(file_path) == False:
            return False
        else:
            if os.listdir(file_path) == []:
                return False
            for cfg in os.listdir(file_path):
                if cfg == ("%s.cfg" %(os.path.splitext(os.path.basename(os.path.normpath(fileName)))[0])):                    
                    return True
            else:
                return False



    ##################
    ### Auto Title ###
    ##################

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
            elif self.MT == "Pinhole":
                self.autotitle = "Pinhole Leakage" 
                self.autotitleY = "Current (A)"
                self.autotitleX = "Strip No"
            elif self.MT == "I_leak_dc":
                self.autotitle = "Strip Leakage Current" 
                self.autotitleY = "Current (A)"
                self.autotitleX = "Strip No"
            elif self.MT == "C_tot":
                self.autotitle = "Capacitance Voltage Characteristics" 
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "C_int":
                self.autotitle = "Interstrip Capacitance Measurement" 
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Strip No"
            elif self.MT == "CC":
                self.autotitle = "Coupling Capacitance Measurement" 
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Strip No"
            elif self.MT == "R_int":
                self.autotitle = "Interstrip Resistance Measurement" 
                self.autotitleY = "Resistance (#Omega)"
                self.autotitleX = "Strip No"
            elif self.MT == "R_poly_dc":
                self.autotitle = "Strip Resistance Measurement" 
                self.autotitleY = "Resistance (#Omega)"
                self.autotitleX = "Strip No"
            elif self.MT == "C_int_Ramp":
                self.autotitle = "Interstrip Capacitance Measurement" 
                self.autotitleY = "Capacitance (F)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "R_int_Ramp":
                self.autotitle = "Strip Resistance Measurement" 
                self.autotitleY = "Resistance (#Omega)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "I_leak_dc_Ramp":
                self.autotitle = "Interstrip Current Leakage" 
                self.autotitleY = "Current (A)"
                self.autotitleX = "Voltage (V)"
            elif self.MT == "Rpunch":
                self.autotitle = "R_{Edge} of " + self.cfgPath.replace("cfg/","").replace(".cfg","").replace("for_","for ").replace("rev_","rev ").replace("m20C","(T = -20#circC)").replace("20C","(T = 20#circC)")[15:] 
                self.autotitleY = "Current (A)"
                self.autotitleX = "Voltage (V)"
            else:
                self.autotitle = "Title" 
                self.autotitleY = "Y Value"
                self.autotitleX = "X Value"
            
        if len(self.__files) >= 2 and self.__files[0].getParaY() != None:
            if self.__files[0].getParaY() != self.__files[1].getParaY():
                sys.exit("Measurement types are not equal!")

        return True

    def checkPID(self, dataInput):
        # checks if PIDs are listed in the file
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
        ROOT.gStyle.SetTitleX(float(self.__cfg.get('Title','X0')))
        ROOT.gStyle.SetTitleY(float(self.__cfg.get('Title','Y0')))
        ROOT.gStyle.SetTitleH(float(self.__cfg.get('Title','H')))
        ROOT.gStyle.SetTitleFont(int(self.__cfg.get('Title','Font')), "")

        # Axis Options
        ROOT.gStyle.SetTitleSize(float(self.__cfg.get('XAxis','Size')), "X")
        ROOT.gStyle.SetTitleSize(float(self.__cfg.get('YAxis','Size')), "Y")
        ROOT.gStyle.SetTitleOffset(float(self.__cfg.get('XAxis','Offset')), "X")
        ROOT.gStyle.SetTitleOffset(float(self.__cfg.get('YAxis','Offset')), "Y")
        ROOT.gStyle.SetTitleFont(int(self.__cfg.get('XAxis','Font')), "X")
        ROOT.gStyle.SetTitleFont(int(self.__cfg.get('YAxis','Font')), "Y")
        ROOT.gStyle.SetLabelFont(int(self.__cfg.get('XAxis','Font')),"X")
        ROOT.gStyle.SetLabelFont(int(self.__cfg.get('YAxis','Font')),"Y")
        ROOT.gStyle.SetLabelSize(float(self.__cfg.get('XAxis','Size')),"X")
        ROOT.gStyle.SetLabelSize(float(self.__cfg.get('YAxis','Size')),"Y")
        ROOT.TGaxis.SetMaxDigits(int(self.__cfg.get('Canvas','MaxDigits')))
        
        
        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(float(self.__cfg.get('Canvas','PadBMargin')))
        ROOT.gStyle.SetPadLeftMargin(float(self.__cfg.get('Canvas','PadLMargin')))
        
        # Marker Options
        ROOT.gStyle.SetMarkerSize(float(self.__cfg.get('Marker','Size')))
        ROOT.gStyle.SetMarkerStyle(int(self.__cfg.get('Marker','Style')))
        ROOT.gStyle.SetMarkerColor(int(self.__cfg.get('Marker','Color')))
        self.LineWidth = 3

        # Pad Options
        ROOT.gStyle.SetPadGridX(True)
        ROOT.gStyle.SetPadGridY(True)

        # when reading cfg its keys are always returned as strings
        self.ColorShades = self.convertTF(self.__cfg.get('Misc','ColorShades'))
        self.absX = self.convertTF(self.__cfg.get('XAxis','Abs'))
        self.absY = self.convertTF(self.__cfg.get('YAxis','Abs'))
        self.logX = self.convertTF(self.__cfg.get('XAxis','Log'))
        self.logY = self.convertTF(self.__cfg.get('YAxis','Log'))

        KITPlot.__init = True
        return True


    def add(self, dataInput=None, measurement="probe"):

        # Load KITData
        if isinstance(dataInput, KITData.KITData):
            self.__files.append(dataInput)
            self.addGraph(dataInput.getX(),dataInput.getY())

        # Load single PID
        elif isinstance(dataInput, int):
            self.__files.append(KITData.KITData(dataInput))
            if "Ramp" in self.__files[-1].getParaY():
                print "Ramp measurement"
                self.addGraph(self.__files[-1].getZ(), self.__files[-1].getY())
            else:
                self.addGraph(self.__files[-1].getX(), self.__files[-1].getY())

        elif isinstance(dataInput, str):
            
            # Load single PID
            if dataInput.isdigit():
                self.__files.append(KITData.KITData(dataInput))
                if "Ramp" in self.__files[-1].getParaY():
                    print "Ramp measurement"
                    self.addGraph(self.__files[-1].getZ(), self.__files[-1].getY())
                else:
                    self.addNorm()

            # Load multiple data files in a folder
            elif os.path.isdir(dataInput):
                for inputFile in os.listdir(dataInput):
                    if (os.path.splitext(inputFile)[1] == ".txt"):
                        self.__files.append(KITData.KITData(dataInput + inputFile))
                    else:
                        pass

                self.arrangeFileList()
                #self.changeNames()

                self.addNorm()
                        
                        # If you open the file the data type changes from str to file 
                        # with open(dataInput + file) as inputFile:
                        #     self.__files.append(KITData.KITData(inputFile))
                        #     self.addGraph(self.__files[-1].getX(),self.__files[-1].getY())
            

            # Load file
            elif os.path.isfile(dataInput):
                # multiple PIDs
                if self.checkPID(dataInput) == True:
                    with open(dataInput) as inputFile:
                        fileList = []
                        for line in inputFile:
                            entry = line.split()
                            if entry[0].isdigit():
                                fileList.append(KITData.KITData(entry[0],measurement))
                        if measurement == "probe":
                            self.__files = fileList
                        elif measurement == "alibava":
                            self.__files.append(KITData.KITData(fileList))
                    
                    self.arrangeFileList()
                    #self.changeNames()

                    for i,File in enumerate(self.__files):
                        if "Ramp" in File.getParaY():
                            self.addGraph(File.getZ(), File.getY())
                        elif File.getParaY() is "Signal":
                            self.addGraph(File.getX(), File.getY())
                        else:
                            self.addNorm(False, i)
                        
                # Rpunch Ramp file
                elif "REdge" in dataInput:

                    data = KITData.KITData(dataInput).getDic()

                    x = []
                    y = []
                    labels = []

                    for i, bias in enumerate(data):
                        xi, yi = zip(*data[bias])
                        self.__files.append(KITData.KITData(list(xi),list(yi),str(data.keys()[i])))

                    self.addNorm()

                # singel file
                else:
                    self.__files.append(KITData.KITData(dataInput))

                    #self.changeNames()
                    self.addNorm()

                    #if "Ramp" in self.__files[-1].getParaY():
                        #self.addGraph(self.__files[-1].getZ(), self.__files[-1].getY())
                    #else:
                    #self.addGraph(self.__files[-1].getX(),self.__files[-1].getY())

        self.getUserNames()
        self.getUserOrder()
        self.MeasurementType()
        self.readEntryList()

        return True


    def addNorm(self, loop=True, j=0):

    # Sends normalized graph values to addGraph
        if loop == True:
            for i, File in enumerate(self.__files):
                if self.__files[i].includesErrors():
                     if self.__cfg.get('Misc','Normalization') == "off":
                         self.addGraph(self.__files[i].getX(),self.__files[i].getY(),self.__files[i].getdX(),self.__files[i].getdY())
                     elif self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
                         self.addGraph(self.__files[i].getX(),self.manipulate(self.__files[i].getY(),i),self.__files[i].getdX(),self.manipulate(self.__files[i].getdY(),i))
                     elif self.__cfg.get('Misc','Normalization') == "1/C^{2}": 
                         self.addGraph(File.getX(),self.manipulate(File.getY(),i),File.getdX(),self.manipulate(File.getdY(),i))
                     else:
                         sys.exit("Invalid normalization input! Try 'off', '1/C^{2}' or '[float,float,...]'!")
                else:
                                  
                    if self.__cfg.get('Misc','Normalization') == "off":
                        self.addGraph(self.__files[i].getX(),self.__files[i].getY())
                    elif self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
                        self.addGraph(self.__files[i].getX(),self.manipulate(self.__files[i].getY(),i))
                    elif self.__cfg.get('Misc','Normalization') == "1/C^{2}": 
                        self.addGraph(File.getX(),self.manipulate(File.getY(),i))
                    else:
                        sys.exit("Invalid normalization input! Try 'off', '1/C^{2}' or '[float,float,...]'!")
        else:
            if self.__cfg.get('Misc','Normalization') == "off":
                self.addGraph(self.__files[j].getX(),self.__files[j].getY())
            elif self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
                self.addGraph(self.__files[j].getX(),self.manipulate(self.__files[j].getY(),j))
            elif self.__cfg.get('Misc','Normalization') == "1/C^{2}": 
                self.addGraph(self.__files[j].getX(),self.manipulate(self.__files[j].getY(),j))
            else:
                sys.exit("Invalid normalization input! Try 'off', '1/C^{2}' or '[float,float,...]'!")
        return True



    def addGraph(self, *args):

        # args: x, y or KITData

        if isinstance(args[0], KITData.KITData):
            if KITData.KITData.getDic() == None:
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
                sys.exit("Dictinary error")



        elif len(args) == 2 and not isinstance(args[0], KITData.KITData):
            
            if self.absX:
                x = np.absolute(args[0])
            else:
                x = args[0]
            
            if self.absY:
                y = np.absolute(args[1])
            else:
                y = args[1]

        elif len(args) == 4 and not isinstance(args[0], KITData.KITData):
             
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


    def draw(self, arg="APE"):

        if len(self.__graphs) == 0:
            print "No graphs to draw"
            return False



        # init canvas
        #self.canvas = ROOT.TCanvas("c1","c1", 1280,768)
        self.canvas = ROOT.TCanvas("c1","c1", int(self.__cfg.get('Canvas','SizeX')), int(self.__cfg.get('Canvas','SizeY')))
        self.canvas.cd()

        # apply plot styles
        self.plotStyles(self.__cfg.get('XAxis','Title'), self.__cfg.get('YAxis','Title'), self.__cfg.get('Title','Title'))    
        
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

        LegH = LegHandler()
        LegH.setKITLegend(self.__cfg.get('Legend'), self.__graphs, self.__files, self.__cfg.get('Canvas','SizeX'), self.__cfg.get('Canvas','SizeY'), self.Scale)
        self.leg = LegH.getLegend()
        self.leg.Draw()
        self.canvas.Update()

        self.saveAs(self.cfgPath.replace("cfg/","").replace(".cfg",""))


        return True


    def saveAs(self, fileName):

        if not os.path.exists("output"):
            os.makedirs("output")
        self.canvas.SaveAs("output/%s.png" %(fileName))        
        self.canvas.SaveAs("output/%s.pdf" %(fileName))

    def update(self):
        
        try:
            self.canvas.Update()
        except:
            pass


    def plotStyles(self, XTitle, YTitle, Title):

        self.__graphs[0].GetXaxis().SetTitle(XTitle)
        self.__graphs[0].GetYaxis().SetTitle(YTitle)
        self.__graphs[0].SetTitle(Title)
        #self.getLegendOrder()
        
        # set titles (take auto titles when creating the cfg and the cfg value from here after)
        self.setTitles()
        # set axis ranges
        self.setRanges()
        # set marker styles (std assigning and/or graph group assigning)
        self.setMarkerStyles()
        # assign colors
        self.setGraphColor()
                
        return True


#####################
### Fancy methods ###
#####################

    def arrangeFileList(self):

        TempList1 = []
        TempList2 = []
        IDList = []
        IndexList = []

        for temp in self.__files:
            TempList1.append(temp.getName())
            TempList2.append(temp.getName())
        
        # if same name appears more than once...
        for i, Name1 in enumerate(TempList1):
            if TempList1.count(Name1) > 1:
                Test = Name1 + "_" + "(" + str(i) + ")"
                TempList2[i] = Test
                TempList1[i] = Test
            else: 
                pass
                
        TempList2.sort()
        
        for i,Name2 in enumerate(TempList2):
            if Name2 == TempList1[i]:
                IndexList.append(i)
            else:
                for j, Name in enumerate(TempList1):
                    if Name == Name2:
                        IndexList.append(j)

        TempList1[:] = []
        
        for index in IndexList:
            TempList1.append(self.__files[index])
        self.__files = TempList1


    def __autoScaling(self):
        # Get min and max value and write it into list [xmin, xmax, ymin, ymax]

        self.perc = 0.05
        ListX = [0]
        ListY = [0]

        if self.__cfg.get('Misc','Normalization')[0] == "[" and self.__cfg.get('Misc','Normalization')[-1] == "]":
            for i,inputFile in enumerate(self.__files):
                ListX += inputFile.getX()
                ListY += self.manipulate(inputFile.getY(),i)
        elif self.__cfg.get('Misc','Normalization') == "1/C^{2}":
            for i,inputFile in enumerate(self.__files):
                ListX += inputFile.getX()
                ListY += self.manipulate(inputFile.getY(),i)
        else:
            for i,inputFile in enumerate(self.__files):
                ListX += inputFile.getX()
                ListY += inputFile.getY()
        
        if self.absX:
            ListX = np.absolute(ListX)
        else:
            pass
        if self.absY:
            ListY = np.absolute(ListY)
        else:
            pass

        if self.absX:
            self.Scale.append(min(ListX)*(1.-self.perc))
            self.Scale.append(min(ListY)*(1.-self.perc))
            self.Scale.append(max(ListX)*(1.+self.perc))
            self.Scale.append(max(ListY)*(1.+self.perc))

        if not self.absX:
            self.Scale.append(min(ListX)*(1.+self.perc))
            self.Scale.append(min(ListY)*(1.-self.perc))
            self.Scale.append(max(ListX)*(1.+self.perc))
            self.Scale.append(max(ListY)*(1.+self.perc))
        
        #if (self.Scale[2]/self.Scale[3]) > 1e-4:
        #    self.logY = True

        return True


    def manipulate(self, ListY, index):
        
        FacList = []
        TempList = []
                    
        if self.__cfg.get('Misc','Normalization') == "1/C^{2}":
            for val in ListY:
                    TempList.append(1/(val*val))
        else:
            for char in self.__cfg.get('Misc','Normalization').replace("[", "").replace("]", "").split(","):
                FacList.append(float(char))
    
            if len(self.__files) != len(FacList):
                sys.exit("Invalid normalization input! Number of factors differs from the number of graphs.")
            else:
                for val in ListY:
                    TempList.append(val/FacList[index])
                    
        ListY = TempList
               
        return ListY


    def changeOrder(self, counter):

        if self.UserOrder == []:
            return counter
        else:
            for j, element in enumerate(self.UserOrder):
                if int(element) == counter:
                    return j
                else:
                    pass
        return 0


    def convertTF(self, val):
        
        if type(val) == bool:
            return val
        elif val != 'False' and val != 'True':
            sys.exit('Wrong parameter type in cfg where only boolean is allowed!')
        elif val == 'False':
            return False
        else:
            return True


    def checkTitleLenght(self, Title):
        
        # adapt title size in case it's too long
        if len(Title) > 30 and float(self.__cfg.get('Title','Y0')) <= 0.97: 
            ROOT.gStyle.SetTitleY(0.99)
            #self.__writeSpecifics(self.cfgPath, "Title", "y0", 0.99)
        else: 
            pass

        return Title



    def readEntryList(self):

        if self.cfg_initialized == True:
            self.__cfg.setParameter(self.cfgPath, 'Legend','EntryList', self.getDefaultNames())
            self.__cfg.setParameter(self.cfgPath, 'Title','Title', self.autotitle)
            self.__cfg.setParameter(self.cfgPath, 'XAxis','Title', self.autotitleX)
            self.__cfg.setParameter(self.cfgPath, 'YAxis','Title', self.autotitleY)

        #elif self.__cfgPresent() == True and self.__cfg.get('Legend','SortPara') == "list":
        elif self.__cfg.get('Legend','SortPara') == "list":

            #if cfg exists, "" can be used to reset the graph details to default
            if self.__cfg.get('Legend','EntryList') == "":
                self.__cfg.setParameter(self.cfgPath, 'Legend','EntryList', self.getDefaultNames())
                print "Entry list is set back to default!"

            #read out all the changes the user made
            else:
                if len(self.__files) != len(self.UserNames):
                    sys.exit("Lenght of entry list is not as expected!")
                else:
                    self.EntryList = self.__cfg.get('Legend','EntryList').split(",")

        #when cfg has just been created, this case will send default values
        else:
            sys.exit("Unknown error with cfg file!")

        return True

    def interpolate(self, x=None, y=None):

        v = []

        if x is not None and y is not None:
            for File in self.__files:
                m, b = np.polyfit(x, y, 1)
                v.append((m, b))

        else:
            x = []
            y = []

            for File in self.__files:
                x = File.getX()
                y = File.getY()
                name = File.getName()
                m, b = np.polyfit(x, y, 1)
                v.append((name, abs(m)))

        return v


#####################
### Legend method ###
#####################


    def setLegend(self):

        LegH = LegHandler()

        LegH.fillKITLegend(self.__cfg.get('Legend'), self.__graphs, self.__files)
        LegH.setOptions(self.__cfg.get('Legend'))
        LegH.moveLegend(int(self.__cfg.get('Canvas','SizeX')), int(self.__cfg.get('Canvas','SizeY')), self.__cfg.get('Legend'), self.__files, self.Scale)

        return LegH.getLegend()



#######################
### Set/get methods ###
#######################


    def getUserOrder(self):

        self.UserOrder = []
        List = self.__cfg.get('Legend','EntryList').split(",")
        
        if self.__cfg.get('Legend','EntryList') != "":
            for Name in List:
                if Name.replace(" ","")[1].isdigit() == False:
                    sys.exit("Wrong format in entry positions. Try '(int) name, ...'!")
                else:
                    if Name.replace(" ","")[2] == ")":
                        self.UserOrder.append(int(Name.replace(" ","")[1]))
                    elif Name.replace(" ","")[2].isdigit() == True:
                        self.UserOrder.append(int(Name.replace(" ","")[1]+Name.replace(" ","")[2]))
                    else:
                        sys.exit("Wrong format in entry positions. Try '(int) name, ...'!")
            
            for Name in self.UserOrder:
                if self.UserOrder.count(Name) > 1:
                    sys.exit("Entry positions must have different values! At least two numbers are equal!")
                elif max(self.UserOrder) > len(self.UserOrder)-1:
                    sys.exit("Unexpected entry positions! Check for skipped numbers...")
                else:
                    pass
        else:
            pass

        return True


    def getUserNames(self):

        self.UserNames = []
        List = self.__cfg.get('Legend','EntryList').split(",")
        if self.__cfg.get('Legend','EntryList') != "":
            for Name in List:
                self.UserNames.append(Name.replace(" ", "")[3:])
        else:
            pass
        return True


    def getDefaultNames(self):
        
        # write legend entries in a string
        Names = ""
        for i, graph in enumerate(self.__files):
            Names += "(" + str(i) + ")" + str(graph.getName()) + ", "
        Names = Names[:-2]        
        
        return Names


    def setRanges(self):
        
        # Scale is always filled ROOT oriantated (xmin, ymin, xmax, ymax)
        self.Scale = []
        self.__autoScaling()

        if self.__cfg.get('XAxis','Range') == "auto":
            self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[2])
        elif ":" in self.__cfg.get('XAxis','Range'):
            Temp = self.__cfg.get('XAxis','Range').split(":")
            self.Scale[0] = float(Temp[0].replace("[",""))
            self.Scale[2] = float(Temp[1].replace("]",""))
            if self.Scale[0] > self.Scale[2]:
                sys.exit("Invalid X-axis range! xmin > xmax?!")
            else:
                pass
            self.__graphs[0].GetXaxis().SetLimits(self.Scale[0],self.Scale[2])
        else:
            sys.exit("Invalid X-axis range! Try 'auto' or '[float:float]'!")
        
        if self.__cfg.get('YAxis','Range') == "auto":
            self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[1],self.Scale[3])
        elif ":" in self.__cfg.get('YAxis','Range'):
            Temp = self.__cfg.get('YAxis','Range').split(":")
            self.Scale[1] = float(Temp[0].replace("[",""))
            self.Scale[3] = float(Temp[1].replace("]",""))
            if self.Scale[1] > self.Scale[3]:
                sys.exit("Invalid Y-axis range! ymin > ymax?!")
            else:
                pass
            self.__graphs[0].GetYaxis().SetRangeUser(self.Scale[1],self.Scale[3])
        else:
            sys.exit("Invalid Y-axis range! Try 'auto' or '[float:float]'!")



    def setMarkerStyles(self):

        for i, graph in enumerate(self.__graphs):
            if "[" and "]" in self.__cfg.get('Misc','GraphGroup'):
                break
            elif self.__cfg.get('Misc','GraphGroup') == "off":
                self.__graphs[self.changeOrder(i)].SetMarkerStyle(self.getMarkerStyle(i))
            elif self.__cfg.get('Misc','GraphGroup') == "name":
                self.__graphs[self.changeOrder(i)].SetMarkerStyle(self.getMarkerShade(i))


            else:
                sys.exit("Invalid group parameter! Try 'off', 'name' or define user groups with '[...],[...],...'!")

        # User Groups
        if "[" and "]" in self.__cfg.get('Misc','GraphGroup'):
            self.getGroupList()
            j = 0

            if len(self.GroupList)-self.GroupList.count(666) != len(self.__graphs):
                sys.exit("Insufficient UserGroup. Numbers do not match!")
            else:
                pass
            for elem in self.GroupList:
                if elem == 666:
                    j = 0
                else:
                    self.__graphs[elem].SetMarkerStyle(self.getMarkerStyle(j))
                    j += 1
        else:
            pass



    def setGraphColor(self):

        for i, graph in enumerate(self.__graphs):
            if self.__cfg.get('Misc','GraphGroup') == "off" :
                self.__graphs[self.changeOrder(i)].SetMarkerColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineWidth(self.LineWidth)
                self.__graphs[self.changeOrder(i)].SetLineStyle(7)
            elif self.__cfg.get('Misc','GraphGroup') == "name" and self.ColorShades == False:
                self.__graphs[self.changeOrder(i)].SetMarkerColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineColor(self.getColor(i))
                self.__graphs[self.changeOrder(i)].SetLineWidth(self.LineWidth)
            elif self.__cfg.get('Misc','GraphGroup') == "name" and self.ColorShades == True:
                 self.__graphs[self.changeOrder(i)].SetMarkerColor(self.getColorShades(i))
                 self.__graphs[self.changeOrder(i)].SetLineColor(self.getColorShades(i))
                 self.__graphs[self.changeOrder(i)].SetLineWidth(self.LineWidth)
            elif self.__cfg.get('Misc','GraphGroup')[0] == "[" and self.__cfg.get('Misc','GraphGroup')[-1] == "]" and self.ColorShades == True:
                break
            elif self.__cfg.get('Misc','GraphGroup') == "off" and self.ColorShades == True:
                sys.exit("Need GraphGroups for applying shades!")

        # User Groups
        if "[" and "]" in self.__cfg.get('Misc','GraphGroup'):
            self.getGroupList()
            colorcount = 0
            shadecount = 0

            if len(self.GroupList)-self.GroupList.count(666) != len(self.__graphs):
                sys.exit("Insufficient UserGroup. Numbers do not match!")
            else:
                pass
            for elem in self.GroupList:
                if elem == 666:
                    colorcount += 1
                    shadecount = 0
                elif self.__cfg.get('Misc','ColorShades') == "True":
                        self.__graphs[elem].SetMarkerColor(self.colorSet[colorcount]+shadecount)
                        self.__graphs[elem].SetLineColor(self.colorSet[colorcount]+shadecount)
                        self.__graphs[elem].SetLineWidth(self.LineWidth)
                        self.__graphs[elem].SetLineStyle(7)
                        shadecount += 1
                elif self.__cfg.get('Misc','ColorShades') == "False":
                        self.__graphs[elem].SetMarkerColor(self.colorSet[colorcount])
                        self.__graphs[elem].SetLineColor(self.colorSet[colorcount])
                        self.__graphs[elem].SetLineWidth(self.LineWidth)
                        self.__graphs[elem].SetLineStyle(7)
                else:
                    pass
        else:
            pass


    def setTitles(self):

        # when the cfg has been created check for autotitle and write it into the cfg. only read out the cfg values afterwards.
        
        if self.__cfg.get('XAxis','Title') == "X Value":
            self.__graphs[0].GetXaxis().SetTitle(self.autotitleX)
            #self.__writeSpecifics(self.cfgPath, "XAxis", "title", self.autotitleX)
        else:
            self.__graphs[0].GetXaxis().SetTitle(self.__cfg.get('XAxis','Title'))

        if self.__cfg.get('YAxis','Title') == "Y Value":
            self.__graphs[0].GetYaxis().SetTitle(self.autotitleY)
            #self.__writeSpecifics(self.cfgPath, "YAxis", "title", self.autotitleY)
        else:
            self.__graphs[0].GetYaxis().SetTitle(self.__cfg.get('YAxis','Title'))

        if self.__cfg.get('Title','Title') == "Title":
            self.__graphs[0].SetTitle(self.autotitle)
            #self.__writeSpecifics(self.cfgPath, "Title", "title", self.autotitle)
        else:
            self.__graphs[0].SetTitle(self.checkTitleLenght(self.__cfg.get('Title','Title')))



    def setAxisTitleSize(self, size):

        ROOT.gStyle.SetTitleSize(size,"X")
        ROOT.gStyle.SetTitleSize(size,"Y")
        
        return True

    def setAxisTitleOffset(self, offset):

        ROOT.gStyle.SetTitleOffset(offset,"X")
        ROOT.gStyle.SetTitleOffset(offset,"Y")

        return True

    
    def getMarkerStyle(self, index):
        
        if index >= 9:
            return self.__markerSet[index % 8]
        else:
            return self.__markerSet[index]
            

    def getMarkerShade(self, index):
        
        self.getShadeList()
        MarkerShade = []
        color_num = self.ShadeList[0]
        
        for i, shade in enumerate(self.ShadeList):
            if not self.ShadeList[i]-color_num > 9:
                MarkerShade.append(self.ShadeList[i]-color_num)
            if self.ShadeList[i]-color_num > 9:
                color_num += 100
                MarkerShade.append(self.ShadeList[i]-color_num)
        
        return self.__markerSet[MarkerShade[index]]


    def getGroupList(self):
    
        self.GroupList = []
        TempList = []
        UserList = []
        for i, Element in enumerate(self.__files):
            if self.__cfg.get('Misc','GraphGroup') == "name":
                TempList.append(self.__files[i].getName()[:5])
            elif self.__cfg.get('Misc','GraphGroup') == "fluence":
                TempList.append(self.__files[i].getFluenceP())
            else:
                pass

        if self.__cfg.get('Misc','GraphGroup')[0] == "[" and self.__cfg.get('Misc','GraphGroup')[-1] == "]":
           for char in self.__cfg.get('Misc','GraphGroup'):
                if char.isdigit() == True:
                    self.GroupList.append(int(char))
                elif char == "[" or char == ",":
                    pass
                else:
                    self.GroupList.append(666)

        for i, TempElement in enumerate(TempList):
            if TempElement not in self.GroupList:
                  self.GroupList.append(TempList[i])

        return self.GroupList


#####################
### Color methods ###
#####################

    def __initColor(self):
    
#        self.colorSet = [1100,1200,1300,1400,1500,1600,1700,1800]
        self.colorSet = [1400,1500,1700,1800,1100,1200,1300,1600]

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
        
        # yellow removed because color 1900 is already taken and it looks shitty
       

        KITPlot.__init = True
        
        return True

    def getColor(self, index):
        
        KITPlot.__color = index + 1
        KITPlot.__color %= 8
        
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

    def getX(self):
        X = []
        for List in self.__files:
            X.append(List.getX())
        return X

    def getY(self):
        Y = []
        for List in self.__files:
            Y.append(List.getY())
        return Y
        
