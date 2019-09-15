#!/usr/bin/env python3
# Mathtext doc: https://matplotlib.org/users/mathtext.html
from argparse import ArgumentParser
from KITPlot import KITPlot
import numpy

PARSER = ArgumentParser()
PARSER.add_argument("filename")
PARSER.add_argument("-s", "--split_graph",
                    help="Internally split the data so that every line in "
                         "file is interpreted as a graph",
                    action="store_true")
PARSER.add_argument("-r", "--reset_legend",
                    help="Automatically resets the entries of the legend",
                    action="store_true")
PARSER.add_argument("-n", "--name",
                    help="Make first argument to base name",
                    action="store_true")
PARSER.add_argument("-cfg",
                    help="Use parameters from this specific cfg file",
                    default=None)
PARSER.add_argument("-def_cfg", "--defaultCfg",
                    help="Use this file as the default cfg file",
                    default=None)
PARSER.add_argument("-al", "--auto_labeling",
                    help="Enabels automatical labeling of axes when data "
                         "comes from DB",
                    default=True)

KWARGS = vars(PARSER.parse_args())
INPUT = KWARGS.pop("filename")
KPLOT1 = KITPlot(**KWARGS)

KPLOT1.addFiles(INPUT)

KPLOT1.draw()

###### FIT #######
# x = []
# y = []
# for x_lst, y_lst in zip(KPLOT1.getX(), KPLOT1.getY()):
#      x.append(x_lst[0])
#      y.append(y_lst[0])
# print(x)
# print(y)
# f, t = KPLOT1.get_fit(
#      [x, y], data_opt="listwise", fit_opt="linear",
#      residual=True, returns="fit")
# print(f, t)

##### LODGERS #####
fig = KPLOT1.getCanvas()
# draw horizontal line
# KPLOT1.addLodger(fig,y=12000, style="-", color="r0",name="test", width=6, alpha=0.3)
# draw vertical line
# KPLOT1.addLodger(fig, x=20, style="-", color="r0", name="test", width=6, alpha=0.3)
# draw xy-graph
# KPLOT1.addLodger(fig, x=t, y=f, style="-", color="r0", name="fit", width=2)
# draw text
# KPLOT1.addLodger(fig, x=1, y=10, text="Test", fontsize=20)
# KPLOT1.addLodger(fig, x=10e14, y=0.0146, text="$\\alpha = x \\pm x \\cdot 10^{-17}$ Acm$^{-1}$",
#                  fontsize=12, opt_dict={"bbox" : dict(facecolor='gray', alpha=0.5)})
####################################################
KPLOT1.showCanvas(save=True)
####################################################
