from PyQt5.QtCore import QObject, pyqtSignal
from controller.helper import *
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from os import path

class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)
    enabled_plot_button = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.temp = None
        self.fitting_params_dict = {}

    def plot(self, missing, freq_range_info, freq_range_point_info, selected_channel, limits, timeout, apply_fitting, model, guess, show_title):
        data = self._model.data_data

        # validate channel
        if not self.validate_selected_channel(selected_channel, missing):
            return

        is_one_channel = not (selected_channel == "all")

        # selects validate frequency
        valid, freq_range = self.validate_freq_range(freq_range_info, freq_range_point_info)
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
            self.plot_one(data, int(selected_channel), limits, timeout, apply_fitting, model, guess, show_title, config)
        else:
            self.plot_multiple(data, missing, limits, timeout, apply_fitting, model, guess, show_title, config)
        return 

    def plot_multiple(self, data, missing, limits, timeout_time, apply_fitting, model, guess, show_title, config):

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

        # get fitting info if guess_model file is loaded
        guess_model_data = self._model.guess_model_data

        for channel_index in range(64):

            # get channel data
            channel_number = channel_index + 1
            channel_data = data[data['channel'] == channel_number]

            # skip missing channels
            if channel_number in missing:
                continue

            # get fitting
            if apply_fitting:
                get_fitting_data_timeout = timeout(timeout=timeout_time)(get_fitting_data)
                try:
                    # loaded file model and guess values take priority
                    if guess_model_data is not None:
                        model = guess_model_data.loc[channel_number, 'model']
                        guess = list(map(float, guess_model_data.loc[channel_number, 'guess'].split(",")))
                    fitting, self.param_names, self.param_values, self.param_errors = get_fitting_data_timeout(channel_data, model, guess)
                    print("processed:", channel_number)
                except Exception as e:
                    print(e)
                    belated_fitting.append(channel_number)
                    self.task_bar_message.emit("red", "Error: fitting timed out. Increase fitting timeout or change fitting params. {}".format(e))

            self.task_bar_message.emit("blue", "Procesing Channel {}".format(channel_number))

            # get subplot
            ax = axs[channel_index % 8][int(channel_index / 8)]

            # plots and scatter
            ax.scatter(channel_data["Re(Z)/Ohm"].values, channel_data["-Im(Z)/Ohm"].values, **config["scatter"])
            if channel_number not in belated_fitting and apply_fitting:
                ax.plot(fitting.real, fitting.imag * -1, **config["plot"])

            # styling the plot
            ax.set_picker(True)

            # remove tick labels.
            # ax.set_xticklabels([])
            # ax.set_yticklabels([])

            # set axes label
            if channel_number == 32:
                ax.set_xlabel(config["axis_label_name"]["x"], **config["axis_label"])

            if channel_number == 4:
                ax.set_ylabel(config["axis_label_name"]["y"], **config["axis_label"])

            # ticks
            ax.tick_params(**config["tick_params"])
            # set set limits
            set_plot_limits(ax, x_min, x_max, y_min, y_max)
            ax.ticklabel_format(style='plain')

            if show_title:
                ax.set_title('Channel {}'.format(channel_number), **config["subplot_title"])

        # setup picker. double clicking on the subplot will open
        # a plot with one channel
        fig.canvas.mpl_connect('button_press_event', lambda event: self.onclick(event, axs, self._model.data_data, limits, timeout_time, model, guess, show_title, apply_fitting))

        # plot title and message box
        message = "Figure {}: {}".format(
            plt.gcf().number,  model if apply_fitting else "No fitting")
        self.task_bar_message.emit("green", message)
        fig.suptitle(message, fontsize=25)
        plt.show()
        plt.close()
        self.enabled_plot_button.emit()

    def plot_one(self, data, channel_number, limits, timeout_time, apply_fitting, model, guess, show_title, config):

        # get channel data
        channel_data = data[data['channel'] == channel_number]

        # get fitting
        if apply_fitting:
            get_fitting_data_timeout = timeout(timeout=timeout_time)(get_fitting_data)
            try:

                # get fitting info if guess_model file is loaded
                guess_model_data = self._model.guess_model_data
                if guess_model_data is not None:
                    model = guess_model_data.loc[channel_number, 'model']
                    guess = list(map(float, guess_model_data.loc[channel_number, 'guess'].split(",")))

                fitting, self.param_names, self.param_values, self.param_errors = get_fitting_data_timeout(channel_data, model, guess)
            except Exception as e:
                self.enabled_plot_button.emit()
                self.task_bar_message.emit("red", "Error: fitting timed out. Increase fitting timeout or change fitting params. {}".format(e))
                return

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

        if show_title:
            ax.set_title('Channel {}'.format(channel_number), **config["subplot_title"])

        # plot title and message box
        message = "Figure {}: {}".format(
            plt.gcf().number, model if apply_fitting else "No fitting")
        self.task_bar_message.emit("green", message)
        fig.suptitle(message, fontsize=25)
        plt.show()
        plt.close()
        self.enabled_plot_button.emit()

    def export(self, file_path, missing, freq_range_info, freq_range_point_info, selected_channel, limits, timeout_time, apply_fitting, model, guess):
        data = self._model.data_data

        # validate channel
        if not self.validate_selected_channel(selected_channel, missing):
            return

        is_one_channel = not (selected_channel == "all")

        # selects validate frequency
        valid, freq_range = self.validate_freq_range(freq_range_info, freq_range_point_info)
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

        # track fittings which were taking too long
        belated_fitting = []

        # x_y file data
        x_y_data = self._model.x_y_data

        # get fitting info if guess_model file is loaded
        guess_model_data = self._model.guess_model_data

        area_thickness_data = self._model.area_thickness_data

        # first time for csv writer
        first_time = True

        for channel_index in range(64):

            # get channel data
            channel_number = channel_index + 1
            channel_data = data[data['channel'] == channel_number]

            # skip missing channels
            if channel_number in missing:
                continue
            # x and y data for channel
            x = x_y_data.loc[channel_number, 'x']
            y = x_y_data.loc[channel_number, 'y']
            # area and thickness for channel
            area = 1
            thickness = 1
            if area_thickness_data is not None:
                area = area_thickness_data.loc[channel_number, 'area']
                thickness = area_thickness_data.loc[channel_number, 'thickness']

            # get fitting
            if apply_fitting:
                get_fitting_data_timeout = timeout(timeout=timeout_time)(get_fitting_data)
                try:
                    if guess_model_data is not None:
                        model = guess_model_data.loc[channel_number, 'model']
                        guess = list(map(float, guess_model_data.loc[channel_number, 'guess'].split(",")))

                    fitting, param_names, param_values, param_errors = get_fitting_data_timeout(channel_data, model, guess)
                    print("processed:", channel_number)

                    # write and append to file
                    if first_time:
                        with open(file_path, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(["channels", "x", "y", *param_names,
                                             *list(map(lambda param: param + "_error", param_names)), "some_calculation"]
                                            )
                            some_calculation, some_calculation_plus, some_calculation_plus_neg = get_some_calculation(
                                param_names, param_values, param_errors, area, thickness)
                            writer.writerow([channel_number, x, y, *param_values, *param_errors, some_calculation])
                            first_time = not first_time
                    else:
                        with open(file_path, 'a', newline='') as f:
                            writer = csv.writer(f)
                            some_calculation, some_calculation_plus, some_calculation_plus_neg = get_some_calculation(
                                param_names, param_values, param_errors, area, thickness)
                            writer.writerow([channel_number, x, y, *param_values, *param_errors, some_calculation])
                except Exception as e:
                    belated_fitting.append(channel_number)
                    print(e)
                    self.task_bar_message.emit("red", "Error: fitting timed out. Increase fitting timeout or change fitting params. {}".format(e))

            self.task_bar_message.emit("blue", "Procesing Channel {}".format(channel_number))


        # plot title and message box
        message = "Exporting successful to file {}".format(path.basename(file_path))
        self.task_bar_message.emit("green", message)
        self.enabled_plot_button.emit()




    def validate_file_folder(self, file_name, file_type, missing=[]):
        # update model
        valid = True
        emit_message = True
        if file_type == "data":
            data, valid, emit_message = self.validate_data_file(file_name, file_type, missing)
        elif file_type == "x_y":
            data, valid = self.validate_other_files(file_name, file_type, {"x", "y", "channel"}, missing)
        elif file_type == "guess_model":
            data, valid = self.validate_other_files(file_name, file_type, {"channel", "model", "guess"}, missing)
        elif file_type == "area_thickness":
            data, valid = self.validate_other_files(file_name, file_type, {"channel", "area", "thickness"}, missing)
        elif file_type == "config":
            data, valid = self.validate_config_file(file_name, file_type)
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
            self.task_bar_message.emit("red", message)
            return [], not valid, emit_message

    def validate_config_file(self, name, file_type):
        try:
            with open(name) as json_file:
                data = json.load(json_file)
                return data, True
        except Exception as error:
            message = "Error: Invalidate {} file format. {}".format(file_type, error)
            self.task_bar_message.emit("red", message)
            return [], False

    def validate_other_files(self, name, file_type, columns, missing_channels):
        try:
            data = pd.read_csv(name)
            diff = columns.difference(set(data.columns.values))
            if bool(diff):
                message = "Error: Invalidate {} file format. Heading not found: {}".format(
                    file_type,
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            else:
                channel_count = data['channel'].count()
                selected_channels = get_selected_channels(missing_channels)
                # channel count should be less than 64 and greater (64 - missing channels)
                if channel_count < len(selected_channels) or channel_count > 64:
                    message = "Error: Invalidate {} file format. Channels should be between {} and 64".format(
                        file_type,
                        len(selected_channels))
                    self.task_bar_message.emit("red", message)
                    return [], False
                elif not pd.Series(selected_channels).isin(data['channel'].values).all():
                    message = "Error: Invalidate {} file format. The following channels should be in the file: {}".format(
                        file_type,
                        ",".join(map(str, selected_channels)))
                    self.task_bar_message.emit("red", message)
                    return [], False
                elif not all(isinstance(x, np.int64) for x in data["channel"].values):
                    message = "Error: Invalidate {} file format. Channel should be integers".format(
                        file_type)
                    self.task_bar_message.emit("red", message)
                    return [], False
                data = data.set_index('channel')
                return data, True


        except Exception as error:
            message = "Error: Invalidate {} file format. {}".format(file_type, error)
            self.task_bar_message.emit("red", message)
            return [], False

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

    def onclick(self, event, axs, data, limits, timeout_time, model, guess,  show_title, apply_fitting):
        #  {None, MouseButton.LEFT, MouseButton.MIDDLE, MouseButton.RIGHT, 'up', 'down'}
        # 3 means right click
        if event.button == 3:
            print("detected right click")
            # right click will show/hide the tick labels.
            ax = event.inaxes
            show_labels = ax.get_xticklabels() == []
            ax.tick_params(labelleft=show_labels, labelbottom=show_labels)
            config = self._model.config_data
            event.canvas.draw()



        if event.button == 1:
            print("detected left click")
            for row in range(8):
                for col in range(8):
                    if event.inaxes == axs[row][col]:
                        channel_number = (col) * 8 + (row + 1)

                        # get config
                        config = self._model.config_data
                        if config is None:
                            config = default_config_single
                        self.plot_one(data, channel_number, limits, timeout_time, apply_fitting, model, guess, show_title, config)
