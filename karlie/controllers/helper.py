import pandas as pd
import re
import numpy as np
import sys


def scale_user_input_to_float(limit):
    return None if limit == "" else float(limit)


def get_selected_cycles_list(selected_cycles):
    # change from string to list of integers
    selected_cycles_list = selected_cycles.split(',')
    selected_cycles_list = [i.strip() for i in selected_cycles_list]
    if '' in selected_cycles_list:
        selected_cycles_list.remove('')

    selected_cycles_list = [int(i)for i in selected_cycles_list]

    return selected_cycles_list


def validate_cycles(all_cycles, selected_cycles):

    if selected_cycles == "all":
        return True, ''
    else:
        # pattern check
        if not re.search("^((\s*\d+\s*,{1}\s*)|\s*\d+\s*)+$", selected_cycles):
            all_cycles_string = ", ".join([str(i) for i in all_cycles])
            return False, "Error: Cycle input incorrect format. Should be something like this {}".format(all_cycles_string)

        # change from string to list of integers
        selected_cycles_list = get_selected_cycles_list(selected_cycles)
        # selected_cycles_list = selected_cycles.split(',')
        # selected_cycles_list = [i.strip() for i in selected_cycles_list]
        # if '' in selected_cycles_list:
        #     selected_cycles_list.remove('')

        # range and duplicate check
        cycle_set = set()
        for cycle_number in selected_cycles_list:
            # found duplicate
            if cycle_number in cycle_set:
                return False, "Error: Cycle input incorrect format. {} appears multiple times".format(cycle_number)
            else:
                cycle_set.add(cycle_number)

            # cycle out of range.
            if int(cycle_number) not in all_cycles.tolist():
                return False, "Error: Cycle input incorrect format. Cycle number {} does not exist".format(cycle_number)

        return True, ''


def validate_channels(selected_channels):
    if selected_channels == "all":
        return True, ''
    else:
        # check pattern
        if not re.search("^(\s*\d+\s*)$", selected_channels):
            return False, "Error: Channel input incorrect format. Input should be a number from 1 to 64".format(1)

        # range check
        selected_channels = int(selected_channels.strip())
        if not (1 <= selected_channels <= 64):
            return False, "Error: Channel input incorrect format. Input should be a number from 1 to 64".format(1)

    return True, ''


def get_unique_cycles(data):
    return data.Cycle.unique()


def get_unique_channels(data):
    return [i for i in range(1, 65)]


def get_charge_from_selected_cycles(selected_cycles):
    # get charge cycles from user selected cycles
    charge_cycles = []
    for cycle in selected_cycles:
        if cycle % 2 != 0:
            charge_cycles.append(cycle)


def get_discharge_from_selected_cycles(selected_cycles):
    # get discharge from user selected cycles
    discharge_cycles = []
    for cycle in selected_cycles:
        if cycle % 2 == 0:
            discharge_cycles.append(cycle)


