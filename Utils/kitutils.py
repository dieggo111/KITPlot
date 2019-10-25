""" Utility methods
"""
#pylint: disable=C0103,C0330,C0326
from collections import OrderedDict
import numpy as np
from KITPlot import KITData

def get_KITcolor():

    KITcolor = OrderedDict([
                       ("KITred"    , OrderedDict([
                                    ("r0" , (191./255, 35./255, 41./255)),
                                    ("r1" , (205./255, 85./255, 75./255)),
                                    ("r2" , (220./255, 130./255, 110./255)),
                                    ("r3" , (255./255, 85./255, 75./255)),
                                    ("r4" , (255./255, 0./255, 0./255)),
                                    ("r5" , (210./255, 0./255, 0./255)),
                                    ("r6" , (140./255, 0./255, 0./255)),
                                    ("r7" , (80./255, 0./255, 0./255))
                                    ])),
                       ("KITgreen"  , OrderedDict([
                                    ("g0" ,  (0./255, 169./255, 144./255)),
                                    ("g1" ,  (75./255, 195./255, 165./255)),
                                    ("g2" ,  (125./255, 210./255, 185./255)),
                                    ("g3" ,  (180./255, 230./255, 210./255)),
                                    ("g4" ,  (215./255, 240./255, 230./255)),
                                    ("g5" ,  (0./255, 119./255, 94./255)),
                                    ("g6" ,  (0./255, 70./255, 70./255))
                                    ])),
                       ("KITorange" , OrderedDict([
                                    ("o0" ,  (247./255, 145./255, 16./255)),
                                    ("o1" ,  (249./255, 174./255, 73./255)),
                                    ("o2" ,  (251./255, 195./255, 118./255)),
                                    ("o3" ,  (252./255, 218./255, 168./255)),
                                    ("o4" ,  (254./255, 236./255, 211./255))
                                    ])),
                       ("KITblue"   , OrderedDict([
                                    ("b0" ,  (67./255, 115./255, 193./255)),
                                    ("b1" ,  (118./255, 145./255, 210./255)),
                                    ("b2" ,  (154./255, 171./255, 221./255)),
                                    ("b3" ,  (67./255, 115./255, 255./255)),
                                    ("b4" ,  (0./255, 0./255, 255./255)),
                                    ("b5" ,  (0./255, 0./255, 170./255)),
                                    ("b6" ,  (0./255, 0./255, 100./255))
                                    ])),
                       ("KITpurple" , OrderedDict([
                                    ("p0" ,  (188./255, 12./255, 141./255)),
                                    ("p1" ,  (205./255, 78./255, 174./255)),
                                    ("p2" ,  (218./255, 125./255, 197./255)),
                                    ("p3" ,  (232./255, 78./255, 174./255)),
                                    ("p4" ,  (120./255, 12./255, 100./255))
                                    ])),
                       ("KITbrown" , OrderedDict([
                                    ("br0" ,  (170./255, 127./255, 36./255)),
                                    ("br1" ,  (193./255, 157./255, 82./255)),
                                    ("br2" ,  (208./255, 181./255, 122./255)),
                                    ("br3" ,  (226./255, 208./255, 169./255)),
                                    ("br4" ,  (241./255, 231./255, 210./255))
                                    ])),
                       ("KITmay"    , OrderedDict([
                                    ("m0" ,  (102./255, 196./255, 48./255)),
                                    ("m1" ,  (148./255, 213./255, 98./255)),
                                    ("m2" ,  (178./255, 225./255, 137./255)),
                                    ("m3" ,  (209./255, 237./255, 180./255)),
                                    ("m4" ,  (232./255, 246./255, 217./255))
                                    ])),
                       ("KITcyan"   , OrderedDict([
                                    ("c0" , (28./255, 174./255, 236./255)),
                                    ("c1" , (95./255, 197./255, 241./255)),
                                    ("c2" , (140./255, 213./255, 245./255)),
                                    ("c3" , (186./255, 229./255, 249./255)),
                                    ("c4" , (221./255, 242./255, 252./255))
                                    ])),
                       ("KITblack"  , OrderedDict([
                                    ("bl0", (0./255, 0./255, 0./255)),
                                    ("bl1", (50./255, 50./255, 50./255)),
                                    ("bl2", (100./255, 100./255, 100./255)),
                                    ("bl3", (150./255, 150./255, 150./255)),
                                    ("bl4", (200./255, 200./255, 200./255))
                                    ])),
                       ("KITrainbow", OrderedDict([
                                    ("rb0", (80./255, 0./255, 0./255)),
                                    ("rb1", (170./255, 0./255, 0./255)),
                                    ("rb2", (255./255, 0./255, 0./255)),
                                    ("rb3", (255./255, 100./255, 0./255)),
                                    ("rb4", (255./255, 150./255, 0./255)),
                                    ("rb5", (255./255, 200./255, 0./255)),
                                    ("rb6", (255./255, 255./255, 0./255)),
                                    ("rb7", (255./255, 255./255, 100./255)),
                                    ("rb8", (255./255, 255./255, 150./255))
                                    ]))
                        ])
    return KITcolor

