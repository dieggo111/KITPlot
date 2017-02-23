import os,sys
import ROOT
from ..kitdata import KITData

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
        
        if 0.02 <= float(TextSize) <= 0.05:
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

        self.__EntryList = dic['EntryList']

        for i, graph in enumerate(graphList):
            if dic['SortPara'] == "name":
                self.legend.AddEntry(graphList[i], fileList[i].getName(), "p")
            elif dic['SortPara'] == "ID":
                self.legend.AddEntry(graphList[i], fileList[i].getID(), "p")
            elif dic['SortPara'] == "list":
                self.legend.AddEntry(graphList[self.changeOrder(i)], self.__EntryList[str(list(self.__EntryList)[self.changeOrder(i)])], "p")
            else:
                sys.exit("Invalid sort parameter! Try 'name', 'ID' or 'list'!")


    def changeOrder(self, counter):

        for i, key in enumerate(self.__EntryList):
            if int(key) == counter:
                return i
            else:
                pass

        return 0


    def setLegendParameters(self, dic, fileList, Scale):
        # Evaluate Legend Position and write it into list [Lxmin, Lymin, Lxmax, Lymax]. Try top right, top left, bottom right
        
        LegendParas = []
        TR = TL = BR = False

        # para_height contains the number of entries and determines the height of the legend box
        para_height = len(fileList)

        # para_width determines the width of the legend box based on the longest entry
        para_width = self.getWidth(fileList)

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
            magic_para = (0.03+para_width*0.014)*float(dic['BoxPara'])
        

        # Default/starting position for the legend box
        TRxmax = 0.89
        TRymax = 0.88
        TRxmin = TRxmax-magic_para
        TRymin = TRymax-para_height*0.042

        TLxmin = 0.18
        TLymax = 0.88
        TLymin = TLymax-para_height*0.04
        TLxmax = TLxmin+magic_para*1.05

        BRxmax = 0.89
        BRymin = 0.18
        BRxmin = BRxmax-magic_para
        BRymax = BRymin+para_height*0.04

        Oxmax = 0.98
        Oymax = 0.93
        Oxmin = Oxmax-magic_para
        Oymin = Oymax-para_height*0.042

        # check if graphs are in box
        TR = self.__isInside(fileList, TRxmin, TRymin, TRxmax, TRymax, Scale)
        TL = self.__isInside(fileList, TLxmin, TLymin, TLxmax, TLymax, Scale)
        BR = self.__isInside(fileList, BRxmin, BRymin, BRxmax, BRymax, Scale)

        # apply legend parameters
        if dic['Position'] in ["TR", "BR", "TL"]:
            TR = TL = BR = False
        else:
            pass

        if TR == True or dic['Position'] == "TR":
            LegendParas.append(TRxmin)
            LegendParas.append(TRymin)
            LegendParas.append(TRxmax) 
            LegendParas.append(TRymax)
        elif TR == False and TL == True or dic['Position'] == "TL":
            LegendParas.append(TLxmin)
            LegendParas.append(TLymin) 
            LegendParas.append(TLxmax) 
            LegendParas.append(TLymax)
        elif TL == TR == False and BR == True or dic['Position'] == "BR":
            LegendParas.append(BRxmin) 
            LegendParas.append(BRymin) 
            LegendParas.append(BRxmax) 
            LegendParas.append(BRymax)
        else:
            # TODO: place legend outside of frame, if there's no sufficient space
            LegendParas.append(Oxmin)
            LegendParas.append(Oymin)
            LegendParas.append(Oxmax) 
            LegendParas.append(Oymax)
            print("Couldn't find sufficient space for legend!")

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





#    def moveLegend(self, canvasX, canvasY, dic, fileList, Scale):

#        ParaList = self.setLegendParameters(dic, fileList, Scale)
#        print ParaList
#        self.legend.SetBBoxX1(640)
#        #legend.SetBBoxX1(int(canvasX*ParaList[0]))      # moves left edge to the left
#        #legend.SetBBoxX2(int(canvasX*ParaList[1]))      # moves right edge to the right
#        #legend.SetBBoxY1(int(canvasY*ParaList[2]))      # moves top edge to the top
#        #legend.SetBBoxY2(int(canvasY*ParaList[3]))      # moves bottom edge to the bottom

#        return True


    def setKITLegend(self, dic, graphList, fileList, canvasX, canvasY, Scale):

        ParaList = self.setLegendParameters(dic, fileList, Scale)

        self.legend = ROOT.TLegend(ParaList[0], ParaList[1], ParaList[2], ParaList[3])
        self.fillKITLegend(dic, graphList, fileList)
        self.setOptions(dic)
        
        return True

    def getWidth(self, fileList):

        para = 0

        for File in fileList:
            if len(File.getName()) > para:
                Long = len(File.getName())
                Short = len(File.getName().replace("i","").replace("I","").replace("j","").replace("r","").replace("l","").replace("t","")) 
                if Short > para:
                    para = Short            # number of wide chars
                    dif = Long-Short        # number of narrow chars
                else:
                    pass
            else:
                pass

        para = int(para + 0.5*dif)

        return para