def get_medusa_columns(mapping):
    if mapping == "karlie":
        starting_row = 7
        columns = {"Cycle", "Time(h)", "VSet (V)", "Vavg (V)"}
        for channel_number in range(1, 65):
            columns.add("Ch.{}-I (uA)".format(channel_number))
        return columns, starting_row
    elif mapping == "eloi":
        starting_row = 71
        columns = {"Time", "Total_I", "Cell_E", "Base_E", "Group_E", "I_(1,1)", "I_(2,1)", "I_(3,1)", "I_(4,1)", "I_(5,1)", "I_(6,1)", "I_(7,1)", "I_(8,1)", "I_(9,1)", "I_(10,1)", "I_(1,2)", "I_(2,2)", "I_(3,2)", "I_(4,2)", "I_(5,2)", "I_(6,2)", "I_(7,2)", "I_(8,2)", "I_(9,2)", "I_(10,2)", "I_(1,3)", "I_(2,3)", "I_(3,3)", "I_(4,3)", "I_(5,3)", "I_(6,3)", "I_(7,3)", "I_(8,3)", "I_(9,3)", "I_(10,3)", "I_(1,4)", "I_(2,4)", "I_(3,4)", "I_(4,4)", "I_(5,4)", "I_(6,4)", "I_(7,4)", "I_(8,4)", "I_(9,4)", "I_(10,4)", "I_(1,5)", "I_(2,5)", "I_(3,5)", "I_(4,5)", "I_(5,5)", "I_(6,5)", "I_(7,5)", "I_(8,5)", "I_(9,5)", "I_(10,5)", "I_(1,6)", "I_(2,6)", "I_(3,6)", "I_(4,6)", "I_(5,6)", "I_(6,6)", "I_(7,6)", "I_(8,6)", "I_(9,6)", "I_(10,6)", "I_(1,7)", "I_(2,7)", "I_(3,7)", "I_(4,7)", "I_(5,7)", "I_(6,7)", "I_(7,7)", "I_(8,7)", "I_(9,7)", "I_(10,7)", "I_(1,8)", "I_(2,8)", "I_(3,8)", "I_(4,8)", "I_(5,8)", "I_(6,8)", "I_(7,8)", "I_(8,8)", "I_(9,8)", "I_(10,8)", "I_(1,9)", "I_(2,9)", "I_(3,9)", "I_(4,9)", "I_(5,9)", "I_(6,9)", "I_(7,9)", "I_(8,9)", "I_(9,9)", "I_(10,9)", "I_(1,10)", "I_(2,10)", "I_(3,10)", "I_(4,10)", "I_(5,10)", "I_(6,10)", "I_(7,10)", "I_(8,10)", "I_(9,10)", "I_(10,10)"}
        return columns, starting_row
    else:
        return {}


def change_col_name_eloi_mapping(data):
    add_cycle_column_in_eloi_mapping(data)
    channel_names = ['6,9', '10,9', '4,10', '8,10', '2,8', '6,8', '10,8', '2,9',
                     '5,9', '9,9', '3,10', '7,10', '1,8', '5,8', '9,8', '1,9',
                     '4,9', '8,9', '2,10', '6,10', '10,10', '4,8', '8,8', '4,4',
                     '3,9', '7,9', '1,10', '5,10', '9,10', '3,8', '7,8', '3,4',
                     '2,5', '10,7', '6,7', '2,7', '8,6', '4,6', '10,5', '6,5',
                     '1,5', '9,7', '5,7', '1,7', '7,6', '3,6', '9,5', '5,5',
                     '2,4', '8,7', '4,7', '10,6', '6,6', '2,6', '8,5', '4,5',
                     '1,4', '7,7', '3,7', '9,6', '5,6', '1,6', '7,5', '3,5']
    column_mapping = {'Cell_E': 'Vavg (V)', 'Time': 'Time(h)'}
    for index, channel_name in enumerate(channel_names):
        channel_number = index + 1
        column_mapping['I_({})'.format(channel_name)] = "Ch.{}-I (uA)".format(channel_number)

    data.rename(columns=column_mapping, inplace=True)


def add_cycle_column_in_eloi_mapping(data):
    # eloi mapping does not have cycles in the data
    # so everytime the time is zero I increment the cycle number
    # and add a column of Cycle in the data
    zero_index = data.index[data['Time'] == 0].tolist()
    number_of_rows = data.shape[0]
    cycle_number = 0
    cycle_data = []
    for index in range(number_of_rows):
        if index in zero_index:
            cycle_number += 1
        cycle_data.append(cycle_number)

    data['Cycle'] = cycle_data


def get_mass_columns():
    columns = {"Cycle", "Name"}
    for channel_number in range(1, 65):
        columns.add("Channel {}".format(channel_number))
    return columns


