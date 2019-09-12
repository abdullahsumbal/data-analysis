from PyQt5.QtCore import QObject, pyqtSignal
import pandas as pd
from controller.helper import *
import matplotlib.pyplot as plt
import json
import numpy as np


class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.matching = []
        self.config = {
                        "tick_params": {
                            "axis": "both",
                            "which": "major",
                            "labelsize": 20,
                            "direction": "in",
                            "top": True,
                            "right": True
                        },
                        "plot": {
                            "linewidth": 2
                        },
                        "subplot_title": {
                            "fontsize": 10,
                            "position": [0.5, 0.8]
                        }
                    }

    def validate_master(self, file_path):
        # read file
        # find out how many files are there
        master_columns = {"medusa", "mass", "x_y", "config"}
        try:
            master_data = pd.read_csv(file_path)
            diff = master_columns.difference(set(master_data.columns.values))
            if bool(diff):
                message = "Error: Invalidate {} file format. Heading not found: {}".format(
                    "master",
                    ",".join(diff))
                raise Exception(message)
            elif master_data.shape != (3, 4):
                message = "Error: Invalidate master file format. There should be 6 files (rows) per 4 heading in master file"
                raise Exception(message)
            elif master_data["medusa"].isnull().values.any():
                message = "Error: Invalidate master file format. There should be 6 medusa files in master file"
                raise Exception(message)

            elif master_data["x_y"].isnull().values.any():
                message = "Error: Invalidate master file format. There should be 6 x_y files in master file"
                raise Exception(message)
        except Exception as e:
            self.task_bar_message.emit("red", str(e))
            return

        all_data = []
        medusa_index = np.where(master_data.columns.values == "medusa")[0][0]
        mass_index = np.where(master_data.columns.values == "mass")[0][0]
        x_y_index = np.where(master_data.columns.values == "x_y")[0][0]
        config_index = np.where(master_data.columns.values == "config")[0][0]
        for index, row in master_data.iterrows():
            all_data.append([])
            medusa_file = row[medusa_index]
            mass_file = row[mass_index]
            x_y_file = row[x_y_index]
            config_file = row[config_index]

            #medusa file validation
            medusa_data, medusa_valid = self.validate_medusa_file(medusa_file, "medusa")
            if not medusa_valid:
                return
            all_data[index].append(medusa_data)


            # mass validation
            if isinstance(mass_file, str):
                mass_data, mass_valid = self.validate_mass_file(mass_file, "config")
                if not mass_valid:
                    return
                all_data[index].append(mass_data)
            else:
                all_data[index].append(None)

            # x_y file validation
            x_y_data, x_y_valid = self.validate_x_y_file(x_y_file, "x_y")
            if not x_y_valid:
                return

            all_data[index].append(x_y_data)

            # config_file validation
            if isinstance(config_file, str):
                config_data, config_valid = self.validate_config_file(config_file, "config")
                if not config_valid:
                    return
                all_data[index].append(config_data)
            else:
                all_data[index].append(None)

        self._model.master_name = (all_data, "master")
        self.find_matching_x_y()
        print(self.matching)

    def plot_charge_voltage(self, selected_cycles_list, show_title):
        fig, axs = plt.subplots(6, 6, figsize=[20, 15])
        colors = ["r", "b", "g"]

        for row_number, row in enumerate(self._model.master_data):
            x_y_data = row[2]
            medusa_data = row[0]
            mass_data = row[1]
            config = row[3]
            if config is None:
                config = self.config
            channels = x_y_data["channel"].values

            # calculation
            all_cycles = medusa_data.Cycle.unique()
            charges_voltage, x_cal_min, x_cal_max, y_cal_min, y_cal_max = get_charges(medusa_data, channels, mass_data)
            # for channel_index, channel_number in enumerate(channels):
            for channel_index, matching_row in enumerate(self.matching):
                channel_number = matching_row[row_number]

                for cycle_number in selected_cycles_list:
                    if cycle_number not in all_cycles:
                        continue
                    ax = axs[channel_index % 6][int(channel_index / 6)]
                    charge = charges_voltage[channel_number][cycle_number]['charge']
                    voltage = charges_voltage[channel_number][cycle_number]['voltage']
                    ax.plot(charge, voltage, c=colors[row_number], **config["plot"])

                if show_title:
                    x_y_row = x_y_data.loc[x_y_data['channel'] == channel_number]
                    x_value = round(x_y_row.loc[:, "x"].values[0], 2)
                    y_value = round(x_y_row.loc[:, "y"].values[0], 2)
                    existing_title = ax.get_title()
                    if existing_title == "":
                        title = "{}, {}: {}".format(x_value, y_value, channel_number)
                    else:
                        title = existing_title + ",{}".format(channel_number)
                    ax.set_title(title, **config["subplot_title"])

        fig.suptitle("Charge vs Voltage", fontsize=25)
        plt.show()

    # plot normalized current vs voltage
    def plot_norm_volt_cur(self, selected_cycles_list, show_title):
        fig, axs = plt.subplots(6, 6, figsize=[20, 15])
        colors = ["r", "b", "g"]

        for row_number, row in enumerate(self._model.master_data):
            x_y_data = row[2]
            medusa_data = row[0]
            mass_data = row[1]
            config = row[3]
            if config is None:
                config = self.config
            channels = x_y_data["channel"].values

            # calculation
            all_cycles = medusa_data.Cycle.unique()
            norm_cur_voltage, x_cal_min, x_cal_max, y_cal_min, y_cal_max = get_norm_cur_voltage(
                medusa_data, selected_cycles_list, channels, mass_data)
            # for channel_index, channel_number in enumerate(channels):
            for channel_index, matching_row in enumerate(self.matching):
                channel_number = matching_row[row_number]

                for cycle_number in selected_cycles_list:
                    if cycle_number not in all_cycles:
                        continue
                    ax = axs[channel_index % 6][int(channel_index / 6)]
                    ax.plot(norm_cur_voltage[channel_number][cycle_number]["voltage"],
                            norm_cur_voltage[channel_number][cycle_number]["current"], c=colors[row_number], **config["plot"])

                if show_title:
                    x_y_row = x_y_data.loc[x_y_data['channel'] == channel_number]
                    x_value = round(x_y_row.loc[:, "x"].values[0], 2)
                    y_value = round(x_y_row.loc[:, "y"].values[0], 2)
                    existing_title = ax.get_title()
                    if existing_title == "":
                        title = "{}, {}: {}".format(x_value, y_value, channel_number)
                    else:
                        title = existing_title + ",{}".format(channel_number)
                    ax.set_title(title, **config["subplot_title"])

        fig.suptitle("Current vs Voltage", fontsize=25)
        plt.show()

    def validate_medusa_file(self, name, file_type, mapping="karlie"):
        columns, starting_row = get_medusa_columns(mapping)
        try:
            data = pd.read_csv(name, skiprows=starting_row)
            diff = columns.difference(set(data.columns.values))
            if bool(diff):
                message = "Error: Invalidate {} file format. Heading not found: {}".format(
                    file_type,
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            else:
                # change column names in eloi's mapping to it matches to karlie's
                if mapping == 'eloi':
                    change_col_name_eloi_mapping(data)
                return data, True

        except Exception as e:
            message = "Error: Invalidate {} file format. {}".format(file_type, e)
            self.task_bar_message.emit("red", message)
            return [], False

    def validate_config_file(self, name, file_type):
        try:
            with open(name) as json_file:
                data = json.load(json_file)
                return data, True
        except Exception as error:
            message = "Error: Invalidate {} file format. {}".format(file_type, error)
            self.task_bar_message.emit("red", message)
            return [], False

    def validate_x_y_file(self, name, file_type):
        columns = {'channel', 'x', 'y'}
        try:
            data = pd.read_csv(name, nrows=64)
            diff = columns.difference(set(data.columns.values))
            if bool(diff):
                message = "Error: Invalidate {} file ({}) format. Heading not found: {}".format(
                    file_type,
                    name,
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            else:
                x_count = data['x'].count()
                y_count = data['y'].count()
                channel_count = data['channel'].count()
                # There should be 64 values for x and y and no missing data
                if x_count != 64 or y_count != 64 or channel_count != 64 or data.isnull().sum().sum() != 0:
                    message = "Error: Invalidate {} file ({}) format. There should be 64 channels, 64 x values and 64 y values".format(
                        file_type,
                        name,
                        ",".join(diff))
                    self.task_bar_message.emit("red", message)
                    return [], False
                elif not (data['x'].between(0,1).all() and data['y'].between(0,1).all()):
                    message = "Error: Invalidate {} file format. x and/or y values are not between 0 and 1".format(
                        file_type)
                    self.task_bar_message.emit("red", message)
                    return [], False
                elif not pd.Series([x for x in range(1, 65)]).isin(data['channel'].values).all():
                    message = "Error: Invalidate {} file format. Channel number is not a range between 1 and 64".format(
                        file_type)
                    self.task_bar_message.emit("red", message)
                    return [], False
                elif not all(isinstance(x, np.int64) for x in data["channel"].values):
                    message = "Error: Invalidate {} file format. Channel should be integers".format(
                        file_type)
                    self.task_bar_message.emit("red", message)
                    return [], False
                # data = data.set_index('channel')
                return data, True

        except Exception as error:
            message = "Error: Invalidate {} file format. {}".format(file_type, error)
            self.task_bar_message.emit("red", message)
            return [], False

    def validate_mass_file(self, name, file_type):
        columns = get_mass_columns()
        try:
            data = pd.read_csv(name, nrows=1)
            diff = columns.difference(set(data.columns.values))
            if bool(diff):
                message = "Error: Invalidate {} file format. Heading not found: {}".format(
                    file_type,
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            return data.iloc[0, 2:].values, True
        except Exception:
            message = "Error: Invalidate {} file format.".format(file_type)
            self.task_bar_message.emit("red", message)
            return [], False

    def find_matching_x_y(self):
        self.matching = []
        master_data = self._model.master_data
        x_y_data = master_data[0][2]
        xs_1= self.get_common_x_y(x_y_data)
        # print(xs_1["x"])
        x_y_data = master_data[1][2]
        xs_2 = self.get_common_x_y(x_y_data)
        x_y_data = master_data[2][2]
        xs_3 = self.get_common_x_y(x_y_data)

        for row in xs_1.iterrows():
            first_channel = int(row[1]["channel"])
            x = row[1]["x"]
            y = row[1]["y"]
            second_channel = xs_2[(xs_2['x'] == x) & (xs_2['y'] == y)]["channel"].values[0]
            third_channel = xs_3[(xs_3['x'] == x) & (xs_3['y'] == y)]["channel"].values[0]
            self.matching.append([first_channel, second_channel, third_channel])

    def get_common_x_y(self, x_y_data):
        return x_y_data[(x_y_data["x"] <= 0.5) &
                        (x_y_data["y"] <= 0.5) &
                        ((1 - x_y_data["x"] - x_y_data["y"]) <= 0.5)]





