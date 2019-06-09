import pandas as pd
import re


def scale_user_input_to_float(limit):
    return None if limit == "" else float(limit)


def validate_x_y_file(name):
    return [], True


def validate_config_file(name):
    return [], True


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


def get_charges(data, selected_cycles_list, selected_channels_list):
    # calculate charges
    charges = {}

    for channel_number in selected_channels_list:
        charges[channel_number] = {}
        for cycle_number in selected_cycles_list:
            charges[channel_number][cycle_number] = []
            cycle_data = data[data['Cycle'] == cycle_number]
            # print(cycle_data)
            current = cycle_data.loc[:, "Ch.{}-I (uA)".format(channel_number)].values
            time_h = cycle_data.loc[:, "Time(h)".format(channel_number)].values
            for index in range(len(time_h) - 1):
                # formula to calculate charges
                avg_charge = (current[index] + current[index + 1]) / 2
                time_diff = time_h[index + 1] - time_h[index]
                charge = avg_charge * time_diff
                charges[channel_number][cycle_number].append(charge)

    return charges


def get_avg_voltage(data, selected_cycles_list, selected_channels_list):
    # calculate average voltage
    avg_voltages = {}

    for channel_number in selected_channels_list:
        avg_voltages[channel_number] = {}
        for cycle_number in selected_cycles_list:
            avg_voltages[channel_number][cycle_number] = []
            cycle_data = data[data['Cycle'] == cycle_number]
            # print(cycle_data)
            current = cycle_data.loc[:, "Ch.{}-I (uA)".format(channel_number)].values
            sum_current = sum(current)
            avg_volt_from_data = cycle_data.loc[:, "Vavg (V)".format(channel_number)].values
            for index in range(len(current)):
                # formula to calculate charges
                avg_voltage = (current[index] * avg_volt_from_data[index]) / sum_current
                avg_voltages[channel_number][cycle_number].append(avg_voltage)

    return avg_voltages