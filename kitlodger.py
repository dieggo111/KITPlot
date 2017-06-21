class KITLodger(object):

    def __init__(self, **kwargs):

        self.__x = kwargs.get('x', None)
        self.__y = kwargs.get('y', None)
        self.__name = kwargs.get('name', None)
        self.__func = None
        self.__vline = None
        self.__hline = None
        self.__vgraph = None
        self.__hgraph = None
        self.__color = kwargs.get('color', 0)
        self.__width = kwargs.get('width', 2)
        self.__style = kwargs.get('style', 1)

        # interpret x,y arguments
        if self.__x == None and self.__y == None:
            # print("Lodger:::Lodger arrived with an empty suitcase. Goodbye.")
            pass
        elif self.__y == None and isinstance(self.__x, (int, float)):
            print("Lodger:::Draw vertical line at x = " + str(self.__x))
            self.__vline = self.__x
        elif self.__x == None and isinstance(self.__y, (int, float)):
            print("Lodger:::Draw horizontal line at y = " + str(self.__y))
            self.__hline = self.__y
        elif self.__y == None and isinstance(self.__x, list):
            print("Lodger:::Draw vertical graph at x = " + str(self.__x))
            self.__vgraph = self.__x
        elif self.__x == None and isinstance(self.__y, list):
            print("Lodger:::Draw horizontal graph at y = " + str(self.__y))
            self.__hgraph = self.__y
        elif isinstance(self.__y, list) and isinstance(self.__x, list):
            print("Lodger:::Draw graph according to (x,y)->list.")
        elif isinstance(y, str) and isinstance(x, list):
            print("Lodger:::Draw graph according to x->list and y->function.")
            self.__func = self.__y



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

    def readCfg(self, arg):
        return True
