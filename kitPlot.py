import numpy as np
from ROOT import *

class kitPlot():

    def __init__(self, plot, x, y):
        
        self.__initStyle()

        if plot == "TGraph":
            self.__graph = TGraph(len(x), np.asarray(x),np.asarray(y))

    def __initStyle(self):

        # Title Options
        gStyle.SetTitleX(0.5)
        gStyle.SetTitleY(0.97)
        gStyle.SetTitleH(0.05)
        
        # Axis Options
        gStyle.SetTitleSize(0.05,"X")
        gStyle.SetTitleSize(0.05,"Y")
        gStyle.SetTitleOffset(1.3,"X")
        gStyle.SetTitleOffset(1.2,"Y")
        
        gStyle.SetLabelSize(0.05,"X")
        gStyle.SetLabelSize(0.05,"Y")
        
        # Canvas Options
        gStyle.SetPadBottomMargin(0.15)
        gStyle.SetPadLeftMargin(0.15)
        
        # Legend Options
        gStyle.SetLegendTextSize(0.035)
        
        # Marker Options
        gStyle.SetMarkerSize(1.5)
        gStyle.SetMarkerStyle(3)

        # Pad Options
        gStyle.SetPadGridX(True)
        gStyle.SetPadGridY(True)

    def setAxisTitleSize(self, size):

        gStyle.SetTitleSize(size,"X")
        gStyle.SetTitleSize(size,"Y")
        
        return True

    def setAxisTitleOffset(self, offset):
        
        gStyle.SetTitleOffset(offset,"X")
        gStyle.SetTitleOffset(offset,"Y")

    def Draw(self, argument):
        self.__graph.Draw(argument)

    def getGraph():
        return self._graph



    
