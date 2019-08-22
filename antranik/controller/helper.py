from os import path
import re

import numpy as np
from impedance.circuits import Randles
from threading import Thread
import functools

def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print ('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

def get_fitting_data(data):

    randles = Randles(initial_guess=[.01, .005, .1, .001, 200])
    columns = ['freq/Hz', 'Re(Z)/Ohm', '-Im(Z)/Ohm']
    # data = pd.read_csv("test/test_01_1_C01.txt", sep="\t", usecols=columns)

    frequencies = data["freq/Hz"].values
    Z = data['Re(Z)/Ohm'].values - 1j * data['-Im(Z)/Ohm'].values

    instance_of_impedance_lib = randles.fit(frequencies, Z)
    print(instance_of_impedance_lib)
    param_names = instance_of_impedance_lib.get_param_names()
    param_values = instance_of_impedance_lib.parameters_
    param_error = instance_of_impedance_lib.conf_

    # f_pred = np.logspace(5, -2)
    randles_fit = randles.predict(frequencies)

    return randles_fit, param_names, param_values, param_error


def get_file_number(file_path):
    name = path.basename(file_path)
    file_number = re.findall("_\d{1,2}", name)
    if len(file_number) == 0:
        raise Exception('Error: Incorrect file format. Should be <name of file>_<channel number>* where * anything')
    return file_number[0][1:]

def get_sorted_files(list_of_files):
    sorted(list_of_files, key=lambda file_path: get_file_number(file_path))
    return list_of_files

def set_labels(ax, x_label, y_label, is_one_channel, channel_number, config):
    # show axis only on the left and bottom
    if is_one_channel:
        ax.set_xlabel(x_label, **config)
        ax.set_ylabel(y_label, **config)

    # there are more than one plot
    # y axis label on channel 3 plot
    if channel_number == 4:
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


def get_data_in_frequency_range(data, freq_range):
    min_freq, max_freq = freq_range
    freq_column_name = 'freq/Hz'
    data = data.loc[data.loc[:, freq_column_name] >= min_freq, :]
    data = data.loc[data.loc[:, freq_column_name] <= max_freq, :]
    return data


def scale_user_input_to_float(limit):
    return None if limit == "" else float(limit)


class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print (event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion


def set_plot_limits(ax, x_min, x_max, y_min, y_max):
    # get the default limits
    x_left = ax.get_xlim()[0]
    x_right = ax.get_xlim()[1]
    y_bottom = ax.get_ylim()[0]
    y_top = ax.get_ylim()[1]
    # if none use calculated limits.
    y_min = y_bottom if y_min == "" else float(y_max)
    y_max = y_top if y_max == "" else float(y_max)
    x_min = x_left if x_min == "" else float(x_min)
    x_max = x_right if x_max == "" else float(x_max)

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


def get_selected_channels(missing):
    selected_channels = []
    for i in range(1, 65):
        if i in missing:
            continue
        selected_channels.append(i)
    return selected_channels

default_config_single = {
    "tick_params": {
        "axis": "both",
        "which": "major",
        "labelsize": 20,
        "direction": "in",
        "left": True,
        "bottom": True
    },
    "axis_label": {
        "fontsize": 30
    },
    "plot": {
        "c": "orange",
        "linewidth": 2
    },
    "scatter": {
        "marker": "o",
        "s": 4,
        "c": "b"
    },
    "figure": {
        "figsize": [20, 15]
    },
    "subplot_title": {
        "fontsize": 10,
        "position": [0.5, 0.8]
    },
    "axis_label_name": {"x": "Re(Z)/Ohm", "y": "-Im(Z)/Ohm"}
}

default_config_multiple = {
    "tick_params": {
        "axis": "both",
        "which": "major",
        "labelsize": 20,
        "direction": "in",
        "top": True,
        "right": True,
        "labelleft": False,
        "labelbottom": False
    },
    "axis_label": {
        "fontsize": 30
    },
    "plot": {
        "linewidth": 2,
        "c": "orange"
    },
    "scatter": {
        "marker": "o",
        "s": 4,
        "c": "b"
    },
    "figure": {
        "figsize": [20, 15]
    },
    "subplot_title": {
        "fontsize": 10,
        "position": [0.5, 0.8]
    },
    "axis_label_name": {"x": "Re(Z)/Ohm", "y": "-Im(Z)/Ohm"}
}
