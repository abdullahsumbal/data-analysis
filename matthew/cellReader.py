import csv
from itertools import islice
import matplotlib.pyplot as plt
import numpy as np

filepath = 'C:\\Users\\Matt\\OneDrive - McGill University\\Work\\Cells\\'

# Empty global lists to store the cycle numbers, voltages, currents, capacities,
# energies, specific capacities and energies, and charge and discharge capacities, 
# specific capacities, energies, specific energies, and capacitances for each cycles
# in chronological order
cycles = []
voltages = []
currents = []
capacities = []
energies = []
sCapacities = []
sChgCapacities = []
sDchgCapacities = []
sEnergies = []
cycleChgCap = []
cycleDchgCap = []
sCycleChgCap = []
sCycleDchgCap = []
cycleChgEng = []
cycleDchgEng = []
sCycleChgEng = []
sCycleDchgEng = []
times = []
mass = []
numFiles = 0

# Initializes a new file by appending a new list to each list then storing each piece of data in its respective
# list
def newFile():
    global mass
    global numFiles
    filename = input('Enter the cell file name: ') + '.csv' 
    
    cycles.append([])
    voltages.append([])
    currents.append([])
    capacities.append([])
    energies.append([])
    sCapacities.append([])
    sEnergies.append([])
    cycleChgCap.append([])
    cycleDchgCap.append([])
    sCycleChgCap.append([])
    sCycleDchgCap.append([])
    cycleChgEng.append([])
    cycleDchgEng.append([])
    sCycleChgEng.append([])
    sCycleDchgEng.append([])
    times.append([])
    
    with open(filepath + filename, 'r') as inputData:
        reader = csv.reader(inputData, dialect = 'excel')
        
        # Iterates through the rows of the CSV file starting at row 3
        currentCycle = 0
        restStep = False
        for row in islice(reader, 3, None):
            
            # Skips the rest step by changing restStep back to false once the charge cycle
            # is entered
            if('CC_Chg' in row[2] or 'CC_DChg' in row[2] or row[0] != ''):
                restStep = False
                
            if(restStep):
                continue
            
            # Sets currentCycle to the value of the first column if that column is not empty and
            # cycle charge and discharge capacities, energies, specific capacities and energies
            if(row[0] != ''):
                currentCycle += 1
                cycleChgCap[numFiles].append(1000*float(row[1]))
                sCycleChgCap[numFiles].append(float(row[3]))
                cycleChgEng[numFiles].append(float(row[6]))
                sCycleChgEng[numFiles].append(float(row[8])/1000)
                cycleDchgCap[numFiles].append(1000*float(row[2]))
                sCycleDchgCap[numFiles].append(float(row[4]))
                cycleDchgEng[numFiles].append(float(row[7]))
                sCycleDchgEng[numFiles].append(float(row[9])/1000)
            
            # Skips the row that is the rest step of Cycle 1 and sets restStep to True to indicate
            # the current step
            elif('Rest' in row[2]):
                restStep = True
                continue
            
            # Skips the rows that contain 'CC_Chg' or 'CC_DChg'
            elif('CC_Chg' in row[2] or 'CC_DChg' in row[2]):
                continue                
                
            # Appends currentCycle to the cycles for every voltage, current, capacity, energy, 
            # and specific capacity and energy part of the cycle
            else:
                cycles[numFiles].append(currentCycle)
                voltages[numFiles].append(float(row[4]))
                currents[numFiles].append(1000*float(row[5]))
                capacities[numFiles].append(1000*float(row[7]))
                sCapacities[numFiles].append(float(row[8]))
                energies[numFiles].append(float(row[9]))
                sEnergies[numFiles].append(float(row[10])/1000)
                if(float(row[7]) == 0.0 and float(row[5]) >=0 and len(times[numFiles]) < currentCycle):
                    time = row[11].strip()
                    times[numFiles].append(time[11:])
                    
    # Calculates the mass by dividing the discharge capacity by the specific discharge capacity
    mass.append(round(cycleDchgCap[numFiles][0]/sCycleDchgCap[numFiles][0], 4))
    numFiles += 1
    print('File %d is %s' % (numFiles, filename))
    print('Sample mass used: %.4f g' % mass[numFiles-1])
       
# Clears every list of the stored data 
def clear():
    cycles.clear()
    voltages.clear()
    currents.clear()
    capacities.clear()
    energies.clear()
    sCapacities.clear()
    sEnergies.clear()
    cycleChgCap.clear()
    cycleDchgCap.clear()
    sCycleChgCap.clear()
    sCycleDchgCap.clear()
    cycleChgEng.clear()
    cycleDchgEng.clear()
    sCycleChgEng.clear()
    sCycleDchgEng.clear()
    mass.clear()
    times.clear()
    global numFiles
    numFiles = 0

# Prints information from the cell for the input file for each cycle
def cellInfo(fileNum = 1):
    fileNum -= 1
    for i in range(int(max(cycles[fileNum]))):
        print('Cycle %d' % (i+1))
        print('Charge Capacity: %.4f mAh, Discharge Capacity: %.4f mAh, Specific Charge Capacity: %.4f mAh/g, Specific Discharge Capacity: %.4f mAh/g' % 
              (cycleChgCap[fileNum][i], cycleDchgCap[fileNum][i], sCycleChgCap[fileNum][i], sCycleDchgCap[fileNum][i]))
        print('Charge Energy: %.4f Wh, Discharge Energy: %.4f Wh, Specific Charge Energy: %.4f Wh/g, Specific Discharge Energy: %.4f Wh/g' % 
              (cycleChgEng[fileNum][i], cycleDchgEng[fileNum][i], sCycleChgEng[fileNum][i], sCycleDchgEng[fileNum][i]))

