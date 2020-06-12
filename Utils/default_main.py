#!/usr/bin/env python3
# Mathtext doc: https://matplotlib.org/users/mathtext.html
from argparse import ArgumentParser
from KITPlot import KITPlot
import numpy as np
import numpy.polynomial.polynomial as poly

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
PARSER.add_argument("-hist", "--histogram",
                    help="Plot data points in histogramm",
                    action="store_true")
PARSER.add_argument("-old", "--old_db",
                    help="Search in new DB",
                    action="store_true",
                    default=False)
#PARSER.add_argument("-old", "--old_db",
#                    help="Search in old DB",
#                    action="store_true",
#                    default=False)


KWARGS = vars(PARSER.parse_args())
INPUT = KWARGS.pop("filename")
KPLOT1 = KITPlot(**KWARGS)

KPLOT1.addFiles(INPUT)

KPLOT1.draw()

FIG = KPLOT1.getCanvas()

###### FIT #######
# ...

# x_new = list(x_new)
##### LODGERS #####
# draw horizontal line
# KPLOT1.addLodger(FIG, y=1000, style="--", color="r0",name="test", width=6, alpha=0.3)
# draw vertical line
# KPLOT1.addLodger(FIG, x=669, style="--", color="r0", name="test", width=2, alpha=0.3)
# draw xy-graph
# KPLOT1.addLodger(FIG, x=t, y=f, style="-", color="r0", name="fit", width=2)
# draw text
# KPLOT1.addLodger(FIG, x=46.48e-12, y=60, text="awd",
#                  fontsize=12, opt_dict={"bbox" : dict(facecolor='gray', alpha=0.5)})
# draw rectangel
# KPLOT1.addLodger(FIG, x=0, y=0.6, color="bl3", alpha=0.3, opt_dict=dict(width=110.5, height=0.2))
####################################################
KPLOT1.showCanvas(save=True)
####################################################
