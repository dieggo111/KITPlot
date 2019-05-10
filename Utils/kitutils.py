""" Utility methods
"""

from collections import OrderedDict

def get_KITcolor():

    KITcolor = OrderedDict([
                       ("KITred"    , OrderedDict([
                                    ("r0" , (191./255, 35./255, 41./255)),
                                    ("r1" , (205./255, 85./255, 75./255)),
                                    ("r2" , (220./255, 130./255, 110./255)),
                                    ("r3" , (230./255, 175./255, 160./255)),
                                    ("r4" , (245./255, 215./255, 200./255))
                                    ])),
                       ("KITgreen"  , OrderedDict([
                                    ("g0" ,  (0./255, 169./255, 144./255)),
                                    ("g1" ,  (75./255, 195./255, 165./255)),
                                    ("g2" ,  (125./255, 210./255, 185./255)),
                                    ("g3" ,  (180./255, 230./255, 210./255)),
                                    ("g4" ,  (215./255, 240./255, 230./255))
                                    ])),
                       ("KITorange" , OrderedDict([
                                    ("o0" ,  (247./255, 145./255, 16./255)),
                                    ("o1" ,  (249./255, 174./255, 73./255)),
                                    ("o2" ,  (251./255, 195./255, 118./255)),
                                    ("o3" ,  (252./255, 218./255, 168./255)),
                                    ("o4" ,  (254./255, 236./255, 211./255))
                                    ])),
                       ("KITblue"   , OrderedDict([
                                    ("b0" ,  (67./255, 115./255, 194./255)),
                                    ("b1" ,  (120./255, 145./255, 210./255)),
                                    ("b2" ,  (155./255, 170./255, 220./255)),
                                    ("b3" ,  (195./255, 200./255, 235./255)),
                                    ("b4" ,  (225./255, 225./255, 245./255))
                                    ])),
                       ("KITpurple" , OrderedDict([
                                    ("p0" ,  (188./255, 12./255, 141./255)),
                                    ("p1" ,  (205./255, 78./255, 174./255)),
                                    ("p2" ,  (218./255, 125./255, 197./255)),
                                    ("p3" ,  (232./255, 175./255, 220./255)),
                                    ("p4" ,  (243./255, 215./255, 237./255))
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


def manipulate(graphList, arg):

    facList = []
    newList = []
    # no normalization
    if arg == 'off':
        pass
    # normalization for CV plots
    elif arg in ["1/C^{2}", "CV"]:
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
    elif "--x" in arg:
        fac = float(arg.split(" ")[1])
        temp_lst = []
        for graph in graphList:
            for val in graph[0]:
                temp_lst.append(val/fac)
            graph[0] = temp_lst
    else:
        print("Warning::Unknown normalization Input. Request rejected.")

    return graphList

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
        elif len(arg[1:-1]) == 1:
            str_list = []
            str_list.append(arg[1:-1])
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

def makeFit(List, print_fit, draw_fit):

    x = []
    y = []

    print("Fit Results:")

    if isinstance(List, KITData):
        x = List.getX()
        y = List.getY()

        p0, p1 = abs(np.polyfit(x ,y, 1))


        print("{:>8} {:>8} {:>8}".format(List.getName(),
                                         " : m = " + str(round(p0,5)),
                                         " ; R = " + str(round(1./p0,5))))

    else:
        #TODO non-kitdata objects
        pass
