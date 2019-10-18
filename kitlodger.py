import numpy as np
import logging
from .Utils import kitutils
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

class KITLodger(object):

    def __init__(self, figure, **kwargs):

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        if self.log.hasHandlers is False:
            format_string = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            formatter = logging.Formatter(format_string)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.log.addHandler(console_handler)

        self.fig = figure
        self.lodger_type = None
        self.__x = kwargs.get('x', None)
        self.__y = kwargs.get('y', None)
        self.__name = kwargs.get('name', None)
        self.__color = kwargs.get('color', "bl0")
        self.__width = kwargs.get('width', 2)
        self.__style = kwargs.get('style', "-")
        self.__text = kwargs.get('text', None)
        self.__fontsize = kwargs.get('fontsize', 14)
        self.__alpha = kwargs.get('alpha', 1)
        self.__opt_dict = kwargs.get('opt_dict', dict())

        self.__paraDict =  {    "x"         : self.__x,
                                "y"         : self.__y,
                                "name"      : self.__name,
                                "color"     : self.__color,
                                "width"     : self.__width,
                                "style"     : self.__style,
                                "text"      : self.__text,
                                "fontsize"  : self.__fontsize,
                                "alpha"     : self.__alpha,
                                "opt_dict"  : self.__opt_dict
                            }

        self.__paraDict = self.stripDict()

    def add_to_plot(self):

        ax = self.fig.add_subplot(1, 1, 1)

        if self.__x is None and self.__y is None and self.__text is None:
            self.log.info("Lodger:::Lodger arrived with an empty suitcase. Goodbye.")
        elif isinstance(self.__y, list) and isinstance(self.__x, list):
            self.log.info("Lodger:::Draw graph according to [x],[y]")
            self.lodger_type = "graph"
            ax.plot(self.__x, self.__y, 
                    color=self.get_lodger_color(self.__color),
                    linewidth=self.__width, linestyle=self.__style,
                    alpha=self.__alpha)
        elif isinstance(self.__x, np.ndarray) and isinstance(self.__y, np.ndarray):
            self.log.info("Lodger:::Draw function.")
            self.lodger_type = "function"
            ax.plot(self.__x, self.__y, 
                    color=self.get_lodger_color(self.__color), 
                    linewidth=self.__width, linestyle=self.__style, 
                    alpha=self.__alpha)
        elif self.__y is None or self.__x is None:
            if isinstance(self.__x, (int, float)):
                self.log.info("Lodger:::Draw vertical line at x = " + str(self.__x))
                self.lodger_type = "verticle line"
                ax.axvline(x=self.__x, 
                           color=self.get_lodger_color(self.__color),
                           linewidth=self.__width, linestyle=self.__style,
                           alpha=self.__alpha)
            if isinstance(self.__y, (int, float)):
                self.log.info("Lodger:::Draw horizontal line at y = " + str(self.__y))
                self.lodger_type = "horizontal line"
                ax.axhline(y=self.__y, 
                           color=self.get_lodger_color(self.__color),
                           linewidth=self.__width, linestyle=self.__style,
                           alpha=self.__alpha)
        elif self.__text is not None:
            self.log.info("Lodger:::Draw text at (x,y)")
            self.lodger_type = "text"
            ax.text(self.__x, self.__y, 
                    self.__text, fontsize=self.__fontsize, 
                    color=self.get_lodger_color(self.__color), 
                    **self.__opt_dict)
            try:
                self.__paraDict.pop("width")
                self.__paraDict.pop("style")
            except:
                pass

        elif "width" in self.__opt_dict.keys() and "height" in self.__opt_dict.keys():
            self.log.info("Lodger::Draw rectangle at (x,y)")
            self.lodger_type = "rectangle"
            rec = Rectangle((self.__x, self.__y), **self.__opt_dict)
            color = self.get_lodger_color(self.__color)
            patch = PatchCollection([rec], facecolor=color, 
                                    edgecolor=color, alpha=self.__alpha)
            ax.add_collection(patch)
            try:
                self.__paraDict.pop("fontsize")
                self.__paraDict.pop("width")
                self.__paraDict.pop("style")
            except:
                pass
        return self.fig

    def add_to_cfg(self, cfg):
        """Add new lodger to lodger section in cfg"""
        try:
            # check if lodger is already in section
            if self.check_for_lodger_in_section(cfg) == True:
                pass
            # lodger is not yet in section
            else:
                lodger_name = self.assign_lodger_name(cfg["Lodgers"])
                self.log.info("addLodgerEntry - update")
                new = cfg["Lodgers"]
                new.update({lodger_name : self.__paraDict})
                cfg["Lodgers"] = new
        # create lodgers section in cfg
        except:
            self.log.info("addLodgerEntry - add_new")
            lodger_name = self.lodger_type
            cfg["Lodgers"] = {lodger_name : self.__paraDict}

        return True

    def assign_lodger_name(self, lodger_dict):
        """Assign lodger name. Add multiplicity index if a lodger of
        same type already exists"""
        lodger_count = len(lodger_dict)-1
        lodger_name = self.lodger_type
        if self.lodger_type in lodger_dict.keys():
            lodger_name += str(lodger_count+1)
        return lodger_name


    def get_lodger_color(self, color):
        """Assign color"""
        KITcolor = kitutils.get_KITcolor()
        try:
            # if color is string and corresponds with KITcolor dict
            for colorDict in KITcolor.values():
                if color in colorDict.keys():
                    return colorDict[color]
            raise Exception
        except:
            # go with default color
            self.log.warning("Warning:::%s is an invalid lodger color. "\
                             "Using default color 'r0' instead.", color)
            return KITcolor["KITred"]["r0"]

    def check_for_lodger_in_section(self, cfg):
        """Checks if specific lodger is already in cfg file"""
        for lodger in cfg["Lodgers"]:
            if self.__paraDict == dict(cfg["Lodgers"][lodger]):
                return True
        return False

    def stripDict(self):
        """ Strip dict from all values that are None or empty"""
        new = {}
        for key, val in self.__paraDict.items():
            if isinstance(val, np.ndarray):
                new[key] = [elem for elem in val]
            if isinstance(val, dict):
                if val != {}:
                    new[key] = val
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
