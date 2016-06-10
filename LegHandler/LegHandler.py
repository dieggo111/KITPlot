import os,sys
import ROOT
sys.path.append('modules/LegHandler/')
import KITData 

class LegHandler(object):

    def __init__(self, dic, graphList, fileList, Scale):

        self.setLegendParameters(dic, fileList, Scale)
        self.legend = ROOT.TLegend(self.LegendParas[0],self.LegendParas[1],self.LegendParas[2],self.LegendParas[3])
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
                self.legend.AddEntry(graphList[i], fileList[i].getName(), "p")
            #elif SortPara == "list":
            #    self.legend.AddEntry(graphList[self.changeOrder(i)], self.graphDetails[self.changeOrder(i)].replace(" ","")[3:], "p")
            else:
                sys.exit("Invalid SortPara! Try 'name', 'ID' or 'list'!")
        
        return True
        

    def setLegendParameters(self, dic, fileList, Scale):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right
        
        self.LegendParas = []
        para_height = 0
        para_width = 0
        self.TR = self.TL = self.BR = True

        # para_height contains the number of entries and determines the height of the legend box
        para_height = len(fileList)

        # para_width contains the lenght of the longest entry
        for File in fileList:
        #for Name in self.graphDetails:
            if len(File.getName()) > para_width:
                para_width = len(File.getName())
            else:
                pass

        # consider some ugly stuff
        if para_width > 30:
                sys.exit("Legend name too long! Reduce the number of characters!")
        elif not 0.5 <= float(dic['BoxPara']) <= 1.5:
            sys.exit("Invalid box parameter! Value must be between 0.5 and 1.5!")
        elif dic['Position'] != "auto" and dic['Position'] != "TR" and dic['Position'] != "TL" and dic['Position'] != "BR":
            sys.exit("Invalid legend position! Try 'auto', 'TR', 'TL' or 'BR'!")
        else:
            pass
        
        # magic_para .... it's magic!
        if float(dic['TextSize']) == 0.02:
            magic_para = para_width/100.*float(dic['BoxPara'])
        else:
            magic_para = (para_width*0.005+0.1)*float(dic['BoxPara'])
        

        # Top right corner is the default/starting position for the legend box
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-magic_para
        Lymin = Lymax-para_height*0.042

        self.TR = self.__isInside(fileList, Lxmin, Lymin, Lxmax, Lymax, Scale)

        
        if self.TR == False or dic['Position'] == "TL":
            Lxmin = 0.18
            Lymax = 0.88
            Lymin = Lymax-para_height*0.04
            Lxmax = Lxmin+magic_para*1.05
            
            self.TL = self.__isInside(fileList, Lxmin, Lymin, Lxmax, Lymax, Scale)

        elif self.TL == self.TR == False or dic['Position'] == "BR":
            Lxmax = 0.89
            Lymin = 0.18
            Lxmin = Lxmax-magic_para
            Lymax = Lymin+para_height*0.04

            self.TB = self.__isInside(fileList, Lxmin, Lymin, Lxmax, Lymax, Scale)

        # TODO: place legend outside of frame, if there's no sufficient space
        elif dic['Position'] == "TR" or self.BR == self.TL == self.TR == False:
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-magic_para
            Lymin = Lymax-para_height*0.04
            if self.BR == self.TL == self.TR == False:
                print "Couldn't find sufficient space for legend!"
        
        self.LegendParas.append(Lxmin)
        self.LegendParas.append(Lymin)
        self.LegendParas.append(Lxmax)
        self.LegendParas.append(Lymax)

        return True



    def __isInside(self, fileList, Lxmin, Lymin, Lxmax, Lymax, Scale):
        
# TLegend needs percentage values from total canvas :(
######################################################################################### =
#                       CANVAS                                                          # |
#                                                                                       # 0.1
#       #########################################################################       # =
#       #                                                                       #       # |
#       #                                                                       #       # |
#       #                                                                       #       # |
#       #                                                                       #       # |
#       #               FRAME                                                   #       # |
#       #                                                                       #       # 0.75
#       #                                                                       #       # |
#       #                                                                       #       # |
#       #                                                                       #       # |
#       #                                                                       #       # |
#       #                             x                                         #       # |
#       #                                                                       #       # |
#       #########################################################################       # =
#       |-----x/(xmax-xmin)-----------|                                                 # |
#|---------x/(xmax-xmin)*0.75+0.15----|                                                 # 0.15
#                                                                                       # |
######################################################################################### =
#|-0.15-|------------------------0.75--------------------------------------------|--0.1---|


        check = True

        # check if points are inside the legend box
        for File in fileList:
            PercX = []
            PercY = []
            for i, valX in enumerate(File.getX()):
                PercX.append(0.15+abs(0.75*valX/(Scale[2]-Scale[0])))
                PercY.append(0.15+abs(0.75*File.getY()[i]/(Scale[3]-Scale[1])))
            for i, x in enumerate(PercX):
                if Lxmin < x < Lxmax:
                    if Lymin < PercY[i] < Lymax:
                        check = False
                    else:
                        pass
                else:
                    pass
        return check



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
        
       
