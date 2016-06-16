import os,sys
import ROOT
sys.path.append('modules/LegHandler/')
import KITData 

class LegHandler(object):

    def __init__(self):

        self.legend = ROOT.TLegend(.7,.5,.98,.93)


    def getLegend(self):
        return self.legend

    def setOptions(self, dic=None):

        if dic is not None:
            self.textSize(dic['TextSize'])
            self.legend.SetFillColor(0)
        else:
            self.textSize(0.02)
            self.legend.SetFillColor(0)
        return True


    def textSize(self, TextSize):
        
        if 0.02 <= float(TextSize) <= 0.03:
            self.legend.SetTextSize(float(TextSize))
        else:
            sys.exit("Invalid legend text size! Need value between 0.02 and 0.03!")

        return True


    def fillLegend(self, graphList, nameList=None):

        for i,graph in enumerate(graphList):
            if nameList == None:
                self.legend.AddEntry(graphList[i], "graph " + str(i), "p")
            elif nameList is not None and type(nameList) == list and type(nameList[0]) == str:
                self.legend.AddEntry(graphList[i], nameList[i], "p")
            else:
                sys.exit("Unexpected name list content. Expected 'str' or 'KITData.KITData'!")
        return True


    def fillKITLegend(self, dic, graphList, fileList):
        
        self.getUserOrder(dic)
        self.getUserNames(dic)
        
        for i, graph in enumerate(graphList):
            if dic['SortPara'] == "name":
                self.legend.AddEntry(graphList[i], fileList[i].getName(), "p")
            elif dic['SortPara'] == "ID":
                self.legend.AddEntry(graphList[i], fileList[i].getID(), "p")
            elif dic['SortPara'] == "list":
                self.legend.AddEntry(graphList[self.changeOrder(i)], fileList[self.changeOrder(i)].getName(), "p")
            else:
                sys.exit("Invalid sort parameter! Try 'name', 'ID' or 'list'!")


    def setLegendParameters(self, dic, fileList, Scale):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right
        
        LegendParas = []
        para_height = 0
        para_width = 0
        TR = TL = BR = True

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
            magic_para = (para_width*0.006+0.1)*float(dic['BoxPara'])
        

        # Top right corner is the default/starting position for the legend box
        Lxmax = 0.98
        Lymax = 0.93
        Lxmin = Lxmax-magic_para
        Lymin = Lymax-para_height*0.042

        TR = self.__isInside(fileList, Lxmin, Lymin, Lxmax, Lymax, Scale)

        
        if TR == False or dic['Position'] == "TL":
            Lxmin = 0.18
            Lymax = 0.88
            Lymin = Lymax-para_height*0.04
            Lxmax = Lxmin+magic_para*1.05
            
            self.TL = self.__isInside(fileList, Lxmin, Lymin, Lxmax, Lymax, Scale)

        elif TL == TR == False or dic['Position'] == "BR":
            Lxmax = 0.89
            Lymin = 0.18
            Lxmin = Lxmax-magic_para
            Lymax = Lymin+para_height*0.04

            TB = self.__isInside(fileList, Lxmin, Lymin, Lxmax, Lymax, Scale)

        # TODO: place legend outside of frame, if there's no sufficient space
        elif dic['Position'] == "TR" or BR == TL == TR == False:
            Lxmax = 0.98
            Lymax = 0.93
            Lxmin = Lxmax-magic_para
            Lymin = Lymax-para_height*0.04
            if BR == TL == TR == False:
                print "Couldn't find sufficient space for legend!"
        
        LegendParas.append(Lxmin)
        LegendParas.append(Lymin)
        LegendParas.append(Lxmax)
        LegendParas.append(Lymax)

        return LegendParas



    def __isInside(self, fileList, Lxmin, Lymin, Lxmax, Lymax, Scale):
        
# TLegend needs percentage values from total canvas :( For 1280x7
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


    def setFillColor(self, val=0):
        if type(val) == int:
            self.legend.SetFillColor(val)
        else:
            sys.exit("Unexpected parameter type for legend fill color! Try 'int'!")
        return True

    def changeOrder(self, counter):

        for j, element in enumerate(self.UserOrder):
            if int(element) == counter:
                return j
            else:
                pass
        return 0

    def getUserOrder(self, dic):

        self.UserOrder = []
        List = dic['EntryList'].split(",")
        
        if dic['EntryList'] != "":
            for Name in List:
                if Name.replace(" ","")[1].isdigit() == False:
                    sys.exit("Wrong format in entry positions. Try '(int) name, ...'!")
                else:
                    self.UserOrder.append(int(Name.replace(" ","")[1]))

            for Name in self.UserOrder:
                if self.UserOrder.count(Name) > 1:
                        sys.exit("Entry positions must have different values! At least two numbers are equal!")
                else:
                    pass
        else:
            pass
        return True

    def getUserNames(self, dic):

        self.UserNames = []
        List = dic['EntryList'].split(",")
        if dic['EntryList'] != "":
            for Name in List:
                self.UserNames.append(Name.replace(" ", "")[3:])
        else:
            pass
        return True


    def moveLegend(self, legend, canvasX, canvasY, dic, fileList, Scale):

        ParaList = self.setLegendParameters(dic, fileList, Scale)
        print ParaList
        #legend.SetBBoxY2(100)
        #legend.SetBBoxX1(int(canvasX*ParaList[0]))      # moves left edge to the left
        #legend.SetBBoxX2(int(canvasX*ParaList[1]))      # moves right edge to the right
        #legend.SetBBoxY1(int(canvasY*ParaList[2]))      # moves top edge to the top
        #legend.SetBBoxY2(int(canvasY*ParaList[3]))      # moves bottom edge to the bottom

        return 





