from collections import OrderedDict
import matplotlib as plt

class KITLodger(object):

    def __init__(self, fig):
        self.fig = fig
        print(type(self.fig))


    def add(self, **kwargs):

        self.__type = kwargs.get('type_','None')
        self.__x = kwargs.get('x', None)
        self.__y = kwargs.get('y', None)
        self.__name = kwargs.get('name', None)
        # self.__func = None
        # self.__vline = None
        # self.__hline = None
        # self.__vgraph = None
        # self.__hgraph = None
        self.__color = kwargs.get('color', 0)
        self.__width = kwargs.get('width', 2)
        self.__style = kwargs.get('style', 1)
        self.__box = kwargs.get('box', None)

        # self.__paraDict = OrderedDict()
        self.__paraDict =  {    "x"     : self.__x,
                                "y"     : self.__y,
                                "name"  : self.__name,
                                "color" : self.__color,
                                "width" : self.__width,
                                "style" : self.__style
                            }


        ax = self.fig.add_subplot(1,1,1)

        if self.__x == None and self.__y == None:
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

        # elif self.__y == None and isinstance(self.__x, list):
        #     print("Lodger:::Draw vertical graph at x = " + str(self.__x))
        #     self.__vgraph = self.__x
        #
        # elif self.__x == None and isinstance(self.__y, list):
        #     print("Lodger:::Draw horizontal graph at y = " + str(self.__y))
        #     self.__hgraph = self.__y

        elif isinstance(self.__y, list) and isinstance(self.__x, list):
            print("Lodger:::Draw graph according to [x],[y]")
            ax.plot(self.__x, self.__y, color=self.__color)


        # elif isinstance(self.__y, str) and isinstance(self.__x, list):
        #     print("Lodger:::Draw graph according to x->list and y->function.")
        #     if self.__y = "m*x+b"

        elif isinstance(self.__box, tuple) and len(self.__box) == 4:
                print("Lodger:::Draw box according to (xmin,xmax,ymin,ymax)")
                plt.rectangle

        return self.fig

    def getDict(self):
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
