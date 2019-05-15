# DataAnalysis
Package containing scripts to analyze CSV files for Neware exports, Medusa2012 exports, Rietica exports, and phase diagrams. See "DataAnalysis Package Instructions" for a detailed list of all available methods and the steps required to change the file path used in each script. 
## plateReader
Processes CSV files produced by the Medusa2012 program for 64 pad combi plates. An example file called “plateFile.csv” can be found in the shared Code folder. 
1.  From the Anaconda3 folder, open the python.exe application.
2.	In the shell, enter the command “from DataAnalysis.plateReader import *”.
3.	Enter the CSV file name without the .csv extension.
    * e.g. For the file “plateFile.csv”, just enter “plateFile”. 
    * A CSV file in the “Data” folder on the desktop can be accessed through the file location: “C:\Users\McCalla Lab\Desktop\Data\plateFile”.
4.	Enter the name of the file containing the masses of each sample on each channel. An example file showing the format of the mass file can be found in the shared Code folder called “massFile.csv”. Note that any other text in the file will be ignored and that the masses for channels 1-64 should be in columns C-BM respectively of row 2. The masses are also located in the same location as the masses in the exported file so the same file can be used for masses as the exported data. 
    * The mass file needs to contain the masses in the same location as the masses in the exported data CSV file.
    * If no mass file is available, you can click “Enter” to pass the command without entering a file name. Masses will be requested as needed for each channel.
5.	To use one of the available methods, type the method name with the desired parameters in the brackets and press Enter.
    * e.g. The method “capacity(channel, cycle)” can be used for channel 1 during cycle 2 to calculate charge and discharge capacities by entering “capacity(1, 2)”.
## cellReader
Processes CSV files produced by Neware for Swagelok cells. An example cell file can be found in the shared Code folder called “cellFile.csv”.
1.	From the Anaconda3 folder, open the python.exe application.
2.	In the shell, enter the command “from DataAnalysis.cellReader import *”.
3.	Enter the CSV file name without the .csv extension.
    * e.g. For the file “cellFile.csv”, just enter “cellFile”.
    * A CSV file in the “Data” folder on the desktop can be accessed through the file location: “C:\Users\McCalla Lab\Desktop\Data\cellFile”.
4.	To use one of the available methods, type the method name with the desired parameters in the brackets and press Enter.
    * e.g. The method “plotVoltsVsCapacity(cycle, fileNum = 1)” can be used to plot Voltage vs Capacity for cycle 2 of file 1 by entering “plotVoltsVsCapacity(2)”.
    * File 1 is the default file number. To plot another file, enter the file number in the method call.
      * “plotVoltsVsCapacity(1, 2)” will plot the data for cycle 1 of file 2.
## phaseDiagram
Processes ternary phase data to generate a ternary phase diagram. An example of the phase diagram file format can be found in the shared Code folder called “phaseDiagramFile.csv”. Note the axis labels are read from the column labels of the input CSV file. 
To run this program, the python-ternary library must be installed in Anaconda3. If this has been installed, a folder called “ternary” can be found in “Ananconda3\Lib\site-packages”. 
To use the phaseDiagram program:
1.	From the Anaconda3 folder, open the python.exe application. 
2.	In the shell, enter the command “from DataAnalysis.phaseDiagram import *”.
3.	Enter the CSV file name without the .csv extension. 
    * e.g. For the file “csvexample.csv”, just enter “csvexample”.
    * A CSV file in the “Data” folder on the desktop can be accessed through the file location: “C:\Users\McCalla Lab\Desktop\Data\csvexample”.
4.	To use one of the available methods, type the method name and press Enter.
    * e.g. Type “plotDiagram()” to generate the ternary phase diagram.
## pxrd
pxrd plots the PXRD and refinement data exported from Rietica and converted into a CSV file or just the x ad y data contained in columns 1 and 2 of CSV file. An example of the CSV file format is in the shared Code folder, called “xrdFile.csv”. 
1.	From the Anaconda3 folder, open the python.exe application.
2.	In the shell, enter the command “from DataAnalysis.pxrd import *”
3.	Enter the CSV file name without the .csv extension. 
    * e.g. For the file “xrdFile.csv”, just enter “xrdFile”
    * A CSV file in the “Data” folder on the desktop can be accessed through the file location: “C:\Users\McCalla Lab\Desktop\Data\xrdFile”.
4.	To use one of the available methods, type the method name and press Enter.
    * e.g. Type “plotXRD()” to plot the input XRD data.