# Changes the sample mass to a user input mass
def setMass(fileNum = 1):
    fileNum -= 1
    mass[fileNum] = float(input('Enter the new mass for File %d in grams: ' % (fileNum + 1)))
    
    # Changes all the specific capacity and energy values to be calculated with
    # the new sample mass
    for i in range(len(cycleChgCap[fileNum])):
        sCycleChgCap[fileNum][i] = cycleChgCap[fileNum][i]/mass[fileNum]
        sCycleChgEng[fileNum][i] = cycleChgEng[fileNum][i]/mass[fileNum]
        sCycleDchgCap[fileNum][i] = cycleDchgCap[fileNum][i]/mass[fileNum]
        sCycleDchgEng[fileNum][i] = cycleDchgEng[fileNum][i]/mass[fileNum]
        
    # Goes through every individual capacity to recalculate with the new mass
    for j in range(len(capacities[fileNum])):
        sCapacities[fileNum][j] = capacities[fileNum][j]/mass[fileNum]
        sEnergies[fileNum][j] = energies[fileNum][j]/mass[fileNum]

# Plots the voltage vs capacity for the input cycle
def plotVoltsVsCapacity(cycle, fileNum = 1):
    fileNum -= 1
    cycleCapacities = []
    cycleVoltages = []
    lastCap = 0.0

    # Appends voltages and capacities for the cell during the input cycle to the cycleVoltages and cycleCapacities
    # lists then plots the resulting data. The last charge capacity is added to every discharge capacity multiplied
    # by minus 1 to shift the discharge capacities so the first point is connected to the last charge capacity.
    for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
        if(currents[fileNum][i] > 0.0):
            cycleCapacities.append(sCapacities[fileNum][i])
            lastCap = sCapacities[fileNum][i]
        else:
            cycleCapacities.append(-1*sCapacities[fileNum][i] + lastCap)
        cycleVoltages.append(voltages[fileNum][i])
    plt.plot(cycleCapacities, cycleVoltages, linewidth = 2.0)
    plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.ylabel('Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the voltage vs capacity for each cycle of the input file
def plotAllCyclesVoltsVsCapacity(fileNum = 1):
    fileNum -= 1
    plt.plot(sCapacities[fileNum], voltages[fileNum], linewidth = 2.0)
    plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.ylabel('Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()

# Plots voltage vs capacity as a connected line
def plotConnectedVoltsVsCapacity(fileNum = 1):
    fileNum -= 1
    caps = []
    volts = []
    lastCCap = 0.0
    lastDCap = 0.0
    
    # During a charge cycle, each capacity and voltage is appended to their respective list
    # and the last capacity in that cycle is stored in lastCCap then added to each capacity 
    # in the discharge cycle to shift the discharge plot positive by the same amount as the 
    # final charge capacity. During the discharge cycle, the negative of the discharge capacity 
    # summed with the last charge capacity is appended to the capacity list then the last 
    # discharge capacity is stored in lastDCap to be added to each charge capacity value
    for i in range(len(sCapacities[fileNum])):
        if(currents[fileNum][i] < 0):
            volts.append(voltages[fileNum][i])
            caps.append(-1.0*sCapacities[fileNum][i] + lastCCap)
            lastDCap = caps[i]
        else:
            volts.append(voltages[fileNum][i])
            caps.append(sCapacities[fileNum][i] + lastDCap)
            lastCCap = caps[i]
    plt.plot(caps, volts, linewidth = 2.0)
    plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.ylabel('Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots voltage vs capacity between the specified cycle window
def plotVoltsVsCapacityCycleWindow(cycle1, cycle2, fileNum = 1):
        fileNum -= 1
        caps = []
        volts = []
        lastCCap = 0.0
        lastDCap = 0.0
        
        # Loops through the cycles from cycle1 to cycle2 inclusive
        for cycle in range(cycle1, cycle2+1):
            volts.append([])
            caps.append([])
            relativeIndex = 0
            
            # Loops through each index in cycle, appending voltages to volts and capacities to caps.
            # The capacities are shifted by the last capacity in the preceding charge or discharge
            # in the same way at plotConnectedVoltsVsCapacity
            for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
                if(currents[fileNum][i] < 0):
                    volts[cycle-cycle1].append(voltages[fileNum][i])
                    caps[cycle-cycle1].append(-1.0*sCapacities[fileNum][i] + lastCCap)
                    lastDCap = caps[cycle-cycle1][relativeIndex]
                else:
                    volts[cycle-cycle1].append(voltages[fileNum][i])
                    caps[cycle-cycle1].append(sCapacities[fileNum][i] + lastDCap)
                    lastCCap = caps[cycle-cycle1][relativeIndex]
                relativeIndex += 1
                
            # Each cycle is labeled with its corresponding number and is plotted with a different color
            plt.plot(caps[cycle-cycle1], volts[cycle-cycle1], linewidth = 2.0, label = 'Cycle %d' % cycle)
        plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
        plt.ylabel('Voltage (V)', fontsize = 'x-large')
        plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
        plt.show()
    
# Plots voltage vs capacity for all input files during the input cycle
def plotAllFilesVoltsVsCapacity(cycle = 1):
    
    # Loops through every file loaded
    for fileNum in range(numFiles):
        cycleCapacities = []
        cycleVoltages = []
        lastCCap = 0.0
            
        # Loops through every index of the input cycle, appending voltages to cycleVoltages
        # and capacities to cycleCapacities using the same formula as plotConnectedVoltsVsCapacity
        for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
            if(currents[fileNum][i] > 0.0):
                cycleCapacities.append(sCapacities[fileNum][i])
                lastCCap = sCapacities[fileNum][i]
            else:
                cycleCapacities.append(-1 * sCapacities[fileNum][i] + lastCCap)
            cycleVoltages.append(voltages[fileNum][i])
        plt.plot(cycleCapacities, cycleVoltages, label='File %d' % (fileNum+1), linewidth=2.0)
    plt.xlabel('Specific Capacity (mAh/g)', fontsize='x-large')
    plt.ylabel('Voltage (V)', fontsize='x-large')
    # plt.legend()
    plt.tick_params(direction='in', labelsize='large', length=5.0, top = True, right = True)
    plt.show()

    
# Plot voltage vs capacity for the voltages between vMin and vMax of the specified cycle
def plotVoltageWindow(vMin, vMax, cycle = 1, fileNum = 1):
    fileNum -= 1
    caps = []
    volts = []
    lastCCap = 0.0
    lastDCap = 0.0
    numCharges = 0
    numDischarges = 0
    
    # Loops through every index of the input cycle, appending voltages to volts and capacities to caps.
    # Capacities and voltages are only appended when the voltage is between the voltage range inclusive.
    # The last charge or discharge capacity is added to the following discharge or charge cycle, respectively
    for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
        if(currents[fileNum][i] < 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
            
            # For the first discharge capacity, the lastCCap shift is adjusted by adding the difference of
            # the last charge capacity and the sum of the first negative discharge capacity at the maximum
            # voltage and last used charge capacity to shift the discharge capacity to the last used capacity
            if(numDischarges == 0):
                lastCCap += sCapacities[fileNum][i]
                numDischarges = 1
                numCharges = 0
            caps.append(-1.0*sCapacities[fileNum][i] + lastCCap)
            volts.append(voltages[fileNum][i])
            lastDCap = -1.0*sCapacities[fileNum][i] + lastCCap
        elif(currents[fileNum][i] > 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
            if(numCharges == 0):
                lastDCap -= sCapacities[fileNum][i]
                numDischarges = 0
                numCharges = 1
            caps.append(sCapacities[fileNum][i] + lastDCap)
            volts.append(voltages[fileNum][i])
            lastCCap = sCapacities[fileNum][i] + lastDCap
    plt.plot(caps, volts, linewidth = 2.0)
    plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.ylabel('Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots every cycle of the input file between the specified voltages
def plotAllCyclesVoltageWindow(vMin, vMax, fileNum = 1):
    fileNum -= 1
    caps = []
    volts = []
    lastCCap = 0.0
    lastDCap = 0.0
    numCharges = 0
    numDischarges = 0
    
    # Loops through every cycle of the input file appending the voltage used to volts and 
    # shifted capacities to caps. Capacities are shifted using the same formula as plotVoltageWindow
    for i in range(len(sCapacities[fileNum])):
        if(currents[fileNum][i] < 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
            if(numDischarges == 0):
                lastCCap += sCapacities[fileNum][i]
                numDischarges = 1
                numCharges = 0
            caps.append(-1.0*sCapacities[fileNum][i] + lastCCap)
            volts.append(voltages[fileNum][i])
            lastDCap = -1.0*sCapacities[fileNum][i] + lastCCap
        elif(currents[fileNum][i] > 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
            if(numCharges == 0):
                lastDCap -= sCapacities[fileNum][i]
                numDischarges = 0
                numCharges = 1
            caps.append(sCapacities[fileNum][i] + lastDCap)
            volts.append(voltages[fileNum][i])
            lastCCap = sCapacities[fileNum][i] + lastDCap
    plt.plot(caps, volts, linewidth = 2.0)
    plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.ylabel('Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the voltages vs capacity for all voltages between vMin and vMax for the input cycle
def plotAllFilesVoltageWindow(vMin, vMax, cycle = 1):
    # Loops through every file
    for fileNum in range(numFiles):
        caps = []
        volts = []
        lastCCap = 0.0
        lastDCap = 0.0
        numCharges = 0
        numDischarges = 0
        
        # Loops through every index in the input cycle, appending voltages to volts and shifted capacities
        # to caps. Capacities are shifted the same way as in plotVoltageWindow.
        for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
            if(currents[fileNum][i] < 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
                if(numDischarges == 0):
                    lastCCap += sCapacities[fileNum][i]
                    numDischarges = 1
                    numCharges = 0
                caps.append(-1.0*sCapacities[fileNum][i] + lastCCap)
                volts.append(voltages[fileNum][i])
                lastDCap = -1.0*sCapacities[fileNum][i] + lastCCap
            elif(currents[fileNum][i] > 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
                if(numCharges == 0):
                    lastDCap -= sCapacities[fileNum][i]
                    numDischarges = 0
                    numCharges = 1
                caps.append(sCapacities[fileNum][i] + lastDCap)
                volts.append(voltages[fileNum][i])
                lastCCap = sCapacities[fileNum][i] + lastDCap
        plt.plot(caps, volts, linewidth = 2.0)
        plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
        plt.ylabel('Voltage (V)', fontsize = 'x-large')        
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots voltage vs capacity for voltages between vMin and vMax and cycles between cycle1 and cycle2
def plotVoltageWindowCycleWindow(vMin, vMax, cycle1, cycle2, fileNum = 1):
    fileNum -= 1
    caps = []
    volts = []
    lastCCap = 0.0
    lastDCap = 0.0
    numCharges = 0
    numDischarges = 0
        
    # Loops through the cycles between cycle1 and cycle2
    for cycle in range(cycle1, cycle2+1):
        volts.append([])
        caps.append([])
            
        # Loops through the indices of each cycle, appending voltages to volts and capacities to caps, 
        # shifting the capacities using the same formula as in plotVoltageWindow
        for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
            if(currents[fileNum][i] < 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
                if(numDischarges == 0):
                    lastCCap += sCapacities[fileNum][i]
                    numDischarges = 1
                    numCharges = 0
                caps[cycle-cycle1].append(-1.0*sCapacities[fileNum][i] + lastCCap)
                volts[cycle-cycle1].append(voltages[fileNum][i])
                lastDCap = -1.0*sCapacities[fileNum][i] + lastCCap
            elif(currents[fileNum][i] > 0 and voltages[fileNum][i] >= vMin and voltages[fileNum][i] <= vMax):
                if(numCharges == 0):
                    lastDCap -= sCapacities[fileNum][i]
                    numDischarges = 0
                    numCharges = 1
                caps[cycle-cycle1].append(sCapacities[fileNum][i] + lastDCap)
                volts[cycle-cycle1].append(voltages[fileNum][i])
                lastCCap = sCapacities[fileNum][i] + lastDCap
        plt.plot(caps[cycle-cycle1], volts[cycle-cycle1], linewidth = 2.0, label = 'Cycle %d' % cycle)
        plt.xlabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
        plt.ylabel('Voltage (V)', fontsize = 'x-large')        
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the 5 point moving average of the derivative of specific capacity as a function voltage for one cycle
def plotdQVsVolts(boxcar = 5, cycle = 1, fileNum = 1):
    fileNum -= 1
    dQ = []
    usedVoltages = []
    currentVolt = voltages[fileNum][cycles[fileNum].index(cycle)]
    index = 0
    
    # Calculates the slope between each specific capacity value and only uses points where the voltage
    # is not equal to the previous voltage to avoid division by zero
    for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
        if((voltages[fileNum][i] >= currentVolt + 0.005) or (voltages[fileNum][i] <= currentVolt - 0.005)):
            if(currents[fileNum][index] > 0 and currents[fileNum][i] < 0):
                currentVolt = voltages[fileNum][i]
                index = i
                continue
            
            if(currents[fileNum][index] > 0 and voltages[fileNum][i] >= currentVolt + 0.005):
                dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                usedVoltages.append(currentVolt)
                currentVolt = voltages[fileNum][i]
                index = i 
                
            if(currents[fileNum][index] < 0 and voltages[fileNum][i] <= currentVolt - 0.005):
                dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                usedVoltages.append(currentVolt)
                currentVolt = voltages[fileNum][i]
                index = i      
    
    # Calculates the moving average with every 5 points
    avg = np.ones(boxcar)/boxcar
    y_avg = np.convolve(dQ, avg, 'same')
    plt.xlabel('Voltage (V)', fontsize = 'x-large')
    plt.ylabel('dQ/dV (mAh/Vg)', fontsize = 'x-large')
    plt.plot(usedVoltages, y_avg, linewidth = 2.0)
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots dQ vs Voltage for the cycles given as inputs
def plotdQCycleWindow(cycle1, cycle2, boxcar = 5, fileNum = 1):
    fileNum -= 1
    dQ = []
    usedVoltages = []
    currentVolt = voltages[fileNum][cycles[fileNum].index(cycle1)]
    index = 0
    
    # Calculates the slope between each specific capacity value and only uses points where the voltage
    # is not equal to the previous voltage to avoid division by zero
    for i in range(cycles[fileNum].index(cycle1), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle2)):
        if((voltages[fileNum][i] >= currentVolt + 0.005) or (voltages[fileNum][i] <= currentVolt - 0.005)):
            if((currents[fileNum][index] > 0 and currents[fileNum][i] < 0) or (currents[fileNum][index] < 0 and currents[fileNum][i] > 0)):
                currentVolt = voltages[fileNum][i]
                index = i
                continue
            
            if(currents[fileNum][index] > 0 and voltages[fileNum][i] >= currentVolt + 0.005):
                dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                usedVoltages.append(currentVolt)
                currentVolt = voltages[fileNum][i]
                index = i 
                
            if(currents[fileNum][index] < 0 and voltages[fileNum][i] <= currentVolt - 0.005):
                dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                usedVoltages.append(currentVolt)
                currentVolt = voltages[fileNum][i]
                index = i            
     
    # Calculates the moving average with every 5 points
    avg = np.ones(boxcar)/boxcar
    y_avg = np.convolve(dQ, avg, 'same')
    plt.xlabel('Voltage (V)', fontsize = 'x-large')
    plt.ylabel('dQ/dV (mAh/Vg)', fontsize = 'x-large')
    plt.plot(usedVoltages, y_avg, linewidth = 2.0)
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the 5 point moving average of the derivative of specific capacity as a function voltage for all the cycles
def plotAllCyclesdQVsVolts(boxcar = 5, fileNum = 1):
    fileNum -= 1
    dQ = []
    usedVoltages = []
    currentVolt = voltages[fileNum][0]
    index = 0
        
    # Calculates the slope between each specific capacity value and only uses points where the voltage
    # is not equal to the previous voltage to avoid division by zero
    for i in range(len(sCapacities[fileNum])):
        if((voltages[fileNum][i] >= currentVolt + 0.005) or (voltages[fileNum][i] <= currentVolt - 0.005)):
            if((currents[fileNum][index] > 0 and currents[fileNum][i] < 0) or (currents[fileNum][index] < 0 and currents[fileNum][i] > 0)):
                currentVolt = voltages[fileNum][i]
                index = i
                continue
            
            if(currents[fileNum][index] > 0 and voltages[fileNum][i] >= currentVolt + 0.005):
                dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                usedVoltages.append(currentVolt)
                currentVolt = voltages[fileNum][i]
                index = i 
                
            if(currents[fileNum][index] < 0 and voltages[fileNum][i] <= currentVolt - 0.005):
                dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                usedVoltages.append(currentVolt)
                currentVolt = voltages[fileNum][i]
                index = i

    # Calculates the moving average with every 5 points
    avg = np.ones(boxcar)/boxcar
    y_avg = np.convolve(dQ, avg, 'same')
    plt.xlabel('Voltage (V)', fontsize = 'x-large')
    plt.ylabel('dQ/dV (mAh/Vg)', fontsize = 'x-large')
    plt.plot(usedVoltages, y_avg, linewidth = 2.0)
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots dQ vs voltage for all loaded files for the input cycle
def plotAllFilesdQVsVolts(boxcar = 5, cycle = 1):
    for fileNum in range(len(cycles)):
        dQ = []
        usedVoltages = []
        currentVolt = voltages[fileNum][cycles[fileNum].index(cycle)]
        index = 0
            
        # Calculates the slope between each specific capacity value and only uses points where the voltage
        # is not equal to the previous voltage to avoid division by zero
        for i in range(cycles[fileNum].index(cycle), len(cycles[fileNum]) - cycles[fileNum][::-1].index(cycle)):
            if((voltages[fileNum][i] >= currentVolt + 0.005) or (voltages[fileNum][i] <= currentVolt - 0.005)):
                if(currents[fileNum][index] > 0 and currents[fileNum][i] < 0):
                    currentVolt = voltages[fileNum][i]
                    index = i
                    continue
                
                if(currents[fileNum][index] > 0 and voltages[fileNum][i] >= currentVolt + 0.005):
                    dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                    usedVoltages.append(currentVolt)
                    currentVolt = voltages[fileNum][i]
                    index = i 
                
                if(currents[fileNum][index] < 0 and voltages[fileNum][i] <= currentVolt - 0.005):
                    dQ.append((sCapacities[fileNum][i] - sCapacities[fileNum][index])/(voltages[fileNum][i] - currentVolt))
                    usedVoltages.append(currentVolt)
                    currentVolt = voltages[fileNum][i]
                    index = i             
        
        # Calculates the moving average with every 5 points
        avg = np.ones(boxcar)/boxcar
        y_avg = np.convolve(dQ, avg, 'same')
        plt.xlabel('Voltage (V)', fontsize = 'x-large')
        plt.ylabel('dQ/dV (mAh/Vg)', fontsize = 'x-large')
        plt.plot(usedVoltages, y_avg, linewidth = 2.0, label = 'File %d' % (i+1))
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()    
    
# Plots the charge and discharge capacities at each cycle for the input file
def plotCapacityVsCycle(fileNum = 1, legend = False):
    fileNum -= 1
    cycle = []
    plt.figure(1)
    ax = plt.subplot(111)
    
    # Adds each cycle number to the cycle list
    for i in range(1, int(max(cycles[fileNum])) + 1):
        cycle.append(i)
        
    # Plots capacities vs cycles and labels each for the legend
    chargePlot, = ax.plot(cycle, sCycleChgCap[fileNum], 'bo', label = 'Charge', ms = 4.0)
    dischargePlot, = ax.plot(cycle, sCycleDchgCap[fileNum], 'ro', label = 'Discharge', ms = 4.0)
    
    # Add cycle start times as a label to the charge capacity
#     for i, txt in enumerate(times[fileNum]):
#         if(i > 0 and i < max(cycle)-1):
#             if((sCycleChgCap[fileNum][i] >= sCycleChgCap[fileNum][i+1] and sCycleChgCap[fileNum][i] >= sCycleChgCap[fileNum][i-1]) or (sCycleChgCap[fileNum][i] <= sCycleChgCap[fileNum][i+1] and sCycleChgCap[fileNum][i] <= sCycleChgCap[fileNum][i-1])):
#                 ax.annotate(txt, (cycle[i], sCycleChgCap[fileNum][i]))
    
    # Shrinks the plot on the x axis and puts the legend outside the plot
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
        
    # Adds cycle numbers by every 5 if there are more than 10 cycles or by 1 if there are less
    # than 10 cycles
    if(len(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots charge capacity vs cycle number for the input file
def plotChargeCapacityVsCycle(fileNum = 1):
    fileNum -= 1
    cycle = []
    for i in range(1, int(max(cycles[fileNum])) + 1):
        cycle.append(i)
        
    plt.plot(cycle, sCycleChgCap[fileNum], 'bo', ms = 4.0)
    if(len(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Charge Capacity (mAh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()

# Plots discharge capacity vs cycle number for the input file
def plotDischargeCapacityVsCycle(fileNum = 1):
    fileNum -= 1
    cycle = []
    for i in range(1, int(max(cycles[fileNum])) + 1):
        cycle.append(i)
    plt.plot(cycle, sCycleDchgCap[fileNum], 'rD', ms = 4.0)
    if(len(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Discharge Capacity (mAh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots charge and discharge capacities of every file vs the cycle number
def plotAllFilesCapacityVsCycle(legend = False):
    cycle = []
    plotted = []
    plt.figure(1)
    ax = plt.subplot(111)
    
    # Iterates through each file that has been loaded
    for fileNum in range(len(cycles)):
        cycle.clear()
        for i in range(1, int(max(cycles[fileNum])) + 1):
            cycle.append(i)
        chargePlot, = ax.plot(cycle, sCycleChgCap[fileNum], 'C%do' % fileNum, label = 'File %d Charge' % (fileNum + 1), ms = 4.0,  fillstyle = 'none')
        dischargePlot, = ax.plot(cycle, sCycleDchgCap[fileNum], 'C%do' % fileNum, label = 'File %d Discharge' % (fileNum + 1), ms = 4.0)
        plotted.append(chargePlot)
        plotted.append(dischargePlot)
        
    # Plots a legend if the parameter is true. Shrinks the plot to place the legend outside the plot
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
    
    # Sets the ticks on the x axis based on the maximum number of cycles of all the files
    maxCycle = 0
    for i in range(numFiles):
        if(max(cycles[i]) > maxCycle):
            maxCycle = max(cycles[i])
    if(maxCycle > 15):
        plt.xticks([x for x in range(5, maxCycle + 1, 5)])
    else:
        plt.xticks([x for x in range(1, maxCycle + 1)])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots charge and discharge capacities for the cycles between cycle1 and cycle2 inclusive.
def plotCapacityVsCycleWindow(cycle1, cycle2, fileNum = 1, legend = False):
    fileNum -= 1
    cycle = []
    cycleChg = []
    cycleDchg = []
    plt.figure(1)
    ax = plt.subplot(111)
    
    # Adds each cycle number to the cycle list
    for i in range(cycle1, cycle2+1):
        cycle.append(i)
        cycleChg.append(sCycleChgCap[fileNum][i-1])
        cycleDchg.append(sCycleDchgCap[fileNum][i-1])
        
    # Plots capacities vs cycles and labels each for the legend
    chargePlot, = ax.plot(cycle, cycleChg, 'bo', label = 'Charge', ms = 4.0)
    dischargePlot, = ax.plot(cycle, cycleDchg, 'ro', label = 'Discharge', ms = 4.0)
    
    # Shrinks the plot on the x axis and puts the legend outside the plot
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
        
    if(len(cycle) > 15):
        plt.xticks([x for x in range(5, cycle2+1, 5)])
    else:
        plt.xticks([x for x in range(cycle1, cycle2+1)])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()

# Plots charge and discharge capacities for cycles within the cycle range for all files, cycle2 inclusive
def plotAllFilesCapacityVsCycleWindow(cycle1, cycle2, legend = False):
    cycle = []
    cycleChg = []
    cycleDchg = []
    plotted = []
    plt.figure(1)
    ax = plt.subplot(111)
    
    # Iterates through each file that has been loaded
    for fileNum in range(numFiles):
        cycle.clear()
        cycleChg.clear()
        cycleDchg.clear()
        for i in range(cycle1, cycle2+1):
            cycle.append(i)
            cycleChg.append(sCycleChgCap[fileNum][i-1])
            cycleDchg.append(sCycleDchgCap[fileNum][i-1])
        chargePlot, = ax.plot(cycle, cycleChg, 'C%do' % fileNum, label = 'File %d Charge' % (fileNum + 1), ms = 4.0,  fillstyle = 'none')
        dischargePlot, = ax.plot(cycle, cycleDchg, 'C%do' % fileNum, label = 'File %d Discharge' % (fileNum + 1), ms = 4.0)
        plotted.append(chargePlot)
        plotted.append(dischargePlot)
        
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
    
    # Sets the ticks on the x axis based on the maximum number of cycles of all the files
    if(cycle2-cycle1+1 > 15):
        plt.xticks([x for x in range(5, cycle2 + 1, 5)])
    else:
        plt.xticks([x for x in range(cycle1, cycle2+1)])
        
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Capacity (mAh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots charge and discharge energy vs cycle number for the input file
def plotEnergyVsCycle(fileNum = 1):
    fileNum -= 1
    cycle = []
    plt.figure(1)
    ax = plt.subplot(111)
    for i in range(1, int(max(cycles[fileNum])) + 1):
        cycle.append(i)
    chargePlot, = ax.plot(cycle, sCycleChgEng[fileNum], 'bo', label = 'Charge', ms = 4.0)
    dischargePlot, = ax.plot(cycle, sCycleDchgEng[fileNum], 'ro', label = 'Discharge', ms = 4.0)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
    ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1 ,1), fontsize = 'small')
    if(len(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Energy (Wh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()

# Plots the charge energy vs cycle number for the input file
def plotChargeEnergyVsCycle(fileNum = 1):
    fileNum -= 1
    cycle = []
    for i in range(1, int(max(cycles[fileNum])) + 1):
        cycle.append(i)
    plt.plot(cycle, sCycleChgEng[fileNum], 'bo', ms = 4.0)
    if(len(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Charge Energy (Wh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()

# Plots discharge energy vs cycle number for the input file
def plotDischargeEnergyVsCycle(fileNum = 1):
    fileNum -= 1
    cycle = []
    for i in range(1, int(max(cycles[fileNum])) + 1):
        cycle.append(i)
    plt.plot(cycle, sCycleDchgEng[fileNum], 'ro', ms = 4.0)
    if(len(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Discharge Energy (Wh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots charge and discharge energy of every file vs cycle number
def plotAllFilesEnergyVsCycle():
    cycle = []
    plotted = []
    plt.figure(1)
    ax = plt.subplot(111)
    for fileNum in range(len(cycles)):
        cycle.clear()
        for i in range(1, int(max(cycles[fileNum])) + 1):
            cycle.append(i)
        chargePlot, = ax.plot(cycle, sCycleChgEng[fileNum], 'C%do' % fileNum, label = 'File %d Charge' % (fileNum + 1), ms = 4.0,  fillstyle = 'none')
        dischargePlot, = ax.plot(cycle, sCycleDchgEng[fileNum], 'C%do' % fileNum, label = 'File %d Discharge' % (fileNum + 1), ms = 4.0)
        plotted.append(chargePlot)
        plotted.append(dischargePlot)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
    ax.legend(handles = plotted, loc = 2, bbox_to_anchor = (1 ,1), fontsize = 'small')
    maxCycle = 0
    for i in range(numFiles):
        if(max(cycles[i]) > maxCycle):
            maxCycle = max(cycles[i])
    if(maxCycle > 15):
        plt.xticks([x for x in range(5, max(cycle) + 1, 5)])
    else:
        plt.xticks([x for x in range(1, maxCycle + 1)])
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Specific Energy (Wh/g)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the average voltage of a cycle vs the cycle number for all cycles
def plotAverageVoltageVsCycle(fileNum = 1, legend = False):
    fileNum -= 1
    averageChgVoltage = []
    averageDchgVoltage = []
    cycle = []
    plt.figure(1)
    ax = plt.subplot(111)
        
    # Loops through every cycle of the file
    for i in range(1, max(cycles[fileNum])+1):
        cycle.append(i)
        cycleChgVoltages = []
        cycleDchgVoltages = []
        
        # Loops through the indices of the cycle to append either charge or discharge voltages to the
        # respective cycle depending on if the current is positive or negative
        for j in range(cycles[fileNum].index(i), len(cycles[fileNum]) - cycles[fileNum][::-1].index(i)):
            if(currents[fileNum][j] >= 0):
                cycleChgVoltages.append(voltages[fileNum][j])
            else:
                cycleDchgVoltages.append(voltages[fileNum][j])
        
        # Averages the charge and discharge voltages for plotting
        averageChgVoltage.append(np.average(cycleChgVoltages))
        averageDchgVoltage.append(np.average(cycleDchgVoltages))
    
    # Plots the cycle numbers and average voltages
    chargePlot, = plt.plot(cycle, averageChgVoltage, 'bo', label = 'Charge', ms = 4.0)
    dischargePlot, = plt.plot(cycle, averageDchgVoltage, 'ro', label = 'Discharge', ms = 4.0)
    
    # Picks tick values depending on if there are more than 10 cycles or not
    # Ticks by 5 for cells with more than 10 cycles or by 1 otherwise
    if(max(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
        
    # Plots a legend if it is entered as a parameter
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
        
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Average Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the average voltage of a cycle vs cycle number for the cycles between cycle1 and cycle2 inclusive
def plotAverageVoltageVsCycleWindow(cycle1, cycle2, fileNum = 1, legend = False):
    fileNum -= 1
    averageChgVoltage = []
    averageDchgVoltage = []
    cycle = []
    plt.figure(1)
    ax = plt.subplot(111)
    
    # Loops through every cycle of the file
    for i in range(cycle1, cycle2+1):
        cycle.append(i)
        cycleChgVoltages = []
        cycleDchgVoltages = []
        
        # Loops through the indices of the cycle to append either charge or discharge voltages to the
        # respective cycle depending on if the current is positive or negative
        for j in range(cycles[fileNum].index(i), len(cycles[fileNum]) - cycles[fileNum][::-1].index(i)):
            if(currents[fileNum][j] >= 0):
                cycleChgVoltages.append(voltages[fileNum][j])
            else:
                cycleDchgVoltages.append(voltages[fileNum][j])
        
        # Averages the charge and discharge voltages for plotting
        averageChgVoltage.append(np.average(cycleChgVoltages))
        averageDchgVoltage.append(np.average(cycleDchgVoltages))
    
    # Plots the cycle numbers and average voltages
    chargePlot, = plt.plot(cycle, averageChgVoltage, 'bo', label = 'Charge', ms = 4.0)
    dischargePlot, = plt.plot(cycle, averageDchgVoltage, 'ro', label = 'Discharge', ms = 4.0)
    
    # Picks tick values depending on if there are more than 10 cycles or not
    # Ticks by 5 for cells with more than 10 cycles or by 1 otherwise
    if(cycle2-cycle1+1 > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
        
    # Plots a legend if it is entered as a parameter
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
        
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Average Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the average voltage of all cycles for all loaded files
def plotAllFilesAverageVoltageVsCycle(legend = False):
    plt.figure(1)
    ax = plt.subplot(111)
    
    for fileNum in range(numFiles):
        averageChgVoltage = []
        averageDchgVoltage = []
        cycle = []
            
        # Loops through every cycle of the file
        for i in range(1, max(cycles[fileNum])+1):
            cycle.append(i)
            cycleChgVoltages = []
            cycleDchgVoltages = []
            
            # Loops through the indices of the cycle to append either charge or discharge voltages to the
            # respective cycle depending on if the current is positive or negative
            for j in range(cycles[fileNum].index(i), len(cycles[fileNum]) - cycles[fileNum][::-1].index(i)):
                if(currents[fileNum][j] >= 0):
                    cycleChgVoltages.append(voltages[fileNum][j])
                else:
                    cycleDchgVoltages.append(voltages[fileNum][j])
            
            # Averages the charge and discharge voltages for plotting
            averageChgVoltage.append(np.average(cycleChgVoltages))
            averageDchgVoltage.append(np.average(cycleDchgVoltages))
        
        # Plots the cycle numbers and average voltages
        chargePlot, = plt.plot(cycle, averageChgVoltage, 'C%do' % fileNum, label = 'File %d Charge' % (fileNum+1), ms = 4.0, fillstyle = 'none')
        dischargePlot, = plt.plot(cycle, averageDchgVoltage, 'C%do' % fileNum, label = 'File %d Discharge' % (fileNum+1), ms = 4.0)

    # Picks tick values depending on if there are more than 10 cycles or not
    # Ticks by 5 for cells with more than 10 cycles or by 1 otherwise
    if(max(cycle) > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
        
    # Plots a legend if it is entered as a parameter
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
        
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Average Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the average voltage of every cycle between cycle1 and cycle2 inclusive vs cycle number for all files
def plotAllFilesAverageVoltageVsCycleWindow(cycle1, cycle2, legend = False):
    plt.figure(1)
    ax = plt.subplot(111)
    
    for fileNum in range(numFiles):
        averageChgVoltage = []
        averageDchgVoltage = []
        cycle = []
            
        # Loops through every cycle of the file
        for i in range(cycle1, cycle2+1):
            cycle.append(i)
            cycleChgVoltages = []
            cycleDchgVoltages = []
            
            # Loops through the indices of the cycle to append either charge or discharge voltages to the
            # respective cycle depending on if the current is positive or negative
            for j in range(cycles[fileNum].index(i), len(cycles[fileNum]) - cycles[fileNum][::-1].index(i)):
                if(currents[fileNum][j] >= 0):
                    cycleChgVoltages.append(voltages[fileNum][j])
                else:
                    cycleDchgVoltages.append(voltages[fileNum][j])
            
            # Averages the charge and discharge voltages for plotting
            averageChgVoltage.append(np.average(cycleChgVoltages))
            averageDchgVoltage.append(np.average(cycleDchgVoltages))
        
        # Plots the cycle numbers and average voltages
        chargePlot, = plt.plot(cycle, averageChgVoltage, 'C%do' % fileNum, label = 'File %d Charge' % (fileNum+1), ms = 4.0, fillstyle = 'none')
        dischargePlot, = plt.plot(cycle, averageDchgVoltage, 'C%do' % fileNum, label = 'File %d Discharge' % (fileNum+1), ms = 4.0)
        
    # Picks tick values depending on if there are more than 10 cycles or not
    # Ticks by 5 for cells with more than 10 cycles or by 1 otherwise
    if(cycle2-cycle1+1 > 15):
        plt.xticks([x for x in cycle[4::5]])
    else:
        plt.xticks([x for x in cycle])
        
    # Plots a legend if it is entered as a parameter
    if(legend):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        ax.legend(handles = [chargePlot, dischargePlot], loc = 2, bbox_to_anchor = (1, 1), fontsize = 'small')
        
    plt.xlabel('Cycle Number', fontsize = 'x-large')
    plt.ylabel('Average Voltage (V)', fontsize = 'x-large')
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.show()
    
# Plots the first charge and discharge capacities at C rates from C/20 to 5C
def plotCapacityVsRate():
    for file in range(0, numFiles - 1, 7):
        chg = []
        dchg = []
        plotCurrent = []
        plotCurrents = []
        count = 0
        for i in range(file, file + 7):
            chg.append([])
            dchg.append([])
            
            # Calculates the rates by dividing the current by the mass
            # and if less than 7 files are loaded, the rate at the zero
            # file is appended instead
            if (i < numFiles):
                plotCurrent.append(currents[i][1]/mass[i])
                plotCurrents.append(currents[i][1]/mass[i])
            else:
                plotCurrent.append(currents[0][1]/mass[0])
                plotCurrents.append(currents[0][1]/mass[0])
                
            # Appends the charge and discharge capacities or zero if there are 
            # less than 7 files loaded
            if(i < numFiles):          
                chg[count].append(sCycleChgCap[i][0])
                dchg[count].append(sCycleDchgCap[i][0])
            else:
                chg[count].append(0)
                dchg[count].append(0)
            count += 1
            
        # Makes the x-axis a logarithmic scale and makes the rates for the last loaded
        # file the x-axis values
        plt.xscale('log')
        plt.xticks([x for x in plotCurrents],[round(x, 0) for x in plotCurrents])
        plt.plot(plotCurrent, chg, 'C%do' % (file/7), ms = 5.0,  fillstyle = 'none')
        plt.plot(plotCurrent, dchg, 'C%do' % (file/7), ms = 5.0)
        plt.xlabel('Current (mA/g)', fontsize = 'x-large')
        plt.ylabel('Capacity (mAh/g)', fontsize = 'x-large')
    plt.minorticks_off()
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.xlim((9, 1250))
    plt.show()
    
# Plots the first 10 discharge capacities vs the rate the cell was run at
def plotDischargeVsRate():
    for file in range(0, numFiles - 1, 7):
        dchg = []
        plotCurrent = []
        plotCurrents = []
        count = 0
        for i in range(file, file + 7):
            dchg.append([])
            if (i < numFiles):
                plotCurrent.append(currents[i][1]/mass[i])
                plotCurrents.append(currents[i][1]/mass[i])
            else:
                plotCurrent.append(currents[0][1]/mass[0])
                plotCurrents.append(currents[0][1]/mass[0])
                
            # Appends the discharge capacity if it exists and if not, appends a 0            
            for j in range(10):
                if(i < numFiles and j < max(cycles[i])):
                    dchg[count].append(sCycleDchgCap[i][j])
                else:
                    dchg[count].append(0)
            count += 1
        plt.xscale('log')
        plt.xticks([x for x in plotCurrents],[round(x, 0) for x in plotCurrents])
        plt.plot(plotCurrent, dchg, 'C%do' % (file/7), ms = 5.0)
        plt.xlabel('Current (mA/g)', fontsize = 'x-large')
        plt.ylabel('Discharge Capacity (mAh/g)', fontsize = 'x-large')
    plt.minorticks_off()
    plt.tick_params(direction='in', labelsize = 'large', length = 5.0, top = True, right = True)
    plt.xlim((9, 1250))
    plt.show()
    
# Runs plotting methods to generate 3 plots for the input file
def plot(fileNum = 1):
    plotConnectedVoltsVsCapacity(fileNum)
    plotCapacityVsCycle(fileNum)
    plotAllFilesCapacityVsCycle()
    
# Runs methods generating overlaid cycling curves for all entered files
def overlay(boxcar = 5, cycle = 1):
    plotAllFilesVoltsVsCapacity(cycle)
    plotAllFilesdQVsVolts(boxcar, cycle)
    
# Runs methods to plot the capacity vs rate
def rate():
    plotCapacityVsRate()
    plotDischargeVsRate()
    
print('\nAvailable Functions:')
print('newFile()')
print('clear()')
print('setMass(fileNum = 1)')
print('cellInfo(fileNum = 1)')
print('plotVoltsVsCapacity(cycle, fileNum = 1)')
print('plotAllCyclesVoltsVsCapacity(fileNum = 1)')
print('plotConnectedVoltsVsCapacity(fileNum = 1)')
print('plotVoltsVsCapacityCycleWindow(cycle1, cycle2, fileNum = 1)')
print('plotAllFilesVoltsVsCapacity(cycle = 1)')
print('plotVoltageWindowCycleWindow(vMin, vMax, cycle1, cycle2, fileNum = 1)')
print('plotVoltageWindow(vMin, vMax, cycle = 1, fileNum = 1)')
print('plotAllCyclesVoltageWindow(vMin, vMax, fileNum = 1)')
print('plotAllFilesVoltageWindow(vMin, vMax, cycle = 1)')
print('plotdQVsVolts(boxcar = 5, cycle = 1, fileNum = 1)')
print('plotdQCycleWindow(cycle1, cycle2, boxcar = 5, fileNum = 1)')
print('plotAllCyclesdQVsVolts(boxcar = 5, fileNum = 1)')
print('plotAllFilesdQVsVolts(boxcar = 5, cycle = 1)')
print('plotCapacityVsCycle(fileNum = 1, legend = False)')
print('plotChargeCapacityVsCycle(fileNum = 1)')
print('plotDischargeCapacityVsCycle(fileNum = 1)')
print('plotAllFilesCapacityVsCycle(legend = False)')
print('plotCapacityVsCycleWindow(cycle1, cycle2, fileNum = 1, legend = False)')
print('plotAllFilesCapacityVsCycleWindow(cycle1, cycle2, legend = False)')
print('plotEnergyVsCycle(fileNum = 1)')
print('plotChargeEnergyVsCycle(fileNum = 1)')
print('plotDischargeEnergyVsCycle(fileNum = 1)')
print('plotAllFilesEnergyVsCycle()')
print('plotAverageVoltageVsCycle(fileNum = 1, legend = False)')
print('plotAverageVoltageVsCycleWindow(cycle1, cycle2, fileNum = 1, legend = False)')
print('plotAllFilesAverageVoltageVsCycle(legend = False)')
print('plotAllFilesAverageVoltageVsCycleWindow(cycle1, cycle2, legend = False)')
print('plotCapacityVsRate()')
print('plotDischargeVsRate()')
print('plot(fileNum = 1)')
print('overlay(boxcar = 5, cycle = 1)')
print('rate()\n')

newFile()
# plotAllFilesAverageVoltageVsCycle()
# plot()
# plotCapacityVsCycle()
# plotAverageVoltageVsCycle()
# plotAverageVoltageVsCycle(1, True)
# plotAverageVoltageVsCycleWindow(1,6)
# plotCapacityVsCycleWindow(1, 15)
# plotAllFilesCapacityVsCycleWindow(1,6)
# plotVoltageWindowCycleWindow(3.5, 4.2, 1, 13)
# plotAllCyclesVoltageWindow(2.3, 6)
# plotVoltsVsCapacityCycleWindow(1, 12)
# plotAllFilesVoltsVsCapacity(1)
# plotAllCyclesVoltsVsCapacity(1)
# plotConnectedVoltsVsCapacity(1)
# plotVoltsVsCapacity(1)
# plotVoltageWindow(3.5,4.1)
# plotAllFilesVoltageWindow(3.5,4.1)
# plot()
# plotAllCyclesdQVsVolts()
# plotdQCycleWindow(1,2, 5)
# plotAllFilesdQVsVolts(5, 1)
# plotCapacityVsRate()
# plotDischargeVsRate()
# plotAllFilesCapacityVsCycle()
# plotdQVsVolts(20, 2, 1)
# cellInfo(1)
# setMass(1)
# plotChargeCapacityVsCycle(1)
# plotDischargeCapacityVsCycle(1)
# plotEnergyVsCycle(1)
# plotChargeEnergyVsCycle(1)
# plotDischargeEnergyVsCycle(1)
# plotAllFilesCapacityVsCycle()
# plotAllFilesEnergyVsCycle()