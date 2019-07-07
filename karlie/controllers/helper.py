import pandas as pd
import re
import numpy as np


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


def get_medusa_columns():
    columns = {"Cycle", "Time(h)", "VSet (V)", "Vavg (V)"}
    for channel_number in range(1, 65):
        columns.add("Ch.{}-I (uA)".format(channel_number))
    return columns


def get_mass_columns():
    columns = {"Cycle", "Name"}
    for channel_number in range(1, 65):
        columns.add("Channel {}".format(channel_number))
    return columns


def get_charges(data, selected_channels_list):
    # calculate charges
    charges = {}
    for channel_number in selected_channels_list:
        charges[channel_number] = {}
        accumulated_charge = 0
        current = data.loc[:, "Ch.{}-I (uA)".format(channel_number)].apply(lambda x: x / 1000).values
        time_h = data.loc[:, "Time(h)"].values
        voltages = data.loc[:, "Vavg (V)"].values
        cycle = data.loc[:, "Cycle"].values
        for index in range(len(time_h) - 1):
            # formula to calculate charges
            cycle_number = cycle[index]
            if cycle_number not in charges[channel_number]:
                charges[channel_number][cycle_number] = {'charge': [], 'voltage': []}
            avg_charge = (current[index] + current[index + 1]) / 2
            time_diff = time_h[index + 1] - time_h[index]
            charge = avg_charge * time_diff
            accumulated_charge += charge
            voltage = voltages[index]

            charges[channel_number][cycle_number]['charge'].append(accumulated_charge)
            charges[channel_number][cycle_number]['voltage'].append(voltage)

    return charges


def get_capacity(data, selected_cycles_list, selected_channels_list):
    # calculate charges
    charges = {}
    for channel_number in selected_channels_list:
        charges[channel_number] = {}
        for cycle_number in selected_cycles_list:
            charges[channel_number][cycle_number] = 0
            cycle_data = data[data['Cycle'] == cycle_number]
            current = cycle_data.loc[:, "Ch.{}-I (uA)".format(channel_number)].values
            time_h = cycle_data.loc[:, "Time(h)".format(channel_number)].values
            charge = 0
            for index in range(len(time_h) - 2):
                # formula to calculate charges
                avg_charge = (current[index] + current[index + 1]) / 2
                time_diff = time_h[index + 1] - time_h[index]
                charge += avg_charge * time_diff
            charges[channel_number][cycle_number] = charge

    return charges

def get_avg_voltage(data, selected_cycles_list, selected_channels_list):
    # calculate average voltage
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

    return avg_voltages


def set_plot_limits(ax, x_min, x_max, y_min, y_max, y_bottom, y_top, x_left, x_right):
    # get default limits
    # y_bottom, y_top = ax.get_ylim()
    # x_left, x_right = ax.get_xlim()
    y_min = y_bottom if y_min is None else y_min
    y_max = y_top if y_max is None else y_max
    x_min = x_left if x_min is None else x_min
    x_max = x_right if x_max is None else x_max

    # assign limits
    ax.set_ylim(bottom=y_min, top=y_max)  # set the y-axis limits
    ax.set_xlim(left=x_min, right=x_max)  # set the x-axis limits


def set_subplot_tile(ax, show_tile, x_y_label_checked, x_y_data, channel_number, config):

    if show_tile:
        if x_y_label_checked:
            x = x_y_data.loc[channel_number, 'x']
            y = x_y_data.loc[channel_number, 'y']
            ax.set_title('{}: {}, {}'.format(channel_number, np.round(x,2), np.round(y, 2)), **config)
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
    data = data.loc[data.loc[:, 'Vavg (V)'] >= min_voltage, :]
    data = data.loc[data.loc[:, 'Vavg (V)'] <= max_voltage, :]
    return data