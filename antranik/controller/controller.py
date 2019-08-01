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

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.temp = None
        self.default_config = {
                "tick_params": {
                    "axis": "both",
                    "which": "major",
                    "labelsize": 20,
                    "direction": "in",
                    "top": True,
                    "right": True
                },
                "axis_label": {
                    "fontsize": 30
                },
                "plot": {
                    "linewidth": 2
                },
                "scatter": {
                    "marker": "o",
                    "s": 4,
                    "c": "b"
                },
                "tick_locator": {},
                "figure": {
                    "figsize": [20, 15]
                },
                "subplot_title": {
                    "fontsize": 10,
                    "position": [0.5, 0.8]
                },
                "axis_label_name": {"x": "Re(Z)/Ohm", "y": "-Im(Z)/Ohm"},
                "subplot_spacing": {"hspace": 0.05, "wspace": 0.05}
            }

    def plot(self, missing, freq_range_info, freq_range_point_info, selected_channel, limits):
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
        config = self.default_config

        # get data in frequency range.
        data = get_data_in_frequency_range(data, freq_range)

        # change scale x-axis user input to int
        x_limit, y_limit = limits
        x_min = scale_user_input_to_float(x_limit[0])
        x_max = scale_user_input_to_float(x_limit[1])
        # change scale y-axis user input to int
        y_min = scale_user_input_to_float(y_limit[0])
        y_max = scale_user_input_to_float(y_limit[1])

        # circuit info
        randles = Randles(initial_guess=[.01, .005, .1, .001, 200])
        randlesCPE = Randles(initial_guess=[.01, .005, .1, .9, .001, 200], CPE=True)
        customCircuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200],
                                      circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-W_1')

        # validate limits
        if not (self.validate_limit(x_min, x_max) and self.validate_limit(y_min, y_max)):
            return

        if selected_channel == "all":
            fig, self.axs = plt.subplots(8, 8, **config["figure"])
        else:
            fig, self.axs = plt.subplots(1, 1, **config["figure"])

        # if is_one_channel:
            # channel_data = data[data['channel'] == int(selected_channel)]
            # frequencies = data["freq/Hz"].values
            # Z = data["Re(Z)/Ohm"].values + 1j*data["-Im(Z)/Ohm"].values
            #
            # # # keep only the impedance data in the first quandrant
            # # frequencies = frequencies[np.imag(Z) < 0]
            # # Z = Z[np.imag(Z) < 0]
            # randles.fit(frequencies, Z)
            # randlesCPE.fit(frequencies, Z)
            # customCircuit.fit(frequencies, Z)
            # from impedance.plotting import plot_nyquist
            #
            # f_pred = np.logspace(5, -2)
            #
            # randles_fit = randles.predict(f_pred)
            # randlesCPE_fit = randlesCPE.predict(f_pred)
            # customCircuit_fit = customCircuit.predict(f_pred)
            #
            # fig, ax = plt.subplots(figsize=(5, 5))
            #
            # plot_nyquist(ax, frequencies, Z)
            # plot_nyquist(ax, f_pred, randles_fit, fmt='-')
            # plot_nyquist(ax, f_pred, randlesCPE_fit, fmt='-')
            # plot_nyquist(ax, f_pred, customCircuit_fit, fmt='-')
            #
            # plt.show()

        for channel_index in range(64):

            channel_number = channel_index + 1

            if not is_one_channel:
                ax = self.axs[channel_index % 8][int(channel_index / 8)]
            elif channel_number == int(selected_channel):
                ax = self.axs
            else:
                continue

            if channel_number in missing:
                continue
            channel_data = data[data['channel'] == channel_number]
            ax.scatter(channel_data["Re(Z)/Ohm"], channel_data["-Im(Z)/Ohm"], **config["scatter"])
            # scatterBuilder(t)
            ax.ticklabel_format(style="sci", scilimits=(0, 4))
            # plt.ticklabel_format(useOffset=False)
            ax.tick_params(labelsize=10)
            ax.set_picker(True)
            # ax.set_ylim(bottom=0, top=2500000)  # set the y-axis limits
            # ax.set_xlim(left=0, right=500000)  # set the x-axis limits
            set_labels(ax, config["axis_label_name"]["x"], config["axis_label_name"]["y"], channel_number, {})
        if is_one_channel:
            zp = ZoomPan()
            zp.zoom_factory(self.axs, base_scale=1.2)
            zp.pan_factory(self.axs)
        else:
            fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.subplots_adjust(**config["subplot_spacing"])
        message = "Figure {}: {}".format(
            plt.gcf().number,
            "plot title")
        self.task_bar_message.emit("green", message)
        fig.suptitle(message, fontsize=25)
        import matplotlib
        print(matplotlib.__version__)
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
        if min > max:
            self.task_bar_message.emit("red", "Maximum limit has to be greater than minimum limit")
            return False
        return True

    def validate_selected_channel(self, selected_channel, missing):
        if selected_channel != "all":
            if int(selected_channel) in missing:
                return False
        return True

    def onclick(self, event):
        if event.dblclick:
            for row in range(8):
                for col in range(8):
                    if event.inaxes == self.axs[row][col]:
                        print(row, col)

                        data = self._model.data_data
                        fig, axs = plt.subplots(1, 1)
                        channel_number = (col)* 8 + (row + 1)
                        channel_data = data[data['channel'] == channel_number]
                        axs.scatter(channel_data["Re(Z)/Ohm"], channel_data["-Im(Z)/Ohm"])
                        zp = ZoomPan()
                        zp.zoom_factory(axs, base_scale=1.2)
                        zp.pan_factory(axs)
                        fig.suptitle("channel {}".format(channel_number))
                        plt.show()
    def onpick(self, event):
        print(event.mouseevent.button)

        for row in range(8):
            for col in range(8):
                if event.artist == self.axs[row][col]:
                    print(row, col)

                    data = self._model.data_data
                    fig, axs = plt.subplots(1, 1)
                    channel_number = (col)* 8 + (row + 1)
                    channel_data = data[data['channel'] == channel_number]
                    axs.scatter(channel_data["Re(Z)/Ohm"], channel_data["-Im(Z)/Ohm"])
                    zp = ZoomPan()
                    zp.zoom_factory(axs, base_scale=1.2)
                    zp.pan_factory(axs)
                    fig.suptitle("channel {}".format(channel_number))
                    plt.show()



class scatterBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()



