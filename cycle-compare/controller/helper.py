import sys

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


def get_mass_columns():
    columns = {"Cycle", "Name"}
    for channel_number in range(1, 65):
        columns.add("Channel {}".format(channel_number))
    return columns