def get_charges(data, selected_channels_list, mass_data):
    # calculate charges
    x_min, x_max = sys.maxsize, -sys.maxsize - 1
    y_min, y_max = min(data.loc[:, "Vavg (V)"].values), max(data.loc[:, "Vavg (V)"].values)
    charges = {}
    for channel_number in selected_channels_list:
        charges[channel_number] = {}
        accumulated_charge = 0
        current = data.loc[:, "Ch.{}-I (uA)".format(channel_number)].apply(lambda x: x / 1000).values
        time_h = data.loc[:, "Time(h)"].values
        voltages = data.loc[:, "Vavg (V)"].values
        cycle = data.loc[:, "Cycle"].values
        mass = 1
        if mass_data is not None:
            mass = mass_data[channel_number - 1]
        for index in range(len(time_h) - 1):
            # formula to calculate charges
            cycle_number = cycle[index]
            if cycle_number not in charges[channel_number]:
                charges[channel_number][cycle_number] = {'charge': [], 'voltage': []}
            avg_charge = (current[index] + current[index + 1]) / 2
            time_diff = time_h[index + 1] - time_h[index]
            charge = avg_charge * time_diff
            accumulated_charge += charge/mass
            voltage = voltages[index]

            charges[channel_number][cycle_number]['charge'].append(accumulated_charge)
            charges[channel_number][cycle_number]['voltage'].append(voltage)

            x_min = min(accumulated_charge, x_min)
            x_max = max(accumulated_charge, x_max)

    return charges, x_min, x_max, y_min, y_max


def get_capacity(data, selected_cycles_list, selected_channels_list, mass_data):
    # calculate charges
    x_min, x_max = min(selected_cycles_list), max(selected_cycles_list)
    y_min, y_max = sys.maxsize, -sys.maxsize - 1
    charges = {}
    charges_pos = {}
    charges_neg = {}
    avg_volts_pos = {}
    avg_volts_neg = {}
    for channel_number in selected_channels_list:
        charges[channel_number] = {}
        charges_pos[channel_number] = {}
        charges_neg[channel_number] = {}
        avg_volts_pos[channel_number] = {}
        avg_volts_neg[channel_number] = {}
        # get mass data
        mass = 1
        if mass_data is not None:
            mass = mass_data[channel_number - 1]
        for cycle_number in selected_cycles_list:
            charges[channel_number][cycle_number] = 0
            charges_pos[channel_number][cycle_number] = 0
            charges_neg[channel_number][cycle_number] = 0
            cycle_data = data[data['Cycle'] == cycle_number]
            current = cycle_data.loc[:, "Ch.{}-I (uA)".format(channel_number)].values
            time_h = cycle_data.loc[:, "Time(h)".format(channel_number)].values
            voltages = cycle_data.loc[:, "Vavg (V)".format(channel_number)].values
            charge = 0
            charge_pos = 0
            charge_neg = 0
            avg_volt_charge_pos = 0
            avg_volt_charge_neg = 0
            for index in range(len(time_h) - 2):
                # formula to calculate charges
                avg_charge = (current[index] + current[index + 1]) / 2
                time_diff = time_h[index + 1] - time_h[index]
                charge += avg_charge * time_diff
                if avg_charge * time_diff >= 0:
                    charge_pos += avg_charge * time_diff
                    avg_volt_charge_pos += ((voltages[index + 1] + voltages[index])/2) * avg_charge * time_diff
                else:
                    charge_neg += avg_charge * time_diff
                    avg_volt_charge_neg += ((voltages[index + 1] + voltages[index])/2) * avg_charge * time_diff
            if cycle_number % 2 == 0:
                charges[channel_number][cycle_number] = charge/(mass * 1000) * -1
            else:
                charges[channel_number][cycle_number] = charge / (mass * 1000)
            charges_pos[channel_number][cycle_number] = charge_pos/(mass * 1000)
            charges_neg[channel_number][cycle_number] = charge_neg/(mass * 1000) * -1 
            if charge_pos != 0:
                avg_volts_pos[channel_number][cycle_number] = avg_volt_charge_pos/charge_pos
            if charge_neg != 0:
                avg_volts_neg[channel_number][cycle_number] = avg_volt_charge_neg/charge_neg
            
            y_min = min(charges[channel_number][cycle_number], y_min)
            y_max = max(charges[channel_number][cycle_number], y_max)

    return charges, charges_pos, charges_neg, avg_volts_pos, avg_volts_neg, x_min, x_max, y_min, y_max

