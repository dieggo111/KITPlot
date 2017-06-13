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

#        self.legend.SetHeader("f1")

        return True


    def changeOrder(self, counter):

        for i, key in enumerate(self.__EntryList):
            if int(key) == counter:
                return i
            else:
                pass

        return 0


    def setLegendParameters(self, dic, fileList, Scale):
        """ Evaluates the legend position and writes it into list [Lxmin,
        Lymin, Lxmax, Lymax]. Valid positions are top right (TR), top left (TL)
        and bottom right (BR).

        Args:
            dic (dictinoary):   ...
            fileList (list):    list containing KITData files
            Scale (list):       list containing the scaling (lower and upper
                                limit) of x- and y-axis

        """

        LegendParas = []
        TR = TL = BR = False

        # para_height is determined by the number of entries. It
        # determines the height of the legend box
        para_height = len(fileList)*float(dic['TextSize']) \
                      + float(dic['TextSize']) + len(fileList)*0.01

        # para_width determines the width of the legend box based on the
        # longest entry and the 'BoxParameter'
        para_width = self.getWidth(fileList,
                                   float(dic['TextSize']),
                                   float(dic['BoxPara']))

        # consider some ugly stuff
        if para_width > 30:
            raise ValueError("Legend name too long! Reduce the number of characters!")
        # elif not 0.5 <= float(dic['BoxPara']) <= 1.5:
        #     raise ValueError("Invalid box parameter! Value must be "
        #              "between 0.5 and 1.5!")
        elif (dic['Position'] != "auto" and dic['Position'] != "TR"
                and dic['Position'] != "TL" and dic['Position'] != "BR"):
            raise ValueError("Invalid legend position! Try 'auto', 'TR', "
                             "'TL' or 'BR'!")
        else:
            pass

        # magic_para .... it's magic!
        if float(dic['TextSize']) == 0.03:
            magic_para_width = 0
        else:
            magic_para_width = 0
        if float(dic['TextSize']) == 0.03:
            magic_para_height = 0
        else:
            magic_para_height = 0

        # Default/starting position for the legend box
        TRxmax = 0.89
        TRymax = 0.88
        TRxmin = TRxmax - para_width - magic_para_width
        TRymin = TRymax - para_height - magic_para_height

        TLxmin = 0.18
        TLymax = 0.88
        TLxmax = TLxmin + para_width + magic_para_width
        TLymin = TLymax - para_height - magic_para_height

        BRxmax = 0.89
        BRymin = 0.18
        BRxmin = BRxmax - para_width - magic_para_width
        BRymax = BRymin + para_height + magic_para_height

        Oxmax = 0.98
        Oymax = 0.93
        Oxmin = Oxmax-magic_para_width
        Oymin = Oymax-magic_para_height

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

# TLegend needs percentage values from total canvas :( For 1280x768
###################################################################### =
#                       CANVAS                                       # |
#                                                                    # 0.1
#       ######################################################       # =
#       #                                                    #       # |
#       #                                                    #       # |
#       #                                                    #       # |
#       #                                                    #       # |
#       #               FRAME                                #       # |
#       #                                                    #       # 0.75
#       #                                                    #       # |
#       #                                                    #       # |
#       #                                                    #       # |
#       #                                                    #       # |
#       #                             x                      #       # |
#       #                                                    #       # |
#       ######################################################       # =
#       |-----x/(xmax-xmin)-----------|                              # |
#|---------x/(xmax-xmin)*0.75+0.15----|                              # 0.15
#                                                                    # |
################################# #################################### =
#|-0.15-|------------------------0.75------ --------------------------|--0.1---|


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

    def getWidth(self, fileList, text, box):

        length = 0
        para = 0

        for File in fileList:
            if len(File.getName()) > length:
                # length of graph name
                Long = len(File.getName())
                # lenght of graph name without narrow characters
                Short = len(File.getName().replace("i","").replace("I","")\
                            .replace("j","").replace("r","").replace("l","")\
                            .replace("t",""))
                if Short > length:
                    wide_chr = Short            # number of wide chars
                    nar_chr = Long-Short        # number of narrow chars
                else:
                    pass
            else:
                pass

        para = (wide_chr*(text - 0.013)*box + nar_chr*0.5*text)

        return para
