""" Utility methods
"""

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

    # adjust length of userOrder to not loose lodgers while zipping
    userOrder = extendList(userOrder,len_total)
    # while len(userOrder)<len_total:
    #     # appended elements must be higher then the max value to avoide doublings
    #     if len(userOrder)<max(userOrder):
    #         userOrder.append(max(userOrder)+1)
    #     else:
    #         userOrder.append(len(userOrder))

    # reorder the list
    # print(userOrder, List)
    List = [y for (x,y) in sorted(zip(userOrder, List))]

    return List

def extendList(List,len_total):

    # adjust length of userOrder to not loose lodgers while zipping
    while len(List)<len_total:
        # appended elements must be higher then the max value to avoide doublings
        if len(List)<max(List):
            List.append(max(List)+1)
        else:
            List.append(len(List))

    return List

def manipulate(graphList, arg):

    facList = []
    tempGraphs = graphList

    # normalization for CV plots
    if arg in ["1/C^{2}", "CV"]:
        for i, graph in enumerate(graphList):
            for y in graph:
                tempList = []
                for val in y:
                    if val == 0:
                        tempList.append(0)
                    else:
                        tempList.append(1/(val*val))
            graph[1] = tempList

    # no normalization
    elif arg == 'off':
        pass

    # normalization via list of factors
    else:
        for fac in extractList(arg):
            facList.append(fac)
        if len(graphList) != len(facList):
            raise ValueError("Invalid normalization input! Number of "
                             "factors differs from the number of graphs.")
        for i, graph in enumerate(graphList):
            tempList = []
            for val in graph[1]:
                tempList.append(val/float(facList[i]))
            graph[1] = tempList

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

    if isinstance(arg, str) and arg[0] == '[' and arg[-1] == ']':
        if ':' in arg:
            str_list = arg.replace("[","").replace("]","").split(":")
        elif ',' in arg:
            str_list = arg.replace("[","").replace("]","").split(",")
        elif len(arg) == 3:
            str_list = list(arg.replace("[","").replace("]",""))
        else:
            raise ValueError("Unkown input. Cfg parameter needs to be a"
                             " string. Accepted seperations are ',' and "
                             "':'. ")
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