# Get "real" capacities and average voltages which include the residual
# charging/discharging that occurs after a change in step
def get_compensated_echem_values(data, selected_channels_list, mass_data):
    true_caps = {}
    true_avg_volts = {}
    
    for channel_number in selected_channels_list:
        true_avg_volts[channel_number] = {}
        true_caps[channel_number] = {}

        
        currents = data.loc[:, "Ch.{}-I (uA)".format(channel_number)].values
        times = data.loc[:, "Time(h)"].values
        volts = data.loc[:, "Vavg (V)"].values
        cycles = data.loc[:, 'Cycle'].values

        mass = 1
        if mass_data is not None:
            mass = mass_data[channel_number - 1]
        
        is_charging = (volts[3] > volts[0])
            
        current = 0
        sum_Q = 0
        volt = 0
        count = 0
        cycle_number = cycles[0]
        
        for i in range(len(currents) - 3):
            if is_charging:
                if currents[i] > 0:
                    d_t = times[i+1] - times[i]
                    Q = ((currents[i] + currents[i+1])/2)
                    current += Q * d_t
                    volt += volts[i] * Q * d_t
                    count += 1
                else:
                    if currents[i+1] < 0 and currents[i+2] < 0 and volts[i+2] < volts[i]: # change from charge to discharge when three consecutive negative values 
                        print(i, "discharge begin", cycle_number) 
                        true_caps[channel_number][cycle_number] = current/mass/1000
                        true_avg_volts[channel_number][cycle_number] = volt/current
                        count = 1
                        Q = ((currents[i] + currents[i+1])/2)
                        current = Q * d_t
                        volt = volts[i] * Q * d_t
                        is_charging = False
                        cycle_number += 1

            else:
                if currents[i] < 0:
                    d_t = times[i+1] - times[i]
                    Q = ((currents[i] + currents[i+1])/2)
                    current += Q * d_t
                    volt += volts[i] * Q * d_t
                    count += 1
                else:
                    if currents[i+1] > 0 and currents[i+2] > 0 and volts[i+2] > volts[i]: # change from discharge to charge when three consecutive positive values 
                        print(i, "charge begin", cycle_number)
                        true_caps[channel_number][cycle_number] = current/mass/1000 * -1
                        true_avg_volts[channel_number][cycle_number] = volt/current
                        count = 1
                        Q = ((currents[i] + currents[i+1])/2)
                        current = Q * d_t
                        volt = volts[i] * Q * d_t
                        is_charging = True
                        cycle_number += 1

        
        true_caps[channel_number][cycle_number] = abs(current/mass/1000)
        true_avg_volts[channel_number][cycle_number] = volt/current

        is_charging = True

    print(cycle_number)
    return true_caps, true_avg_volts

def get_norm_cur_voltage(data, selected_cycles_list, selected_channels_list, mass_data):
    # calculate charges
    x_min, x_max = sys.maxsize, -sys.maxsize - 1
    y_min, y_max = sys.maxsize, -sys.maxsize - 1
    norm_cur_voltage = {}
    for channel_number in selected_channels_list:
        norm_cur_voltage[channel_number] = {}
        # get mass data
        mass = 1
        if mass_data is not None:
            mass = mass_data[channel_number - 1]
        for cycle_number in selected_cycles_list:
            norm_cur_voltage[channel_number][cycle_number] = {}
            # get selected cycle data
            cycle_data = data[data['Cycle'] == cycle_number]
            # get voltage
            voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
            # get current
            current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].apply(lambda x: x / (1000 * mass))
            current_cycle = current_cycle.values
            norm_cur_voltage[channel_number][cycle_number]['current'] = current_cycle
            norm_cur_voltage[channel_number][cycle_number]['voltage'] = voltage_cycle

            y_min = min(current_cycle.min(), y_min)
            y_max = max(current_cycle.max(), y_max)
            x_min = min(voltage_cycle.min(), x_min)
            x_max = max(voltage_cycle.max(), x_max)

    return norm_cur_voltage, x_min, x_max, y_min, y_max


