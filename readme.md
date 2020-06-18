# KITPlot Readme

## 1. Synopsis

Hello World! Welcome to the KITPlot script. This script was created by
Daniel Schell (daniel.schell@kit.edu) and Marius Metzler
(marius.metzler@kit.edu). This script is about creating distinctive,
well-arranged plots especially for bachelor/master students at ETP, who find common, commercially available plotting software as lame and inconvenient as we do. The greatest benefit of KITPlot is that it is able to directly communicate with the ETP database. It also automatizes standard operations and procedures as well as making plots easily editable and reproducible via distinctive config files.

## 2. Structure

The script consists of 4 modules:

* The **KITPlot** module handles the conversion of a given input type into KITData objects. It then calls a drawing method while using parameters from a .cfg file. Eventually, the output contains:
   * 2 plot graphics (.png and .pdf file) that will be automatically
   stored in your output folder (will be created in your main
   folder if necessary)
   * a .cfg file that will be automatically stored in your cfg folder (will be created in your main folder if necessary)

* The **KITData** module can handle a number of different inputs (database IDs in string or integer type as well as file or folder paths). It then fetches the necessary data from the source, thereby creating a KITData instance in which all the data is stored.

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

## 4. Valid Inputs

### Single file
There are many valid input types which can be digested by KITPlot. The most basic one is plotting a file, which contains columns of data seperated by commas, tabs or spaces.
* 2 columns -> x, y values
* 3 columns -> x, y, z values
* 4 columns -> x, y, ex, ey
* 6 columns -> x, y, z, ex, ey, ez

You would invoke the plotting procedure of the data stored in *.\data\file.txt* by executing the following command in your main directory:
* *python .\main.py .\data\file.txt*

### Multiple files
If you have multiple files with data that you want to plot at once (each representing a single graph in your plot), then you want to put those files in a folder. Use the folder path as argument:
* *python .\main.py .\data\folder\\*

### JSON files
You can also plot JSON files if you comply with the following structure. The JSON file should contain a list (indicated by the square brackets) containing dicts (indicated by curly brackets). Use one dict for each graph. The KITPlot will try to lookup the keys "x" and "y" ("z", "ex", ...). The corresponding values must be lists with your data points (ususally float type).

* [{"x": [1, 2], "y": [0.123, 0.345]}, {...}]

### Database IDs
You can plot measurements by fetching the data from ETP database directly. Just pass the ID as an argument in the command line:
* *python .\main.py 15001*

You can also plot multiple IDs like that in one go by putting several IDs in squared brackets and seperating them by commas (e.g. *[15001,15002]*). Don't use spaces or else the argparse module will raise an error.

### ID files
If you have a plot with multiple graphs whose data you fetched from the database via IDs, it is good practice to create a file and write those IDs in there (one per line). This way, you can always replot it and change some stuff without looking up the IDs again.

### Raw data
So far we only talked about data that you identified by a command line string. But you can also pass raw data (python type data like lists and tuples). Besides, you can also pass an database ID as an integer. This can be done in the *main.py*. If you look in your *main.py* file you can see how the command line argument is passed to the KITPlot instance by calling the *addFiles()* method. By the way, you can call *addFiles()* method multiple times in order to add more and more graphs to your canvas. They can also be of different types, e.g. a database ID together with a file path. Here is an example:

* *KPLOT1.addFiles(15001)* -> plot measurement with database ID 15001
* *KPLOT1.addFiles([15001, 15002])* -> plot measurement with ID 15001 and 15002
* KPLOT1.addFiles([[1,2,3], [0.123, 0.345, 0.567]])* -> plot a graph where the list with index 0 contains the x values and the list with index 1 contains the y values




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
Examples of how to use them are given in the *default_main.py*. Additional matplotlib parameters can be passed with the *opt_dict* keyword. E.g.

* *KPLOT1.addLodger(fig, x=46.48e-12, y=60, text="test", fontsize=12, opt_dict={"bbox" : dict(facecolor='gray', alpha=0.5)})

If you add the line on the bottom of your *main.py* file, then the *addLodger()* method will create a gray textbox at the specified point (x,y) in your coordinate system with an opacity of 50%. The box contains the word "text" printed in size 12.