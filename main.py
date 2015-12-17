import sys
import numpy as np
from ROOT import *
from KITDataFile import KITDataFile
from KITPlot import KITPlot


file1 = kitDataFile(sys.argv[1])
file2 = kitDataFile(sys.argv[2])

kPlot = kitPlot()
kPlot2 = kitPlot()

g1 = TGraph(len(file1.getX()),file1.getX(1),file1.getY(1))
g2 = TGraph(len(file1.getX()),file1.getX(1),file1.getZ(1))
g1.SetMarkerColor(1100)
g2.SetMarkerColor(1200)
g3 = TGraph(len(file2.getX()),file2.getX(1),file2.getY(1))
g3.SetMarkerColor(1300)

y2 = [x + y for x, y in zip(file1.getY(), file1.getZ())]
g4 = TGraph(len(file1.getX()),file1.getX(1),np.asarray(y2))
g4.SetMarkerColor(1400)

c1 = TCanvas("c1","c1",1280,768)
c1.cd()

g2.Draw("AP")
g1.Draw("PSAME")
g3.Draw("PSAME")
g4.Draw("PSAME")

c1.SaveAs("test.pdf")
    
