from collections import OrderedDict
import matplotlib as plt
from .KITConfig import KITConfig

class KITLodger(object):

    def __init__(self, figure, **kwargs):
        self.iter = iter(["lodger1","lodger2","lodger3"])
        self.fig = figure
        self.lodger_type = None
        self.__x = kwargs.get('x', None)
        self.__y = kwargs.get('y', None)
        self.__name = kwargs.get('name', None)
        self.__color = kwargs.get('color', 0)
        self.__width = kwargs.get('width', 2)
        self.__style = kwargs.get('style', 1)
        self.__text = kwargs.get('text', None)
        self.__fontsize = kwargs.get('fontsize', 14)

        self.__paraDict =  {    "x"         : self.__x,
                                "y"         : self.__y,
                                "name"      : self.__name,
                                "color"     : self.__color,
                                "width"     : self.__width,
                                "style"     : self.__style,
                                "text"      : self.__text,
                                "fontsize"  : self.__fontsize
                            }

        self.__paraDict = self.stripDict()

    def add_to_plot(self):

        ax = self.fig.add_subplot(1,1,1)

        if self.__x == None and self.__y == None and self.__text == None:
            print("Lodger:::Lodger arrived with an empty suitcase. Goodbye.")
        elif self.__y == None and isinstance(self.__x, (int, float)):
            print("Lodger:::Draw vertical line at x = " + str(self.__x))
            self.lodger_type = "verticle line"
            ax.axvline(x=self.__x,color=self.__color,
                       linewidth=self.__width,linestyle=self.__style)
        elif self.__x == None and isinstance(self.__y, (int, float)):
            print("Lodger:::Draw horizontal line at y = " + str(self.__y))
            self.lodger_type = "horizontal line"
            ax.axhline(y=self.__y,color=self.__color,
                       linewidth=self.__width,linestyle=self.__style)
        elif isinstance(self.__y, list) and isinstance(self.__x, list):
            print("Lodger:::Draw graph according to [x],[y]")
            self.lodger_type = "graph"
            ax.plot(self.__x, self.__y, color=self.__color)
        elif self.__text != None:
            print("Lodger:::Draw text at (x,y)")
            self.lodger_type = "text"
            ax.text(self.__x,self.__y,self.__text,fontsize=self.__fontsize)
        # elif isinstance(self.__y, str) and isinstance(self.__x, list):
        #     print("Lodger:::Draw graph according to x->list and y->function.")
        #     if self.__y = "m*x+b"

        return self.fig

    def add_to_cfg(self, cfg):

        # add new lodger to lodger section in cfg
        try:
            # check if lodger is already in section
            if self.check_for_lodger_in_section(cfg) == True:
                pass
            # lodger is not yet in section
            else:
                lodger_count = len(list(cfg["Lodgers"].keys()))
                lodger_name = self.lodger_type + str(lodger_count+1)
                print("addLodgerEntry - update")
                new = cfg["Lodgers"]
                new.update({lodger_name : self.__paraDict})
                cfg["Lodgers"] = new

        # create lodgers section in cfg
        except:
            print("addLodgerEntry - add_new")
            lodger_name = self.lodger_type
            cfg["Lodgers"] = {lodger_name : self.__paraDict}

        # testDict = OrderedDict([("xxx", "111")])
        # print(testDict)
        # testDict.update({"yyy" : "222"})
        # print(testDict)

        return True

    def check_for_lodger_in_section(self,cfg):
        for lodger in cfg["Lodgers"]:
            if self.__paraDict == dict(cfg["Lodgers"][lodger]):
                return True
        return False

    def stripDict(self):
        """ Strip dict from all values that are None"""

        for key in list(self.__paraDict.keys()):
            if self.__paraDict[key] == None:
                del self.__paraDict[key]
        return self.__paraDict

    def getDict(self):
        """ Returns dictionary with lodger parameters"""

        return self.__paraDict

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def name(self):
        return self.__name

    def hline(self):
        return self.__hline

    def vline(self):
        return self.__vline

    def func(self):
        return self.__func

    def style(self):
        return self.__style

    def width(self):
        return self.__width

    def color(self):
        return self.__color

    def vgraph(self):
        return self.__vgraph

    def hgraph(self):
        return self.__hgraph
