
class KITUtils(object):

    def counter_loop(self, List, index):

        if index >= len(List):
            counter = List[index%len(List)]
        else:
            counter = List[index]

        return counter

    def manipulate(self, graphList, arg):

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


    def extractList(self, string, output="int"):
        """ Turns a 'string(list)' into a list. Converts its elements into
            floats if possible. Real input strings are just returned as they
            are.

            Args:
                string (str): original value of respective key in cfg dict
                output (str): determines the output type of the list elements
        """

        if output not in ["int", "float"]:
            raise ValueError("Unexpected argument.")

        if string[0] == '[' and string[-1] == ']':
            if ':' in string:
                string_list = string.replace("[","").replace("]","").split(":")
            elif ',' in string:
                string_list = string.replace("[","").replace("]","").split(",")
            else:
                raise ValueError("Unkown input. Cfg parameter needs to be a"
                                 " string. Accepted seperations are ',' and "
                                 "':'. ")
            try:
                if output == "int":
                    new_list = [int(string) for string in string_list]
                elif output == "float":
                    new_list = [float(string) for string in string_list]
                return new_list
            except:
                return string_list
        else:
            return string
