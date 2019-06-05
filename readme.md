################################################################################
KITPlot Readme
################################################################################
1) Synopsis:
################################################################################
Hello World! Welcome to the KITPlot script. This script was created by
Daniel Schell (daniel.schell@kit.edu) and Marius Metzler
(marius.metzler@kit.edu). This script is about creating distinctive,
well-arranged plots especially for bachelor/master students at ETP, who find
common, commercially available plotting software as lame and inconvenient
as we do. The greatest benefit of KITPlot is that it is able to directly
communicate with the ETP database. It also automatizes standard operations and
procedures as well as making plots easily editable and reproducible via
distinctive config files.

################################################################################
2) Structure:
################################################################################
The script consists of 4 modules:
    a) The KITData module determines the input type of the data you want to
       plot. It accepts:
        - single .txt file that contains a data table (x-value, y-value,
          x-error, y-error separated by tabs or spaces)
        - folder that houses several .txt files
        - single ID (*probe ID* for probe station measurements,
          *Run* for alibava measurements)
        - single .txt file that contains a list of IDs

        KITData then creates a KITData object for every graph, which contains
        the data table and provides convenient methods for handling all
        sensor parameters.

    b) The KITPlot module handles the conversion of a given input type into
       KITData objects. It then calls a drawing function while using parameters
       from a .cfg file. Eventually, the output contains:
        - 2 plot graphics (.png and .pdf file) that will be automatically
          stored in your output folder (will be created in your main
          folder if necessary)
        - and a .cfg file that will be automatically stored in your cfg folder
          (will be created in your main folder if necessary)

    c) The ConfigHandler module writes/reads/edits a plot-specific .cfg file.
       Since KITPlot is console-based and has no graphical interface, the
       config file solution makes up for it.

    e) kitmatpoltlib handles all the drawing.

################################################################################
3) Installation:
################################################################################
    a) Create a main folder and give it a nice name (f.e. *KITPlot*)
    b) Inside this folder you ought to create a folder for cfg files named
       "cfg" and for output files named "output". Clone the KITPlot
       repository from *https://github.com/dieggo111/KITPlot*,
       put its content inside an extra folder within your main folder and name
       it *KITPlot*.
    c) Download and install python 3 on your system
       (https://www.python.org/downloads/).
    d) The most recent version of python 3 contains *pip3*, a download
       manager/installer for python modules, which should be used to download
       the following modules:
       - numpy: *pip3 install numpy*
       - json: *pip3 install simplejson*
       - pymysql: Download download and unzip source file from
                  https://pypi.python.org/pypi/mysql-connector-python/2.0.4 or
                  use the one in the
                  repository. Open console/terminal and go to PyMySQL-0.7.11
                  folder. Type "python setup.py build" and then
                  "python setup.py install".
    e) Plotting is based on matplotlib.
       - matplotlib: *pip3 install matplotlib*

    f) Lastly, you need login information to access the database, which are
       stored in the *db.cfg*. For security reasons the login file can not be
       downloaded, but must be requested from Daniel or Marius.

################################################################################
4) Let's get started:
################################################################################
    Before creating your first plot you need to write a few lines of code for
    yourself. Create a *main.py* file import KITPlot and KITData as well as sys
    or other modules you need. KITPlot needs at least 1 argument to do its
    magic. A second argument is optional.
        - First argument: data input. As described earlier, this can be a path
          of a file, folder or a run number from the database. It is also
          possible to pass a list with PIDs or a single PID.

        - Second argument: cfg file. If this is not given (None), then the
          script will search the cfg folder for a cfg file with the same name
          as the input. If you want to use a cfg file from another plot then
          this argument should be the path of this cfg file. Bottom line: names
          are important! Do not try to plot two folders that happen to have the
          same name. The former output will be overwritten with the new plot.

    A basic example of a main file can be found in *KITPlot\Utils\default_main.py*

    If no errors are being raised, the plot will show up on your screen.
    You can now start to edit plot with the related cfg file in your cfg folder.

