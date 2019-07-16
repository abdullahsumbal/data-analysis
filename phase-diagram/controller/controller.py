from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize
import matplotlib.pyplot as plt
import ternary
import numpy as np
import os
import json
from controller.helper import *


class MainController(QObject):
    task_bar_message = pyqtSignal(dict)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.default_config = {
                        "axis_label": {
                            "fontsize": 25
                        },
                        "scatter": {
                            "marker": "o",
                            "colorbar": True,
                            "linewidth": 5
                        },
                        "colors": ["blue", "red"],
                        "figure": {
                            "figsize": [15, 10]
                        },
                        "title": {
                            "fontsize": 25,
                            "y": 1.08
                        },
                        "axis_ticks": {
                            "axis": "blr",
                            "linewidth": 1.0,
                            "fontsize": 20,
                            "multiple": 0.1,
                            "tick_formats": "%.1f",
                            "offset": 0.02
                        },
                        "gridlines": {
                            "multiple": 0.1,
                            "color": "blue"
                        },
                        "colorbar_tick_params": {
                            "labelsize": 20,
                            "width": 3,
                            "size": 10,
                            "direction": "out"
                        }
                    }

    def plot(self, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2,
             selected_operation, min_color_scale, max_color_scale, is_percentage):

        #get config
        if self._model.config_data is not None:
            config = self._model.config_data
        else:
            config = self.default_config

        data = self._model.ternary_file_data
        # perform calculation
        data, title = self.calculate(data, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2, selected_operation, is_percentage)
        # remove the inf and nan
        inf_nan_indexes = data.index[data['calculated'].isin([np.nan, np.inf, -np.inf])].tolist()
        inf_indexes = data[data['calculated'].isin([np.inf, -np.inf])]
        data = data.drop(inf_nan_indexes)

        # get default min and max color scale if values are not defined
        if min_color_scale is None:
            min_color_scale = min(data["calculated"].values)
        else:
            min_color_scale = float(min_color_scale)
        if max_color_scale is None:
            max_color_scale = max(data["calculated"].values)
        else:
            max_color_scale = float(max_color_scale)

        # remove/replace data that is out of range
        # remove
        # data = data.loc[data.loc[:, 'calculated'] >= min_color_scale, :]
        # data = data.loc[data.loc[:, 'calculated'] <= max_color_scale, :]
        # replace
        data['calculated'].values[data['calculated'].values < min_color_scale] = min_color_scale
        data['calculated'].values[data['calculated'].values > max_color_scale] = max_color_scale

        points = np.array([data["x"].values, data["y"].values]).transpose()
        # colors map
        cm = LinearSegmentedColormap.from_list('Capacities', config["colors"], N=1024)

        # normalize data
        norm = Normalize(vmin=min_color_scale, vmax=max_color_scale)

        # get color based on color map
        data["calculated_norm"] = data["calculated"].apply(lambda x: norm(x))
        data["calculated_color"] = data["calculated_norm"].apply(lambda x: cm(x))
        colors = data["calculated_color"].values

        # Creates a ternary set of axes to plot the diagram from python-ternary
        fig, ax = plt.subplots(**config["figure"])
        # fix aspect ratio.
        ax.set_aspect("equal")
        ax.set_title("Figure : {} | {}".format(plt.gcf().number, title), **config["title"])
        tax = ternary.TernaryAxesSubplot(ax=ax, scale=1.0)
        tax.boundary()
        tax.gridlines(**config["gridlines"])
        tax.scatter(points, c=colors,  colormap=cm, vmin=min_color_scale, vmax=max_color_scale, **config["scatter"])
        # colorbar
        cbar_ax = fig.axes[-1]
        cbar_ax.tick_params(**config["colorbar_tick_params"])
        # ticks
        tax.ticks(**config["axis_ticks"])
        # set axis labels
        tax.left_axis_label("1 - x - y", offset=0.11, **config["axis_label"])
        tax.right_axis_label("y", offset=0.105, **config["axis_label"])
        tax.bottom_axis_label("x", offset=0.005, **config["axis_label"])
        plt.axis('off')
        # if there are some inf index , so report it to user
        if not inf_indexes.empty:
            tooltip = inf_indexes[['x', 'y']].to_string()
            task_bar_data = {"color": "orange",
                             'message': "Figure : {} | Warning: calculation contains inf | {}".format(plt.gcf().number, title),
                             'tooltip': tooltip}
            self.task_bar_message.emit(task_bar_data)
        else:
            self.task_bar_message.emit({"color": "green",
                                        "message": "Figure : {} | {}".format(plt.gcf().number, title),
                                        "tooltip": "{} rows were removed: {}".format(str(len(inf_nan_indexes)), ",".join(str(x) for x in inf_nan_indexes))})
        tax.show()
        tax.close()

    def export(self, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2,
                                   selected_operation, is_percentage, file_name):

        data = self._model.ternary_file_data
        # perform calculation
        data, _ = self.calculate(data, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2, selected_operation, is_percentage)

        # get basename to show in task bar.
        csv_file_basename = os.path.basename(file_name)
        try:
            columns_to_export = ["x", "y", selected_type_dict[selected_type_1] + selected_cycle_1, "calculated"]
            if selected_type_2 is not None:
                columns_to_export.insert(3, selected_type_dict[selected_type_2] + selected_cycle_2)
            data = data[columns_to_export]
            data.to_csv(file_name, index=False)
            self.task_bar_message.emit({"color": "green", "message": "Successfully written to {}".format(csv_file_basename)})
        except PermissionError:
            self.task_bar_message.emit({"color": "red", "message": "Do not have permission to open file. {} may be in use.".format(csv_file_basename)})


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
            self.task_bar_message.emit({"color": "red", "message": message})
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
                self.task_bar_message.emit({"color": "red", "message": message})
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
            self.task_bar_message.emit({"color": "red", "message": message})
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
                    self.task_bar_message.emit({"color": "red", "message": message})
                    return [], False
                # if master_data is not None:
                #     master_data = pd.concat([master_data, ternary_data], sort=False)
                # else:
                master_data = ternary_data

            # everything is fine return file
            return master_data, True
        except Exception as e:
            message = "Error: Invalidate {} file format. Check Line {} | {}".format(file_type, index + 2, e)
            self.task_bar_message.emit({"color": "red", "message": message})
            return [], False

    def validate_config_file(self, name, file_type):
        try:
            with open(name) as json_file:
                data = json.load(json_file)
                return data, True
        except Exception as error:
            message = "Error: Invalidate {} file format. {}".format(file_type, error)
            self.task_bar_message.emit({"color": "red", "message": message})
            return [], False

    def calculate(self, data, selected_type_1, selected_cycle_1, selected_type_2, selected_cycle_2, selected_operation, is_percentage):

        title = ""
        # if compare is not checked
        if selected_operation is None:
            data["calculated"] = data[selected_type_dict[selected_type_1] + selected_cycle_1]
            title += "Type: {} and Cycle {}".format(selected_type_1, selected_cycle_1)
            # print(data[[selected_type_dict[selected_type_1] + selected_cycle_1, "calculated"]])
            return data, title

        # if compare is checked
        if selected_operation == "Subtract (-)":
            data["calculated"] = data[selected_type_dict[selected_type_1] + selected_cycle_1] - \
                                 data[selected_type_dict[selected_type_2] + selected_cycle_2]
        elif selected_operation == "Multiple (*)":
            data["calculated"] = data[selected_type_dict[selected_type_1] + selected_cycle_1] * \
                                 data[selected_type_dict[selected_type_2] + selected_cycle_2]
        elif selected_operation == "Divide (/)":
            data["calculated"] = data[selected_type_dict[selected_type_1] + selected_cycle_1] / \
                                 data[selected_type_dict[selected_type_2] + selected_cycle_2]

        title += "Type: {} and Cycle {}  {}  Type {} and Cycle {}".format(
            selected_type_1,
            selected_cycle_1,
            selected_operation,
            selected_type_2,
            selected_cycle_2)
        if is_percentage:
            # data["avg"] = data[selected_type_dict[selected_type_1] + selected_cycle_1]/2 + \
            #                      data[selected_type_dict[selected_type_2] + selected_cycle_2]/2
            data["calculated"] = data["calculated"] / data[selected_type_dict[selected_type_1] + selected_cycle_1]
            title += "  (Percentage)"
        # print(data[[selected_type_dict[selected_type_1] + selected_cycle_1,
        # selected_type_dict[selected_type_2] + selected_cycle_2, "calculated"]])
        return data, title
