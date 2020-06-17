# KITPlot Readme

## 1. Synopsis

Hello World! Welcome to the KITPlot script. This script was created by
Daniel Schell (daniel.schell@kit.edu) and Marius Metzler
(marius.metzler@kit.edu). This script is about creating distinctive,
well-arranged plots especially for bachelor/master students at ETP, who find common, commercially available plotting software as lame and inconvenient as we do. The greatest benefit of KITPlot is that it is able to directly communicate with the ETP database. It also automatizes standard operations and procedures as well as making plots easily editable and reproducible via distinctive config files.

## 2. Structure

The script consists of 4 modules:
* The **KITData** module determines the input type of the data you want to plot. It accepts:
   * single .txt file that contains a data table (x-value, y-value,
          x-error, y-error separated by tabs or spaces)
   * folder that contains several .txt files
   * single ID
   * single .txt file that contains a list of IDs
   * raw data objects (lists)

   KITData then creates a KITData object for every graph, which contains the data table and provides convenient methods for handling all sensor parameters.

* The **KITPlot** module handles the conversion of a given input type into KITData objects. It then calls a drawing function while using parameters from a .cfg file. Eventually, the output contains:
   * 2 plot graphics (.png and .pdf file) that will be automatically
   stored in your output folder (will be created in your main
   folder if necessary)
   * and a .cfg file that will be automatically stored in your cfg folder (will be created in your main folder if necessary)

* The **KITConfig** module writes/reads/edits a plot-specific .cfg file.

* **KITMatplotlib** handles all the drawing.

## 2. Installation

* Create a main folder and give it a nice name (e.g. *KITScripts*)

* Inside this folder you ought to create a folder for cfg files named "cfg" and for output files named "output". Clone the KITPlot repository from https://gitlab.cern.ch/kit-cms/KITPlot/kitplot.git or visit https://gitlab.cern.ch/kit-cms/KITPlot/kitplot in order to download it manually. The *KITPlot* repo should be placed inside your main folder.

* You need authentication credentials in order to access the ETP database, which must be stored in a file called *db.cfg*. Create this file in your main folder. For security reasons, the login file can not be downloaded, but must be requested from an admin. A boilerplate file can be found in the *Utils* folder (KITPlot/Utils/default_db.cfg).

* While you're at it, you can also create a file called *main.py* in your main folder. This is the file that you will eventually execute in order to plot data with the KITPlot framework. Copy the example code from (KITPlot/Utils/default_main.py) and paste it into your main.py file. In the next chapter we gonna explain how to execute the plotting procedure.

* In the end, your folder should be structured as follows:

   * KITScripts/
      * cfg/
      * KITPlot/
      * output/
      * db.cfg
      * main.py

* You need python3 the run the framework on your OS. As for now, KITPlot is tested with python version 3.0.8. Download and install it on your system (https://www.python.org/downloads/).

* Finally, you can use the python package manager *pip* in order to install all the packages that you need for running KITPlot. The requirements are listed in *requirements.txt*. Open a terminal/shell and execute:
   * *pip install requirements.txt*


## 3. Let's get started

As already mentioned, you need to generate a *main.py* file in your main folder just outside your KITPlot repository. Just copy the code from the boilerplate file in KITPlot/Utils/default_main.py.

KITPlot needs at least 1 argument to do its magic. A second argument is optional as well as several option tags.

* First argument: data input. As described earlier, this can be e.g. the path of a file, which contains data or an ID which identifies a measurement in the ETP database.

* Optional arguments: could be the path to a specific cfg file. If none given, then the framework will search the cfg folder for a cfg file with the same name as the input. If you want to use a cfg file from another plot then this argument should be the path of this cfg file. Bottom line: names are important! Do not try to plot two folders that happen to have the same name. The former output will be overwritten with the new plot.

If no errors are being raised, the plot will show up on your screen.
You can now start to edit plot with the related cfg file in your cfg folder.

## 5. cfg file

Most parameters in our cfg file are self-explanatory. Some have a special syntax that needs be considered or need some explanation. Most important thing to remember is, that lists need to be stringified ([1,2,3] -> "[1,2,3]").

* **Axis and Titles**
   * **"Range": [200:1000]**: sets axis range from 200 to 1000 units. Mind the brackets!
   * **"Log": false**: Enables/disables log scale. Remember that having a 0 in your data table may raise errors.
   * **"Abs": true**: Enables/disables absolute values.
   * **"Title": ""**: Set axis and plot titles. You can announce special characters here in latex style like *$\\circ$*, *$\\sigma$* or super/subscript by *$_{i}$* and *$^{2}$*.

* **Misc**
   * **"Normalization": "off"**: When plotting quantities like currents or resistances you might want to normalize them. This can be done by inserting a normalization factor (denominators). This can be a single integer (which would be used to divide every y-value) or a stringified list like *"[.590296,7.590296,1.277161,1.277161]"* in respect of the original sensor order. If you want to normalize x-values end the string with *--x*. You can also apply multiple options by inserting a dict with random keys and options as values.
   * **"CVMeasurement": false**: Enables/disables the 1/C^2 normalization which is commonly used for CV plots.
   * **"ShowStats": true"**: If true, the framework will output mean values and standard deviations of the plotted graphs. If it's CV data then the framework will also try to calculate the full depletion voltage.

* **Legend**
   * *"Position": "auto"*: If this is set to auto then the scripts will search all 4 corners for the best spot to place the legend. You might wanna adjust this by using
      * *TR* (top right corner)
      * *TL* (top left corner)
      * *BR* (bottom right corner)
      * *BL* (bottom left corner)
      * *outside* (next to the pad)
      * *below* (below the pad)
   * *"EntryList": {
      "0": "sensor1",
      "1": "sensor2",
      "2": "sensor3"}: The legend elements are naturally ordered according to the data input. This original order (0, 1, 2) can be edited by changing the number in the brackets. However, other options will always refer to the original order.

* **Line**
   * **"Style": 1**: Change the line style of your graphs by altering the integer value where *1* corresponds to a solid line style. If you want to see different line styles for different graphs, then use a stringified list with integers like *"[1, 1, 2]"*. If you want no lines at all then insert a *"None"*.


## 6. Lodgers:

You can add graphs, lines and texts to your canvas by using lodgers.
Examples of how to use them are given in the *default_main.py* Additional matplotlib parameters can be passed with the *opt_dict* keyword.

