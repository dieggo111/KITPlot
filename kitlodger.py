from collections import OrderedDict
import matplotlib as plt

class KITLodger(object):

    def __init__(self, figure, **kwargs):

        self.fig = figure
        self.__x = kwargs.get('x', None)
        self.__y = kwargs.get('y', None)
        self.__name = kwargs.get('name', None)
        self.__color = kwargs.get('color', 0)
        self.__width = kwargs.get('width', 2)
        self.__style = kwargs.get('style', 1)
        self.__text = kwargs.get('text', None)
        self.__fontsize = kwargs.get('fontsize', 14)

        # self.__paraDict = OrderedDict()
        self.__paraDict =  {    "x"     : self.__x,
                                "y"     : self.__y,
                                "name"  : self.__name,
                                "color" : self.__color,
                                "width" : self.__width,
                                "style" : self.__style,
                                "text"   : self.__text
                            }


    def add(self):

        ax = self.fig.add_subplot(1,1,1)

        if self.__x == None and self.__y == None and self.__text == None:
            print("Lodger:::Lodger arrived with an empty suitcase. Goodbye.")
            # pass
        elif self.__y == None and isinstance(self.__x, (int, float)):
            print("Lodger:::Draw vertical line at x = " + str(self.__x))
            ax.axvline(x=self.__x,color=self.__color,
                       linewidth=self.__width,linestyle=self.__style)
        elif self.__x == None and isinstance(self.__y, (int, float)):
            print("Lodger:::Draw horizontal line at y = " + str(self.__y))
            ax.axhline(y=self.__y,color=self.__color,
                       linewidth=self.__width,linestyle=self.__style)
        elif isinstance(self.__y, list) and isinstance(self.__x, list):
            print("Lodger:::Draw graph according to [x],[y]")
            ax.plot(self.__x, self.__y, color=self.__color)
        # elif isinstance(self.__y, str) and isinstance(self.__x, list):
        #     print("Lodger:::Draw graph according to x->list and y->function.")
        #     if self.__y = "m*x+b"
        elif self.__text != None:
            print("Lodger:::Draw text at (x,y)")
            ax.text(self.__x,self.__y,self.__text,fontsize=self.__fontsize)

        return self.fig


    def getDict(self):
        """ Returns dictionary with lodger parameters, but removes all items
            without value in advance.
        """
        for key in list(self.__paraDict.keys()):
            if self.__paraDict[key] == None:
                del self.__paraDict[key]
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
