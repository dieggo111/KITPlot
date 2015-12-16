import sys
from ROOT import *
from kitDataFile import kitDataFile
from kitPlot import kitPlot

file1 = kitDataFile(sys.argv[1])

kPlot = kitPlot("TGraph", file1.getX(), file1.getY())

c1 = TCanvas("c1","c1",1280,768)
c1.cd()

kPlot.Draw("AP")
c1.SaveAs("test.png")
    
