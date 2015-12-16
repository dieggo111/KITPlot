import sys
from ROOT import *
from kitDataFile import kitDataFile
from kitPlot import kitPlot

file1 = kitDataFile(sys.argv[1])

kPlot = kitPlot()
g1 = TGraph(len(file1.getX()),file1.getX(1),file1.getY(1))
g2 = TGraph(len(file1.getX()),file1.getX(1),file1.getZ(1))


c1 = TCanvas("c1","c1",1280,768)
c1.cd()

c1.SetLogy()

g2.Draw("AP")
g1.Draw("SAME")

c1.SaveAs("test.png")
    