################################################################################
5) cfg file:
################################################################################
    Most parameters in our cfg file are self-explanatory. Some have a special
    syntax that needs be considered or need some explanation:

    - *Range = [200:1000]*: sets axis range from 200 to 1000 units.
                            Mind the brackets!
    - *Font = 62*: 62 is standard arial, bulky and ideal for presentations.
                   See ROOT documentation for other options.
    - *Log = false*: This needs to be a boolean value. Remember that having a 0
                     in your data table may raise errors.
    - *Abs = true*: This needs to be a boolean value.
    - *Title = ""*: You can announce special characters here in latex style
                    *$* like *$\\circ*, *$\\sigma* or super/subscript
                    by *$_{i}$* and *$^{2}$*.
    - *GraphGroup = off*: Default values are *off*, *name*, *fluence*.
                          Sometimes you might want to visualize that certain
                          graphs belong together by giving them a similar color.
                          *off* will just alter marker color and style for
                          every graph. By choosing *name*, all graphs that
                          share the first 5 letters of their name will be drawn
                          in the same color but with altering markers (f.e.
                          sensors of the same type but from different wafers).
                          If *fluence* is chosen then then sensors with equal
                          fluences will be drawn in the same color (the flunces
                          are retrieved from the database). Lastly, you can
                          make your own *GraphGroup* by using the original
                          sensor order and put them into brackets like
                          *[1,2][6][3,4,5]*.
    - *ColorShades = false*: This needs to be a boolean value. If you use
                             GraphGroups, you might as well want to use
                             ColorShades. Let*s say you have 3 red graphs and
                             set this to True, then you will get 3 different
                             kinds of red instead of one to make the graphs more
                             distinctive and recognizable.
    - *Normalization = off*: When plotting quantities like currents or
                             resistances you might want to normalize them.
                             This can be done by inserting the normalization
                             factors (denominators) like
                             *[7.590296,7.590296,1.277161,1.277161]* in respect
                             of the original sensor order. In this case, every
                             y-value of graph 1 and 2 (original sensor order)
                             would be divided (normalized) by 7.590296. Other
                             options are *CV* which plots the inverted squared
                             y-values. If you want to normalize x-values end
                             the string with *--x*. You can also apply multiple
                             options by inserting a dict with random keys and
                             options as values.
    - *Position = auto*: If this is set to auto then the scripts will search all
                         4 corners for the best spot to place the legend. You
                          might wanna adjust this by using
                         *TR* (top right corner),
                         *TL*,
                         *BR* (bottom right corner) or
                         *BL*.

    - *BoxPara = 1*: If you change the name of a legend element you might want
                     to adjust the legend box width by changing this factor in
                     between 0.5 and 1.5.

    - *EntryList = (0)a, (1)b, (3)c, (2)d*: The legend elements are naturally
                                            ordered by ROOT. This original order
                                            (here: a = 0, b = 1, c = 2, d = 3)
                                            can be edited by changing the number
                                            in the brackets. However, other
                                            options will always refer to the
                                            original order.

    - *Line* -> *Style* = *[1,7]*: This feature enables drawing different lines
                                   in different styles. In this example, the
                                   first line is continuous while the second
                                   line is dashed. You can also just write
                                   something like *Style* = 1 (integer) to draw
                                   all lines in the same style. If you want no
                                   lines at all then insert a *"None"*.

    - *Marker* -> *Set* = "[21,20,...]": KITPlot will iterate through this list
                                         when drawing graphs to determine
                                         the marker style. This list is just a
                                         suggestion. Feel free to edit the
                                         number of marker styles in this list.
                                         See ROOT documentation for the respective
                                         marker styles.

    - *Line* -> *Color* = "[1100,1200,...]": KITPlot will iterate through this
                                             list when drawing graphs to
                                             determine the line color. KITPlot
                                             uses its own color palette, but can
                                             also use the ROOT palette, although
                                             some options might not work then.
                                             The *self.__initColor* function
                                             incorporates our self-made color
                                             palette.

################################################################################
6) Lodgers:
################################################################################
    You can add graphs, lines and texts to your canvas by using lodgers.
    Examples of how to use them are given in the suggested main. Additional
    matplotlib parameters can be passed with the *opt_dict* keyword.

################################################################################
7) Fits:
################################################################################
    You can also use the fit function for analysis. The results can be added to
    your canvas via lodgers.
