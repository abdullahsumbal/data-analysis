import re
import math
import matplotlib.colors as mcolors

selected_type_dict = {"Average Voltage": "average_voltage_", "Charge": "charge_"}

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


def calculate(data, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2, selected_operation):

    # if compare is not checked
    if selected_operation is None:
        data["calculated"] = data[selected_type_dict[selected_type_1] + selected_cycle_1]
        print(data[[selected_type_dict[selected_type_1] + selected_cycle_1, "calculated"]])
        return data

    # if compare is checked
    if selected_operation == "Subtract (-)":
        data["calculated"] = data[selected_type_dict[selected_type_1] + selected_cycle_1] - \
                             data[selected_type_dict[selected_type_2] + selected_cycle_2]
    elif selected_operation == "Multiple (*)":
        data["calculated"] = data[selected_type_dict[selected_type_1] + selected_cycle_1] * \
                             data[selected_type_dict[selected_type_2] + selected_cycle_2]

    print(data[[selected_type_dict[selected_type_1] + selected_cycle_1, selected_type_dict[selected_type_2] + selected_cycle_2, "calculated"]])
    return data

def remove_exclude(data, exclude_channels):
    for channel in exclude_channels:
        # Get names of indexes for which column Age has value 30
        indexNames = data[data['channels'] == channel].index

        # Delete these row indexes from dataFrame
        data.drop(indexNames, inplace=True)
    return data


def remove_duplicate(data):
    data = data.groupby(['x', "y"], as_index=False).mean()
    return data


def validate_exclude_channels(channels):
    # if the channels are coming from reading master file.
    # and exclude field is empty, it is read is float nan
    if isinstance(channels, float) and math.isnan(channels):
        return []

    # if no input given then return empty array. used when user
    # does not enter anything in the lineEdit for outlier
    if re.search("^\s*$", channels):
        return []

    if not re.search("^((\s*\d+\s*,{1}\s*)|\s*\d+\s*)+$", channels):
        return None
    else:
        # change from string to list of integers
        channels_list = channels.split(',')
        channels_list = [i.strip() for i in channels_list]
        if '' in channels_list:
            channels_list.remove('')
        channels_list = [int(i) for i in channels_list]
        return channels_list
