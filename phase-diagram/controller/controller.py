from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize
import matplotlib.pyplot as plt
import ternary
import numpy as np
from controller.helper import *


class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)

    def __init__(self, model):
        super().__init__()
        self._model = model

    def plot(self, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2,
             selected_operation, min_color_scale, max_color_scale):

        data = self._model.ternary_file_data
        # perform calculation
        data = calculate(data, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2, selected_operation)
        # remove the inf and nan
        inf_nan_indexes = data.index[data['calculated'].isin([np.nan, np.inf, -np.inf])].tolist()
        print("bad indexes:", inf_nan_indexes)
        data = data.drop(inf_nan_indexes)

        # get default min and max color scale if values are not defined
        if min_color_scale is None:
            min_color_scale = min(data["calculated"].values)
        if max_color_scale is None:
            max_color_scale = max(data["calculated"].values)

        # remove data that is out of range
        data = data.loc[data.loc[:, 'calculated'] >= min_color_scale, :]
        data = data.loc[data.loc[:, 'calculated'] <= max_color_scale, :]

        points = np.array([data["x"].values, data["y"].values]).transpose()
        # colors map
        # c = mcolors.ColorConverter().to_rgb
        # reds = plt.get_cmap("Reds")
        # norm = plt.Normalize(0, 1)
        # rvb = make_colormap(
        #     [c('red'), c('violet'), 0.33, c('violet'), c('blue'), 0.66, c('blue')])
        cm = LinearSegmentedColormap.from_list('Capacities', ['blue', 'red'], N=1024)

        # normalize data
        norm = Normalize(vmin=max_color_scale, vmax=max_color_scale)

        # get color based on color map
        data["calculated"] = data["calculated"].apply(lambda x: cm(norm(x)))
        colors = data["calculated"].values

        # Creates a ternary set of axes to plot the diagram from python-ternary
        fig, ax = plt.subplots(figsize=(15, 10))
        tax = ternary.TernaryAxesSubplot(ax=ax, scale=1.0)
        tax.boundary()
        tax.gridlines(multiple=0.1, color='blue')
        tax.scatter(points, marker = 'o', c = colors, s=64,colorbar = True, colormap = cm, vmin=min_color_scale, vmax=max_color_scale)
        tax.ticks(axis='blr', linewidth=1.0, multiple=0.1, tick_formats='%.1f', offset=0.02)
        plt.axis('off')
        tax.show()
        tax.close()

    @pyqtSlot(str)
    def file_name_changed(self, name):
        # update model
        data, valid = self.validate_ternary_file(name, "ternary")

        if valid:
            self._model.file_name = {"name": name, "data": data}

    def file_name_changed(self, file_name, file_type, exclude_channels=""):
        # TODO: Validate if the file
        valid = False
        if file_type == "master":
            data, valid = self.validate_master_file(file_name, file_type)
        elif file_type == "ternary":
            data, valid = self.validate_ternary_file(file_name, file_type, exclude_channels, self._model.ternary_file_data)
        elif file_type == "config":
            data, valid = self.validate_config_file(file_name, file_type)

        # update model
        if valid:
            self._model.add_data(data, file_type)

    def validate_ternary_file(self, name, file_type, exclude_channels, master_data):
        # validate exclude channel
        exclude_channels = validate_exclude_channels(exclude_channels)
        if exclude_channels is None:
            message = "Invalid exclude channel format"
            self.task_bar_message.emit("red", message)
            return [], False
        columns = {"channels", "x", "y"}
        try:
            # read file
            data = pd.read_csv(name)
            diff = columns.difference(set(data.columns.values))

            # check columns
            if bool(diff):
                message = "Error: Invalidate file format. Heading not found: {}".format(
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            else:  # all checks are done , we gucci to update model
                # remove exclude channels (outliers)
                data = remove_exclude(data, exclude_channels)
                if master_data is not None:
                    data = pd.concat([master_data, data], sort=True)

                # remove duplicate and average them
                data = remove_duplicate(data)
                return data, True
        except Exception as e:
            message = "Error: Invalidate {} file format. {}".format(file_type, e)
            self.task_bar_message.emit("red", message)
            return [], False

    def validate_master_file(self, name, file_type):
        try:
            # read file
            data = pd.read_csv(name)
            master_data = None
            for index, row in data.iterrows():
                file_path = row[0]
                exclude_channels = row[1]
                ternary_data, valid = self.validate_ternary_file(file_path, "ternary", exclude_channels, master_data)
                if not valid:
                    message = "Error: Invalidate file format. Error in row {}".format(index+1)
                    self.task_bar_message.emit("red", message)
                    return [], False
                # if master_data is not None:
                #     master_data = pd.concat([master_data, ternary_data], sort=False)
                # else:
                master_data = ternary_data

            # everything is fine return file
            return master_data, True
        except Exception as e:
            message = "Error: Invalidate {} file format. Check Line {} | {}".format(file_type, index + 2, e)
            self.task_bar_message.emit("red", message)
            return [], False
