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
                    tempList.append(1/(val*val))
            graph[1] = tempList

    # no normalization
    elif arg == 'off':
        pass

    # normalization via list of factors
    else:
        for fac in self.extractList(arg):
            facList.append(fac)
        if len(graphList) != len(facList):
            raise ValueError("Invalid normalization input! Number of "
                             "factors differs from the number of graphs.")
        for i, graph in enumerate(graphList):
            for y in graph:
                tempList = []
                for val in y:
                    tempList.append(val/facList[i])
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
