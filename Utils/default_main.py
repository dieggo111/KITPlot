#!/usr/bin/env python3
# Mathtext doc: https://matplotlib.org/users/mathtext.html

import sys
from KITPlot import KITData
from KITPlot import KITPlot
import numpy as np
import matplotlib.pyplot as plt


if len(sys.argv) > 2:
    kPlot1 = KITPlot(sys.argv[1],sys.argv[2])
else:
    kPlot1 = KITPlot(sys.argv[1])

kPlot1.draw("matplotlib")
fig = kPlot1.getCanvas()

##### LODGERS #####
# draw horizontal line
# kPlot1.addLodger(fig,y=7,style="--",color="r0",name="test",width=2)
# draw vertical line
# kPlot1.addLodger(fig,x=5,style="-.",color="r0",name="test",width=2)
# draw xy-graph
# kPlot1.addLodger(fig,x=[0,10],y=[0,10],style=2,color="r0",name="test",width=2)
# draw text
# kPlot1.addLodger(fig,x=1,y=10,text="Test",fontsize=20)
###################

kPlot1.showCanvas()
kPlot1.saveCanvas()
input()
