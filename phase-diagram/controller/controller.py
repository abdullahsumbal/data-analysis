from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import pandas as pd
import ternary
from controller.helper import *
from os import path


class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)

    def __init__(self, model):
        super().__init__()
        self._model = model

    def plot(self):
        data = self._model.ternary_file_data
        scale = 1
        figure, tax = ternary.figure(scale=scale)

        # Draw Boundary and Gridlines
        tax.boundary(linewidth=2.0)
        tax.gridlines(color="blue", multiple=5)

        # Set Axis labels and Title
        fontsize = 12
        offset = 0.14
        tax.set_title("Various Lines\n", fontsize=fontsize)
        tax.right_corner_label("X", fontsize=fontsize)
        tax.top_corner_label("Y", fontsize=fontsize)
        tax.left_corner_label("Z", fontsize=fontsize)
        tax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize, offset=offset)
        tax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize, offset=offset)
        tax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$", fontsize=fontsize, offset=offset)

        # Draw lines parallel to the axes
        tax.horizontal_line(0.1)
        tax.left_parallel_line(10, linewidth=2., color='red', linestyle="--")
        tax.right_parallel_line(20, linewidth=3., color='blue')

        # Draw an arbitrary line, ternary will project the points for you
        points = []
        for channel in range(64):
            points.append((data["x"].values, data["y"].values))
        p1 = (22, 8, 10)
        p2 = (2, 22, 16)
        tax.scatter(points, marker='o', color='green')

        tax.ticks(axis='lbr', multiple=5, linewidth=1, offset=0.025)
        tax.get_axes().axis('off')
        tax.clear_matplotlib_ticks()
        tax.show()

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
            data, valid = self.validate_ternary_file(file_name, file_type, exclude_channels)
        elif file_type == "config":
            data, valid = self.validate_config_file(file_name, file_type)

        # update model
        if valid:
            self._model.add_data(data, file_type)

    def validate_ternary_file(self, name, file_type, exclude_channels):
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
                if self._model.ternary_file_data is not None:
                    data = pd.concat([self._model.ternary_file_data, data], sort=True)
                # print(data.shape)
                print("Removing", exclude_channels)
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
                ternary_data, valid = self.validate_ternary_file(file_path, "ternary", exclude_channels)
                if not valid:
                    message = "Error: Invalidate file format. Error in row {}".format(index+1)
                    self.task_bar_message.emit("red", message)
                    return [], False
                if master_data is not None:
                    master_data = pd.concat([master_data, ternary_data], sort=False)
                else:
                    master_data = ternary_data

            # everything is fine return file
            return master_data, True
        except Exception as e:
            message = "Error: Invalidate {} file format. Check Line {} | {}".format(file_type, index + 2, e)
            self.task_bar_message.emit("red", message)
            return [], False
