from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
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
                        },
                        "subplot_axis_label_name": {
                            "norm": {"x": "V vs Li/Li\u207A", "y": "Normalized Current (mA/g)"},
                            "charge": {"x": "Charge/Discharge Capacity (mAh/g)", "y": "Average Voltage (V)"},
                            "avg_voltage": {"x": "Cycles Number", "y": "Average Voltage (V)"},
                            "capacity": {"x": "Cycles Number", "y": "Specific Capacity (mAh/g)"}
                        },
                         "subplot_spacing": {"hspace": 0.05, "wspace": 0.05}
                    }

    # @pyqtSlot(str)
    # def file_name_changed(self, name):
    #     # update model
    #
    #     valid = self.validate_master(name)
    #     self._model.file_name = name


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

            # this is for testing because I don't have good data
            # x_y_data = x_y_data.iloc[:36, :]
            # x_y_data = x_y_data[(x_y_data["x"] + x_y_data["y"] >= 0.5) |
            #               (x_y_data["x"] + (1 - x_y_data["y"]) >= 0.5) &
            #               (x_y_data["y"] + (1 - x_y_data["x"]) >= 0.5)]
            # print(x_y_data.shape)
            all_data[index].append(x_y_data)

            # config_file validation
            if isinstance(config_file, str):
                config_data, config_valid = self.validate_config_file(config_file, "config")
                if not config_valid:
                    return
                all_data[index].append(config_data)
            else:
                all_data[index].append(None)


        self._model.master_name = ((all_data, "master"))
        self.test()
        # self.plot_norm_volt_cur()
        # self.plot_charge_voltage()


    def plot_charge_voltage(self):
        fig, axs = plt.subplots(6, 6, figsize=[20, 15])
        colors = ["r", "b", "g"]

        for row_number, row in enumerate(self._model.master_data):
            x_y_data = row[2]
            medusa_data = row[0]
            mass_data = row[1]
            config = self.config
            channels = x_y_data["channel"].values

            # calculation
            selected_cycles_list = medusa_data.Cycle.unique()
            charges_voltage, x_cal_min, x_cal_max, y_cal_min, y_cal_max = get_charges(medusa_data, channels, mass_data)
            print(channels.shape)
            for channel_index, channel_number in enumerate(channels):

                for cycle_number in selected_cycles_list:
                    ax = axs[channel_index % 6][int(channel_index / 6)]
                    charge = charges_voltage[channel_number][cycle_number]['charge']
                    voltage = charges_voltage[channel_number][cycle_number]['voltage']
                    ax.plot(charge, voltage, c=colors[row_number], **self.config["plot"])

                    ax.set_title('Channel {}'.format(channel_number), **config["subplot_title"])

        fig.suptitle("Charge vs Voltage", fontsize=25)
        plt.show()





    # plot normalized current vs voltage
    def plot_norm_volt_cur(self):
        fig, axs = plt.subplots(6, 6, figsize=[20, 15])
        colors = ["r", "b", "g"]

        for row_number, row in enumerate(self._model.master_data):
            x_y_data = row[2]
            medusa_data = row[0]
            mass_data = row[1]
            config = self.config
            channels = x_y_data["channels"].values

            # calculation
            selected_cycles_list = medusa_data.Cycle.unique()
            norm_cur_voltage, x_cal_min, x_cal_max, y_cal_min, y_cal_max = get_norm_cur_voltage(
                medusa_data, selected_cycles_list, channels, mass_data)
            print(channels.shape)
            for channel_index, channel_number in enumerate(channels):

                for cycle_number in selected_cycles_list:
                    ax = axs[channel_index % 6][int(channel_index / 6)]
                    ax.plot(norm_cur_voltage[channel_number][cycle_number]["voltage"],
                            norm_cur_voltage[channel_number][cycle_number]["current"], c=colors[row_number])

                    ax.set_title('Channel {}'.format(channel_number), **config["subplot_title"])

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
        columns = {'channels', 'x', 'y'}
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
                channel_count = data['channels'].count()
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
                elif not pd.Series([x for x in range(1, 65)]).isin(data['channels'].values).all():
                    message = "Error: Invalidate {} file format. Channel number is not a range between 1 and 64".format(
                        file_type)
                    self.task_bar_message.emit("red", message)
                    return [], False
                elif not all(isinstance(x, np.int64) for x in data["channels"].values):
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

    def test(self):
        xs = pd.DataFrame()
        master_data = self._model.master_data
        x_y_data = master_data[0][2]
        xs["x_1"] = self.get_common_x_y(x_y_data)["x"]
        print(xs["x_1"].shape)
        x_y_data = master_data[1][2]
        xs["x_2"] = self.get_common_x_y(x_y_data)["x"]
        print(xs["x_2"].shape)
        x_y_data = master_data[2][2]
        xs["x_3"] = self.get_common_x_y(x_y_data)["x"]
        print(xs["x_3"].shape)
        print(xs[(xs["x_1"].values == xs["x_3"].values)])

        # x_y_data_1 = master_data[1][2]
        # for x in x_y_data["x"]:
        #     if x not in x_y_data_1["x"].values:
        #         print("not found", x)
        # xs = pd.DataFrame()
        # xs["x_1"] = master_data[0][2]["x"]
        # xs["x_2"] = master_data[2][2]["x"]



    def get_common_x_y(self, x_y_data):
        return x_y_data
        return x_y_data[(x_y_data["x"]  <= 0.5) &
                            (   x_y_data["y"] <= 0.5) &
                            ((1 - - x_y_data["x"] - x_y_data["y"]) <= 0.5)]