def get_avg_voltage(data, selected_cycles_list, selected_channels_list):
    # calculate average voltage
    x_min, x_max = min(selected_cycles_list) , max(selected_cycles_list)
    y_min, y_max = sys.maxsize, -sys.maxsize - 1
    avg_voltages = {}
    for channel_number in selected_channels_list:
        avg_voltages[channel_number] = {}
        for cycle_number in selected_cycles_list:
            avg_voltages[channel_number][cycle_number] = 0
            cycle_data = data[data['Cycle'] == cycle_number]
            current = cycle_data.loc[:, "Ch.{}-I (uA)".format(channel_number)].apply(lambda x: x / 1000).values
            sum_current = sum(current)
            avg_volt_from_data = cycle_data.loc[:, "Vavg (V)".format(channel_number)].values
            voltage_into_current = np.sum(np.multiply(current, avg_volt_from_data))
            avg_voltages[channel_number][cycle_number] = voltage_into_current / sum_current

            y_min = min(avg_voltages[channel_number][cycle_number], y_min)
            y_max = max(avg_voltages[channel_number][cycle_number], y_max)

    return avg_voltages, x_min, x_max, y_min, y_max


def set_plot_limits(ax, x_min, x_max, y_min, y_max, x_left, x_right, y_bottom, y_top):
    # if none use calculated limits.
    y_min = y_bottom if y_min is None else y_min
    y_max = y_top if y_max is None else y_max
    x_min = x_left if x_min is None else x_min
    x_max = x_right if x_max is None else x_max

    # margin
    x_range = x_max - x_min
    y_range = y_max - y_min
    x_max = x_max + (x_range * 0.05)
    x_min = x_min - (x_range * 0.05)
    y_max = y_max + (y_range * 0.05)
    y_min = y_min - (y_range * 0.05)

    # assign limits
    ax.set_ylim(bottom=y_min, top=y_max)  # set the y-axis limits
    ax.set_xlim(left=x_min, right=x_max)  # set the x-axis limits


def set_subplot_tile(ax, show_tile, x_y_label_checked, x_y_data, channel_number, config):

    if show_tile:
        if x_y_label_checked:
            x = x_y_data.loc[channel_number, 'x']
            y = x_y_data.loc[channel_number, 'y']
            ax.set_title('{}: {}, {}'.format(channel_number, np.round(x, 2), np.round(y, 2)), **config)
        else:
            ax.set_title('Channel {}'.format(channel_number), **config)


def set_labels(ax, x_label, y_label, plot_one_channel, channel_number, config):
    # show axis only on the left and bottom
    if plot_one_channel:
        ax.set_xlabel(x_label, **config)
        ax.set_ylabel(y_label, **config)
    # there are more than one plot
    # y axis label on channel 3 plot
    elif channel_number == 4:
        ax.set_ylabel(y_label, **config)
        ax.set_xticklabels([])
    #  x axis label on channel
    elif channel_number == 32:
        ax.set_xlabel(x_label, **config)
        ax.set_yticklabels([])
    # only y axis label
    elif channel_number in range(0, 8):
        ax.set_xticklabels([])
    # only show x axis label
    elif channel_number in [16, 24, 32, 40, 48, 56, 64]:
        ax.set_yticklabels([])
    # everything else no label
    elif channel_number != 8:
        ax.set_yticklabels([])
        ax.set_xticklabels([])


def get_data_in_voltage_range(data, voltage_range):
    min_voltage, max_voltage = voltage_range
    voltage_column_name = 'Vavg (V)'
    data = data.loc[data.loc[:, voltage_column_name] >= min_voltage, :]
    data = data.loc[data.loc[:, voltage_column_name] <= max_voltage, :]
    return data
