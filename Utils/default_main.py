#!/usr/bin/env python3
# Mathtext doc: https://matplotlib.org/users/mathtext.html
from argparse import ArgumentParser
from KITPlot import KITPlot


PARSER = ArgumentParser()
PARSER.add_argument("filename")
PARSER.add_argument("-s", "--split_graph",
                    help="Internally split the data so that every line in "
                         "file is interpreted as a graph",
                    action="store_true")
PARSER.add_argument("-r", "--reset_legend",
                    help="Automatically resets the entries of the legend",
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
# kPlot1.addFiles([46609, 46607, 46493], name="Alibava_2")
# kPlot1.addFiles([51150, 49557, 49427, 50999, 49305, 50269, 49363, 49319, 50144], name="FZ290_IV_620h")
# kPlot1.addFiles([50507,50429], name="Baby_IV_comp")
# kPlot1.addFiles([50611,50580], name="Baby_IV_comp2")
# kPlot1.addFiles([48146, 48079, 48077, 48144, 50645, 50647, 50659, 50643], name="Irradiation_IV_comp_5e14")

KPLOT1.draw()

###### FIT #######
# x = []
# y = []
# for x_lst, y_lst in zip(kPlot1.getX(), kPlot1.getY()):
#     x.append(x_lst[0])
#     y.append(y_lst[0])
# f, t = kPlot1.get_fit(
#     [x, y], data_opt="listwise", fit_opt="linear",
#     residual=True, returns="fit")

##### LODGERS #####
# fig = kPlot1.getCanvas()
# draw horizontal line
# KPLOT1.addLodger(fig,y=8400,style="-",color="r0",name="test",width=2,alpha=0.3)
# draw vertical line
# KPLOT1.addLodger(fig, x=180, style="-", color="b0", name="test", width=6)
# draw xy-graph
# KPLOT1.addLodger(fig, x=t, y=f, style=2, color="r0", name="fit", width=2)
# draw text
# KPLOT1.addLodger(fig, x=1, y=10, text="Test", fontsize=20)
# KPLOT1.addLodger(fig, x=10e14, y=0.0146, text="$\\alpha$ = -4.295e-17",
#                  fontsize=16, opt_dict={"bbox" : dict(facecolor='red', alpha=0.5)})
####################################################
KPLOT1.showCanvas(save=True)
####################################################
