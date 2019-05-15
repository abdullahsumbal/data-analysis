import csv
import ternary
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

filepath = 'C:\\Users\\Matt\\OneDrive - McGill University\\Work\\Cells\\'

# Empty global lists to store the fractions of each of the three elements and their respective capacities.
# The element names are then stored in the global xName, yName, and zName strings
xVal = []
yVal = []
zVal = []
data = []
xName = ''
yName = ''
zName = ''
dataName = ''

# Clears data from a previous file if it is present then loads the new data
# Takes the column that will be used to generate the color bar as dataColumn, 
# either as upper- or lower-case letters or as in integer. Takes an alternate
# label for the color bar that will be used instead of the column header.
def newFile(dataColumn = 'A', dataLabel = ''):
    
    # Checks the value of dataColumn to convert the value to a useable integer
    if(type(dataColumn) == int):
        dataColumn -= 1
    elif(ord(dataColumn) > 96):
        dataColumn = ord(dataColumn) - ord('a')
    elif(ord(dataColumn) > 64):
        dataColumn = ord(dataColumn) - ord('A')
    elif(ord(dataColumn) > 47 and ord(dataColumn) < 58):
        dataColumn = ord(dataColumn) - ord('0') - 1
    else:
        raise ValueError('dataColumn must be a character or number')
           
    # Takes the file name and clears stored data
    filename = input('Enter the phase diagram file name: ') + '.csv'
    if (xVal != []):
        xVal.clear()
        yVal.clear()
        zVal.clear()
        data.clear()
        
    global xName
    global yName
    global zName
    global dataName
    
    # Reads the data from the input phase diagram file
    with open(filepath + filename, 'r') as inputData:
        reader = csv.reader(inputData, dialect = 'excel')
        header = True
        
        for row in reader:
            
            # Reads the column headers
            if (header == True):
                xName = row[0]
                yName = row[1]
                zName = row[2]
                dataName = row[dataColumn]
                header = False
                
            # Reads the phase data and color bar data if it is necessary
            # and will fill the data with 0 if not needed
            else:
                if (dataColumn < 3):
                    xVal.append(float(row[0]))
                    yVal.append(float(row[1]))
                    zVal.append(float(row[2]))
                    data.append(0)
                else:
                    xVal.append(float(row[0]))
                    yVal.append(float(row[1]))
                    zVal.append(float(row[2]))
                    data.append(float(row[dataColumn]))
                    
    # Changes the dataName to dataLabel if dataLabel is not empty              
    if(dataLabel != ''):
        dataName = dataLabel
    plotDiagram()            
    
# Plots the ternary data using python-ternary
def plotDiagram():
    points = []
    colors = []
    
    # Creates tuples that will be used as data points
    for i in range(len(xVal)):
        points.append((xVal[i], yVal[i], zVal[i]))
        
    # Assigns colors to each composition based on the capacity found. The highest capacity is
    # given the color red (1, 0, 0) then the color goes down to black (0, 0, 0) for the lowest
    # capacity. 
    for cap in data:
        if(min(data) != max(data)):
            colors.append((((cap-min(data))/(max(data)-min(data))), 0.0, 0.0))
        else:
            colors.append((1,0,0))

    # Creates a ternary set of axes to plot the diagram from python-ternary
    figure, tax = ternary.figure(scale = 1.0)
    tax.boundary()
    tax.gridlines(multiple = 0.1, color = 'blue')
    
    # Plots data with a color bar if the minimum and maximum values of data are not equal (ie. 0)
    if(min(data) != max(data)):
        figure.set_size_inches(6.5,7.06)
        cm = LinearSegmentedColormap.from_list('Capacities', ['black', 'red'], N = 1024)
        cb_args = {'shrink':0.5, 'aspect':20, 'pad':0.02, 'orientation':'horizontal'}
        tax.scatter(points, marker = 'o', c = colors, s = 20, colorbar = True, colormap = cm, vmin = min(data), vmax = max(data), cbarlabel = dataName, cb_kwargs = cb_args)
        tax.left_axis_label(zName, fontsize = 14, offset = 0.11)
        tax.right_axis_label(yName, fontsize = 14, offset = 0.105)
        tax.bottom_axis_label(xName, fontsize = 14, offset = 0.007)
        
    # Plots a phase diagram without a color bar and each point as red
    else:
        figure.set_size_inches(6.5,5.87)
        tax.left_axis_label(zName, fontsize = 14, offset = 0.11)
        tax.right_axis_label(yName, fontsize = 14, offset = 0.105)
        tax.bottom_axis_label(xName, fontsize = 14, offset = 0.005)
        tax.scatter(points, marker = 'o', c = colors, s = 20, label = '%.4f mAh/g' % max(data))
        if (max(data) != 0):
            tax.legend()
    tax.ticks(axis = 'blr', linewidth = 1.0, multiple = 0.1, tick_formats = '%.1f', offset = 0.02)
    plt.axis('off')
    print('Ternary plots generated using the python-ternary library\nMarc Harper et al. (2015). python-ternary: Ternary Plots in Python. Zenodo. 10.5281/zenodo.34938')
    tax.show()
        
print('\nAvailable Functions:')
print('newFile(dataColumn = \'A\', dataLabel = \'\')')
print('plotDiagram()\n')