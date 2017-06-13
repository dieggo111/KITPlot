import numpy as np
# try to load plot engines
try:
    import ROOT
except:
    pass
try:
    import matplotlib.pyplot as plt
except:
    pass

class KITDraw(object):

    def __init__(self, engine):

        if engine == "ROOT":
            self.engine = 'ROOT'
        elif engine == 'matplotlib':
            self.engine = 'matplotlib'
        else:
            raise ValueError("KITDraw needs argument for setting up the "
                             " plot engine.")


    def test(self, x, y):

        plot = plt.plot(x, y)
        plt.setp(plot, color='r', linewidth='2.')
        plt.show()
        return True


if __name__ == '__main__':

    KITDraw('matplotlib').test([0,2,5,8],[1,3,4,5])


    input()
