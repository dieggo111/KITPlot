import numpy as np
import ROOT

class kitPlot():

    def __init__(self, plot=None, x=[], y=[]):
        
        self.__initStyle()

        if plot == "TGraph":
            self.__graph = ROOT.TGraph(len(x), np.asarray(x),np.asarray(y))
        else:
            pass
            


    def __initStyle(self):

        # Title Options
        ROOT.gStyle.SetTitleX(0.5)
        ROOT.gStyle.SetTitleY(0.97)
        ROOT.gStyle.SetTitleH(0.05)
        
        # Axis Options
        ROOT.gStyle.SetTitleSize(0.05,"X")
        ROOT.gStyle.SetTitleSize(0.05,"Y")
        ROOT.gStyle.SetTitleOffset(1.3,"X")
        ROOT.gStyle.SetTitleOffset(1.2,"Y")
        
        ROOT.gStyle.SetLabelSize(0.05,"X")
        ROOT.gStyle.SetLabelSize(0.05,"Y")
        
        # Canvas Options
        ROOT.gStyle.SetPadBottomMargin(0.15)
        ROOT.gStyle.SetPadLeftMargin(0.15)
        
        # Legend Options
        ROOT.gStyle.SetLegendTextSize(0.035)
        
        # Marker Options
        ROOT.gStyle.SetMarkerSize(1.5)
        ROOT.gStyle.SetMarkerStyle(3)

        # Pad Options
        ROOT.gStyle.SetPadGridX(True)
        ROOT.gStyle.SetPadGridY(True)

        return True

    def setAxisTitleSize(self, size):

        ROOT.gStyle.SetTitleSize(size,"X")
        ROOT.gStyle.SetTitleSize(size,"Y")
        
        return True

    def setAxisTitleOffset(self, offset):

        ROOT.gStyle.SetTitleOffset(offset,"X")
        ROOT.gStyle.SetTitleOffset(offset,"Y")

        return True

    def Draw(self, argument):
        self.__graph.Draw(argument)
        
        return True

    def getGraph():
        return self._graph



    
