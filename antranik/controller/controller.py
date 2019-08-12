from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from controller.helper import *
import pandas as pd
import glob
import matplotlib.pyplot as plt
from impedance.circuits import Randles, CustomCircuit
import matplotlib
matplotlib.use("TkAgg")
import numpy as np

class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)
    enabled_plot_button = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.temp = None

    def plot(self, missing, freq_range_info, freq_range_point_info, selected_channel, limits, apply_fitting):
        data = self._model.data_data

        # validate channel
        if not self.validate_selected_channel(selected_channel, missing):
            return

        is_one_channel = not (selected_channel == "all")

        # selects validate frequency
        valid, freq_range = self.validate_freq_range(freq_range_info, freq_range_point_info)
        print(freq_range)
        if not valid:
            return

        # get config
        config = self._model.config_data
        if config is None:
            if is_one_channel:
                config = default_config_single
            else:
                config = default_config_multiple

        # get data in frequency range.
        data = get_data_in_frequency_range(data, freq_range)

        x_limit, y_limit = limits
        x_min = x_limit[0]
        x_max = x_limit[1]
        y_min = y_limit[0]
        y_max = y_limit[1]

        # validate limits
        if not (self.validate_limit(x_min, x_max) and self.validate_limit(y_min, y_max)):
            return

        if is_one_channel:
            self.plot_one(data, int(selected_channel), limits, apply_fitting, config)
        else:
            self.plot_multiple(data, missing, limits, apply_fitting, config)
        return 

    def plot_multiple(self, data, missing, limits, apply_fitting,  config):

        # get fitting
        # fitting = get_fitting_data(data)
        # scale given by user
        x_limit, y_limit = limits
        x_min = x_limit[0]
        x_max = x_limit[1]
        y_min = y_limit[0]
        y_max = y_limit[1]

        # plot all 64 but skip misisng
        fig, axs = plt.subplots(8, 8, **config["figure"])

        # track fittings which were taking too long
        belated_fitting = []

        for channel_index in range(64):

            # get channel data
            channel_number = channel_index + 1
            channel_data = data[data['channel'] == channel_number]

            # get fitting
            if apply_fitting:
                try:
                    fitting = get_fitting_data(channel_data)
                except Exception:
                    belated_fitting.append(channel_number)

            print(channel_number)
            self.task_bar_message.emit("blue", "Procesing Channel {}".format(channel_number))

            # skip missing channels
            if channel_number in missing:
                continue
            # get subplot
            ax = axs[channel_index % 8][int(channel_index / 8)]

            # plots and scatter
            ax.scatter(channel_data["Re(Z)/Ohm"], channel_data["-Im(Z)/Ohm"], **config["scatter"])
            if channel_number not in belated_fitting and apply_fitting:
                ax.plot(fitting.real, fitting.imag * -1, **config["plot"])

            # styling the plot
            ax.set_picker(True)

            # remove tick labels.
            ax.set_xticklabels([])
            ax.set_yticklabels([])

            # set axes label
            if channel_number == 32:
                ax.set_xlabel(config["axis_label_name"]["x"], **config["axis_label"])

            if channel_number == 4:
                ax.set_ylabel(config["axis_label_name"]["y"], **config["axis_label"])

            # ticks
            ax.tick_params(**config["tick_params"])
            # set set limits
            set_plot_limits(ax, x_min, x_max, y_min, y_max)

        # setup picker. double clicking on the subplot will open
        # a plot with one channel
        fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event, axs, self._model.data_data))

        # plot title and message box
        message = "Figure {}: {}".format(
            plt.gcf().number,
            "plot title")
        self.task_bar_message.emit("green", message)
        fig.suptitle(message, fontsize=25)
        self.enabled_plot_button.emit()
        plt.show()

    def plot_one(self, data, channel_number, limits, apply_fitting, config):

        # get channel data
        channel_data = data[data['channel'] == channel_number]

        # get fitting
        from time import gmtime, strftime
        # print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        if apply_fitting:
            try:
                fitting = get_fitting_data(channel_data)
            except Exception:
                self.enabled_plot_button.emit()
                return
        # print(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        # scale given by user
        x_limit, y_limit = limits
        x_min = x_limit[0]
        x_max = x_limit[1]
        y_min = y_limit[0]
        y_max = y_limit[1]

        # subplot which is only one
        fig, ax = plt.subplots(1, 1, **config["figure"])

        # plot
        ax.scatter(channel_data["Re(Z)/Ohm"], channel_data["-Im(Z)/Ohm"], **config["scatter"])
        if apply_fitting:
            ax.plot(fitting.real, fitting.imag * -1, **config["plot"])
        ax.tick_params(labelsize=10)
        # set axes label
        ax.set_xlabel(config["axis_label_name"]["x"], **config["axis_label"])
        ax.set_ylabel(config["axis_label_name"]["y"], **config["axis_label"])

        # set set limits
        set_plot_limits(ax, x_min, x_max, y_min, y_max)

        # ticks
        ax.tick_params(**config["tick_params"])

        # cool zoom
        zp = ZoomPan()
        zp.zoom_factory(ax, base_scale=1.2)
        zp.pan_factory(ax)

        # plot title and message box
        message = "Figure {}: {}".format(
            plt.gcf().number,
            "plot title")
        self.task_bar_message.emit("green", message)
        fig.suptitle(message, fontsize=25)
        self.enabled_plot_button.emit()
        plt.show()

    def validate_file_folder(self, file_name, file_type, missing=[]):
        # update model
        valid = True
        emit_message = True
        if file_type == "data":
            data, valid, emit_message = self.validate_data_file(file_name, file_type, missing)
        # update model
        if valid:
            self._model.file_name = (file_name, data, file_type, emit_message)

    def validate_data_file(self, file_name, file_type, missing):
        columns = ['freq/Hz', 'Re(Z)/Ohm', '-Im(Z)/Ohm']
        emit_message = True
        valid = True
        try:
            # get files
            list_of_files = glob.glob(file_name + "/*.txt")
            # make sure there is something in the files
            if len(list_of_files) == 0:
                raise Exception('Error: No file found in folder')
                self.task_bar_message.emit("red", message)
                return [], not valid, emit_message
            elif len(missing) + len(list_of_files) != 64:
                message = "Error: Total channels(files) found: {} | Total given missing channel : {}. Please give {} mssing channels".format(
                    len(list_of_files), len(missing), 64 - len(list_of_files))
                self.task_bar_message.emit("red", message)
                return [], not valid, emit_message

            data = None
            sort_files = get_sorted_files(list_of_files)
            file_index = 0
            # read files and append data
            # print(missing)
            # print(sort_files)
            for channel_number in range(1, 65):
                # remove missing channel
                if channel_number in missing:
                    continue
                file = sort_files[file_index]
                if data is None:
                    data = pd.read_csv(file, sep="\t", usecols=columns)
                    data["channel"] = channel_number
                else:
                    channel_data = pd.read_csv(file, sep="\t", usecols=columns)
                    channel_data["channel"] = channel_number
                    data = data.append(channel_data)
                file_index += 1

            # if there are less than 10 file in folder, show in orange
            if len(list_of_files) < 10:
                message = "Warning: {} files loaded successfully. Total files found: {}".format(file_type, len(list_of_files))
                self.task_bar_message.emit("orange", message)
                return data, valid, False
            return data, valid, emit_message
        except Exception as error:
            message = "Error: Invalidate {} folder. {}".format(file_type, error)
            print(message)
            self.task_bar_message.emit("red", message)
            return [], not valid, emit_message

    def get_freq_range_for_plotting(self, freq_range_info):
        if freq_range_info["default"] == False:
            return string_to_range_frequency(freq_range_info["range"])
        else:
            return self.get_frequency_range_from_data()[:2]

    def get_freq_point_range_for_plotting(self, freq_range_info):
        if freq_range_info["default"] == False:
            return string_to_range_frequency(freq_range_info["range"])
        else:
            return 1, self.get_frequency_range_from_data()[2]
    def get_frequency_range_from_data(self):
        data = self._model.data_data
        min_freq = data["freq/Hz"].min()
        max_freq = data["freq/Hz"].max()
        # here i am assuming that all files have same number of freq points
        channel_numbers = data["channel"].unique()
        total_points = data[data["channel"] == channel_numbers[0]].shape[0]
        return min_freq, max_freq, total_points

    def validate_freq_range(self, freq_range_info, freq_point_range_info):
        valid = True
        if freq_range_info["default"] and freq_point_range_info["default"]:
            freq_range = self.get_frequency_range_from_data()[:2]
            return valid, freq_range
        elif not freq_range_info["default"] and freq_point_range_info["default"]:
            return self.is_freq_in_range(freq_range_info["range"]), freq_range_info["range"]
        elif not freq_point_range_info["default"]:
            valid, freq_range = self.frequency_point_to_frequency_value(freq_point_range_info["range"])
        else:
            self.task_bar_message.emit("red", "This can never happend")
        return valid, freq_range

    def is_freq_in_range(self, freq_range):
        data = self._model.data_data
        valid = data["freq/Hz"].between(freq_range[0], freq_range[1], inclusive=True).any()
        if not valid:
            self.task_bar_message.emit("red", "Error: Selected Frequency is not in range.")
        return valid

    def frequency_point_to_frequency_value(self, freq_point_range):
        min_freq_point, max_freq_point = freq_point_range
        data = self._model.data_data
        channel_numbers = data["channel"].unique()
        first_channel_data = data[data["channel"] == channel_numbers[0]]["freq/Hz"]

        if min_freq_point > max_freq_point:
            self.task_bar_message.emit("red", "Error: min Frequency point can not be smaller than max Frequency point")
            return False, []
        if first_channel_data.shape[0] < max_freq_point:
            self.task_bar_message.emit("red", "Error: frequency point {} is out of range. Should be no more than {}".format(max_freq_point, first_channel_data.shape[0]))
            return False, []
        return True, (first_channel_data.iloc[max_freq_point - 1], first_channel_data.iloc[min_freq_point - 1])

    def validate_limit(self, min, max):
        if not (min and max):
            return True
        # min has to be greater than max
        if float(min) > float(max):
            self.task_bar_message.emit("red", "Maximum limit has to be greater than minimum limit")
            return False
        return True

    def validate_selected_channel(self, selected_channel, missing):
        if selected_channel != "all":
            if int(selected_channel) in missing:
                return False
        return True

    def onclick(self, event, axs, data):
        if event.dblclick:
            for row in range(8):
                for col in range(8):
                    if event.inaxes == axs[row][col]:
                        fig, axs = plt.subplots(1, 1)
                        channel_number = (col)* 8 + (row + 1)
                        channel_data = data[data['channel'] == channel_number]
                        axs.scatter(channel_data["Re(Z)/Ohm"], channel_data["-Im(Z)/Ohm"])
                        zp = ZoomPan()
                        zp.zoom_factory(axs, base_scale=1.2)
                        zp.pan_factory(axs)
                        fig.suptitle("channel {}".format(channel_number))
                        plt.show()
    def onpick(self, event, axs, data):
        print(event.mouseevent.button)

        for row in range(8):
            for col in range(8):
                if event.artist == axs[row][col]:
                    print(row, col)

                    fig, axs = plt.subplots(1, 1)
                    channel_number = (col)* 8 + (row + 1)
                    channel_data = data[data['channel'] == channel_number]
                    axs.scatter(channel_data["Re(Z)/Ohm"], channel_data["-Im(Z)/Ohm"])
                    zp = ZoomPan()
                    zp.zoom_factory(axs, base_scale=1.2)
                    zp.pan_factory(axs)
                    fig.suptitle("channel {}".format(channel_number))
                    plt.show()