def adjustOrder(List, entryDict, len_total):
    """ Adjusts order of list according to the changes made in 'EntryList'.
        This will order the legend entrys.

        Args:
            List (list): list that you want to reorder (original list of
                         graph names)
    """

    # extract desired order from 'EntryList'
    userOrder = []
    userOrder = [int(item[0]) for item in list(entryDict.items())]

    # reorder the list
    List = [y for (x,y) in sorted(zip(userOrder, List))]

    return List


def manipulate(graphList, arg, cv_norm):
    msg = ""
    if cv_norm is True:
        graphList, msg = normalize(graphList, "CV")

    if arg == 'off':
        pass
    elif isinstance(arg, OrderedDict):
        for val in arg.values():
            val = extractList(val)
            graphList, text = normalize(graphList, val)
            if msg == "":
                msg = text
            else:
                msg = msg + ", " + text
    else:
        graphList, msg = normalize(graphList, arg)
    return graphList, msg


def normalize(graphList, arg):
    facList = []
    # normalization for CV plots
    if arg in ["1/C^{2}", "CV"]:
        for i, graph in enumerate(graphList):
            try:
                tempList = []
                for val in graph[1]:
                    if val == 0:
                        tempList.append(0)
                    else:
                        tempList.append(1/(val*val))
                graph[1] = tempList
            except:
                if graph[1] == 0:
                    pass
                else:
                    graph[1] = 1/(graph[1]*graph[1])
        msg = "Manipulated y-values by inverting their square"

    # normalization via list of factors
    elif isinstance(arg, list):
        for fac in arg:
            facList.append(fac)
        if len(graphList) != len(facList):
            raise ValueError("Invalid normalization input! Number of "
                             "factors differs from the number of graphs.")
        for i, graph in enumerate(graphList):
            tempList = []
            try:
                for val in graph[1]:
                    tempList.append(val/float(facList[i]))
                graph[1] = tempList
            except:
                graph[1] = graph[1]/float(facList[i])
        msg = "Normalized y-values by given denominators"

    # normalization via single factor
    elif isinstance(arg, (float, int)):
        for i, graph in enumerate(graphList):
            tempList = []
            try:
                for val in graph[1]:
                    tempList.append(val/arg)
                graph[1] = tempList
            except:
                graph[1] = graph[1]/arg
        msg = "Normalized y-values by given denominator {}".format(arg)

    elif "--x" in arg:
        fac = float(arg.split(" ")[1])
        for graph in graphList:
            temp_lst = []
            for val in graph[0]:
                temp_lst.append(val/fac)
            graph[0] = temp_lst
        msg = "Normalized x-values by given denominator {}".format(arg)

    else:
        print("Warning::Unknown normalization Input. Request rejected.")

    return graphList, msg

def extractList(arg, output="int"):
    """ Turns a 'str(list)' into a list. Converts its elements into
        floats if possible. Real strings as well as other types are just
        returned as they are.

        Args:
            arg: original value of respective key in cfg dict
            output (str): determines the output type of the list elements
    """

    if output not in ["int", "float"]:
        raise ValueError("Unexpected argument.")

    # for ints/floats disguised as str
    try:
        if isinstance(arg, str):
            return float(arg)
    except:
        pass

    if isinstance(arg, str) and arg[0] == '[' and arg[-1] == ']':
        if ':' in arg:
            str_list = arg.replace("[","").replace("]","").split(":")
        elif ',' in arg:
            str_list = arg.replace("[","").replace("]","").split(",")
        elif arg[1:-1].isdigit():
            return [int(arg[1:-1])]
        else:
            raise ValueError("Unkown input. ")

        try:
            if output == "int":
                new_list = [int(string) for string in str_list]
            elif output == "float":
                new_list = [float(string) for string in str_list]
            return new_list
        except:
            return str_list
    else:
        return arg


def arrangeFileList(List):
    """ The KITData files in .__files are somewhat arbitrarily
    ordered at first. This method pre-orders them in respect of their names.

    """
    TempList1 = []
    TempList2 = []
    IDList = []
    IndexList = []

    for temp in List:
        TempList1.append(temp.getName())
        TempList2.append(temp.getName())

    # if same name appears more than once...
    for i, Name1 in enumerate(TempList1):
        if TempList1.count(Name1) > 1:
            Test = Name1 + "_" + "(" + str(i) + ")"
            TempList2[i] = Test
            TempList1[i] = Test
        else:
            pass

    TempList2.sort()

    for i,Name2 in enumerate(TempList2):
        if Name2 == TempList1[i]:
            IndexList.append(i)
        else:
            for j, Name in enumerate(TempList1):
                if Name == Name2:
                    IndexList.append(j)

    TempList1[:] = []

    for index in IndexList:
        TempList1.append(List[index])
    List = TempList1

def interpolate(List, x=None, y=None):

    v = []

    if x is not None and y is not None:
        for File in List:
            m, b = np.polyfit(x, y, 1)
            v.append((m, b))

    else:
        x = []
        y = []

        for File in List:
            x = File.getX()
            y = File.getY()
            name = File.getName()
            m, b = np.polyfit(x, y, 1)
            v.append((name, abs(m)))

    return v
