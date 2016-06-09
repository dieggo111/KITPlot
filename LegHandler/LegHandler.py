import os,sys
import ROOT
sys.path.append('modules/LegHandler/')
import KITData 

class LegHandler(object):

    def __init__(self, dic, graphList, fileList):

        #self.legend = ROOT.TLegend(self.LegendParas[0],self.LegendParas[1],self.LegendParas[2],self.LegendParas[3])
        self.legend = ROOT.TLegend(0.75,0.75,0.9,0.9)
        self.legend.SetFillColor(0)
        self.__textSize(float(dic['TextSize']))
        self.__fillLegend(dic['SortPara'], graphList, fileList)

    def getLegend(self):
        return self.legend

    def __textSize(self, TextSize):
        
        if 0.02 <= TextSize <= 0.03:
            self.legend.SetTextSize(TextSize)
        else:
            sys.exit("Invalid legend text size! Need value between 0.02 and 0.03!")

        return True


    def __fillLegend(self, SortPara, graphList, fileList):

        for i,graph in enumerate(graphList):
            if SortPara == "name":
                self.legend.AddEntry(graphList[i], fileList[i].getName(), "p")
            elif SortPara == "ID":
                self.legend.AddEntry(graphList[i], fileList[i].getID(), "p")
            elif SortPara == "list":
                #print fileList[i].getName()
                self.legend.AddEntry(graphList[i], fileList[i].getName(), "p")
            #elif SortPara == "list":
            #    self.legend.AddEntry(graphList[self.changeOrder(i)], self.graphDetails[self.changeOrder(i)].replace(" ","")[3:], "p")
            else:
                sys.exit("Invalid SortPara! Try 'name', 'ID' or 'list'!")
        
        return True
        

    def setLegendParameters(self):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right or outside
        # Plot is arround 80% of canvas from (0.1,0.15) to (0.9,0.9). 
        
        self.LegendParas = []
        para_height = 0
        para_width = 0
        self.TopRight = self.TopLeft = self.BottomRight = True
        
        # para_height contains the number of entries and determines the height of the legend box
        para_height = len(fileList)

        # para_width contains the lenght of the longest entry
        for Name in self.graphDetails:
            if len(Name) > para_width:
                para_width = len(Name)
            else:
                pass

        # hold off some errors
        if para_width > 30:
                sys.exit("Legend name too long! Reduce the number of characters!")
        elif not 0.5 <= self.legendBoxPara <= 1.5:
            sys.exit("Invalid box parameter! Value must be between 0.5 and 1.5!")
        else:
            pass
        
        # magic_para .... it's magic!
        if self.legendTextSize == 0.02:
            magic_para = para_width/100.*self.legendBoxPara
        else:
            magic_para = para_width*0.0105*self.legendBoxPara
        
        
        if self.legendPosition != "auto" and self.legendPosition != "TR" and self.legendPosition != "TL" and self.legendPosition != "BR":
            sys.exit("Invalid legend position! Try 'auto', 'TR', 'TL' or 'BR'!")
        
        # Top right corner is the default/starting position for the legend box
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-magic_para
        Lymin = Lymax-para_height*0.04
            
            
        # Check if elements are in the top right corner. 
        for i in range(len(fileList)):
            for j in range(len(fileList[i].getX())):
                if abs(fileList[i].getX()[j]/(self.xmax*(1.+self.perc)))-0.1 > Lxmin and self.legendPosition == "auto":
                    if abs(fileList[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin:
                        self.TopRight = False
        
        if self.TopRight == False or self.legendPosition == "TL":
            Lxmin = 0.18
            Lymax = 0.88
            Lymin = Lymax-para_height*0.04
            Lxmax = Lxmin+magic_para*1.05

        # Check if elements are in the top left corner.
        for i in range(len(fileList)):
            for j in range(len(fileList[i].getX())):
                if Lxmin-0.1 < abs(fileList[i].getX()[j]/(self.xmax*(1.+self.perc))) < Lxmax+0.05:
                    if abs(fileList[i].getY()[j]/(self.ymax*(1.+self.perc))) > Lymin+0.08 and self.legendPosition == "auto":
                        self.TopLeft = False
                
        if self.TopLeft == self.TopRight == False or self.legendPosition == "BR":
            Lxmax = 0.89
            Lymin = 0.18
            Lxmin = Lxmax-magic_para
            Lymax = Lymin+para_height*0.04
            
        # If the plot is too crowded, create more space on the right.
        for i in range(len(fileList)):
            for j in range(len(fileList[i].getX())):
                if abs(fileList[i].getX()[j]/(self.xmax*(1.+self.perc))) > Lxmin:
                    if abs(fileList[i].getY()[len(fileList[i].getY())-1]/(self.ymax*(1.+self.perc))) < Lymax and self.legendPosition == "auto":
                        self.BottomRight = False
            
            
        if self.legendPosition == "TR" or self.BottomRight == self.TopLeft == self.TopRight == False:
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-magic_para
            Lymin = Lymax-para_height*0.04
            if self.BottomRight == self.TopLeft == self.TopRight == False:
                print "Couldn't find sufficient space!"
        
        self.LegendParas.append(Lxmin)
        self.LegendParas.append(Lymin)
        self.LegendParas.append(Lxmax)
        self.LegendParas.append(Lymax)


####################################################
    def getLegendOrder(self):

        self.EntryPosition = []

        for Name in self.graphDetails:
            self.EntryPosition.append(Name.replace(" ","")[1])
        
        for Name in self.EntryPosition:
            if self.EntryPosition.count(Name) > 1:
                    sys.exit("Entry positions must have different values! At least two numbers are equal!")
            else:
                pass


    def changeOrder(self, counter):

        for j, number in enumerate(self.EntryPosition):
            
            if int(number) == counter:
                return int(j)
            else:
                pass

        return 0
        
       
