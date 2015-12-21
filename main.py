import sys
import numpy as np
import ROOT 
from KITDataFile import KITDataFile
from KITPlot import KITPlot

file1 = KITDataFile(sys.argv[1])

kPlot1 = KITPlot(file1.getX(),file1.getY())




#g1.GetXaxis().SetRangeUser(file1.getScaleX)
#g1.GetYaxis().SetRangeUser(file1.getScaleY)  
	





#g1.SetTitle("IV-Curve")


#kPlot1.initCanvas()


#c1.SaveAs("test.pdf")
    
raw_input()
