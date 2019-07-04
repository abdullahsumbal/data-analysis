import re
import math
import pandas as pd


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