import numpy as np
from .Utils import kitutils

class KITLodger(object):

    def __init__(self, figure, **kwargs):

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
        self.__alpha = kwargs.get('alpha', 1)

        self.__paraDict =  {    "x"         : self.__x,
                                "y"         : self.__y,
                                "name"      : self.__name,
                                "color"     : self.__color,
                                "width"     : self.__width,
                                "style"     : self.__style,
                                "text"      : self.__text,
                                "fontsize"  : self.__fontsize,
                                "alpha"     : self.__alpha
                            }

        self.__paraDict = self.stripDict()

    def add_to_plot(self):

        ax = self.fig.add_subplot(1, 1, 1)

        if self.__x is None and self.__y is None and self.__text is None:
            print("Lodger:::Lodger arrived with an empty suitcase. Goodbye.")
        elif isinstance(self.__y, list) and isinstance(self.__x, list):
            print("Lodger:::Draw graph according to [x],[y]")
            self.lodger_type = "graph"
            ax.plot(self.__x, self.__y, color=self.get_lodger_color(self.__color))
        elif isinstance(self.__x, np.ndarray) and isinstance(self.__y, np.ndarray):
            print("Lodger:::Draw function.")
            self.lodger_type = "function"
            ax.plot(self.__x, self.__y, color='black')
        elif self.__y is None or self.__x is None:
            if isinstance(self.__x, (int, float)):
                print("Lodger:::Draw vertical line at x = " + str(self.__x))
                self.lodger_type = "verticle line"
                ax.axvline(x=self.__x, color=self.get_lodger_color(self.__color),
                           linewidth=self.__width, linestyle=self.__style,
                           alpha=self.__alpha)
            if isinstance(self.__y, (int, float)):
                print("Lodger:::Draw horizontal line at y = " + str(self.__y))
                self.lodger_type = "horizontal line"
                ax.axhline(y=self.__y, color=self.get_lodger_color(self.__color),
                           linewidth=self.__width, linestyle=self.__style,
                           alpha=self.__alpha)
        elif self.__text is not None:
            print("Lodger:::Draw text at (x,y)")
            self.lodger_type = "text"
            ax.text(self.__x, self.__y, self.__text, fontsize=self.__fontsize)
        return self.fig

    def add_to_cfg(self, cfg):
        """Add new lodger to lodger section in cfg"""
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

        return True

    def get_lodger_color(self, color):

        KITcolor = kitutils.get_KITcolor()
        try:
            if color == "black":
                return color
            # if color is string and corresponds with KITcolor dict
            for colorDict in list(KITcolor.values()):
                return colorDict[color]
        except:
            # go with default color
            print("Warning:::%s is an invalid lodger color. Using default color 'r0' instead." %(color))
            return KITcolor["KITred"]["r0"]

    def check_for_lodger_in_section(self,cfg):
        for lodger in cfg["Lodgers"]:
            if self.__paraDict == dict(cfg["Lodgers"][lodger]):
                return True
        return False

    def stripDict(self):
        """ Strip dict from all values that are None"""
        new = {}
        for key, val in self.__paraDict.items():
            if isinstance(val, np.ndarray):
                print(val, [elem for elem in val])
                new[key] = [elem for elem in val]
            elif self.__paraDict[key] is not None:
                new[key] = val
        return new

    def getDict(self):
        """ Returns dictionary with lodger parameters"""
        return self.__paraDict

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def name(self):
        return self.__name

    def style(self):
        return self.__style

    def width(self):
        return self.__width

    def color(self):
        return self.__color
