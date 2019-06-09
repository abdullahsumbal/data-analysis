from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import matplotlib.pyplot as plt
from controllers.helper import *
import pandas as pd


class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.figure_number = 1

    def plot(self, selected_cycles, selected_channels, x_limit, y_limit, plot_name):
        # cycle validation
        all_cycles = get_unique_cycles(self._model.medusa_data)
        valid, message = validate_cycles(all_cycles, selected_cycles)
        if not valid:
            self.task_bar_message.emit("red", message)
            return

        # channel validation
        valid, message = validate_channels(selected_channels)
        if not valid:
            self.task_bar_message.emit("red", message)
            return

        # get data from model
        data = self._model.medusa_data

        # changing cycle user input into array
        if selected_cycles == "all":
            selected_cycles_list = all_cycles.tolist()
        else:
            selected_cycles_list = get_selected_cycles_list(selected_cycles)

        # change scale x-axis user input to int
        x_min = scale_user_input_to_float(x_limit[0])
        x_max = scale_user_input_to_float(x_limit[1])
        # change scale y-axis user input to int
        y_min = scale_user_input_to_float(y_limit[0])
        y_max = scale_user_input_to_float(y_limit[1])

        # validate limits
        if not (self.validate_limit(x_min, x_max) and self.validate_limit(y_min, y_max)):
            return

        # plot graph based on plot names
        if plot_name == "norm":
            self.plot_norm_volt_cur(x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels, data)
        elif plot_name == "charge":
            self.plot_charge_discharge(x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels, data)

    # plot normalized current vs voltage
    def plot_charge_discharge(self, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels, data):

        # changing channel user input into array
        if selected_channels == "all":
            # selected_channels = [i for i in range(1, 65)]
            plt.figure(self.figure_number, figsize=(20, 15))
            channel_number = 1
            for row in range(8):
                for col in range(8):
                    for cycle in selected_cycles_list:
                        # get mass data
                        mass = 1
                        if self._model.mass_data is not None:
                            mass = self._model.mass_data.loc[:,"Channel {}".format(channel_number)].values[0]

                        # get selected cycle data
                        cycle_data = data[data['Cycle'] == cycle]
                        # get voltage
                        voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
                        # get current
                        current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].values/mass

                        # make subplot
                        plt.subplot(8, 8, channel_number)

                        plt.plot(voltage_cycle, current_cycle, 'b', linewidth=2.0, label='Charge')

                    # increment figure number for new plots.
                    channel_number += 1

            plt.ylim(bottom=y_min, top=y_max)  # set the y-axis limits
            plt.xlim(left=x_min, right=x_max)  # set the x-axis limits
            # update status bar
            self.task_bar_message.emit("green", "Figure {}: Plotting cycles {} and all channels".format(
                self.figure_number,
                ",".join(map(str, selected_cycles_list))
                ))
            self.figure_number += 1
            plt.show()
            plt.close()
        else:
            selected_channels = [int(selected_channels.strip())]
            plt.figure(self.figure_number, figsize=(20, 15))
            for channel_number in selected_channels:
                for cycle in selected_cycles_list:
                    # get mass data
                    mass = 1
                    if self._model.mass_data is not None:
                        mass = self._model.mass_data.loc[:, "Channel {}".format(channel_number)].values[0]
                    # get selected cycle data
                    cycle_data = data[data['Cycle'] == cycle]
                    # get voltage
                    voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
                    # get current
                    current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].values/mass
                    plt.plot(voltage_cycle, current_cycle, 'b', linewidth=2.0, label='Charge')

            plt.ylim(bottom=y_min, top=y_max)  # set the y-axis limits
            plt.xlim(left=x_min, right=x_max)  # set the x-axis limits
            # update status bar
            self.task_bar_message.emit("green", "Figure {}: Plotting cycles {} and channel {}".format(
                self.figure_number,
                ",".join(map(str, selected_cycles_list)),
                *selected_channels))
            self.figure_number += 1
            plt.show()
            plt.close()

    # plot normalized current vs voltage
    def plot_norm_volt_cur(self, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels, data):

        # changing channel user input into array
        if selected_channels == "all":
            # selected_channels = [i for i in range(1, 65)]
            plt.figure(self.figure_number, figsize=(20, 15))
            channel_number = 1
            for row in range(8):
                for col in range(8):
                    for cycle in selected_cycles_list:
                        # get mass data
                        mass = 1
                        if len(self._model.mass_data) > 0:
                            mass = self._model.mass_data[channel_number - 1]

                        # get selected cycle data
                        cycle_data = data[data['Cycle'] == cycle]
                        # get voltage
                        voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
                        # get current
                        current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].values/mass

                        # make subplot
                        plt.subplot(8, 8, channel_number)

                        plt.plot(voltage_cycle, current_cycle, 'b', linewidth=2.0, label='Charge')

                    # increment figure number for new plots.
                    channel_number += 1

            plt.ylim(bottom=y_min, top=y_max)  # set the y-axis limits
            plt.xlim(left=x_min, right=x_max)  # set the x-axis limits
            # update status bar
            self.task_bar_message.emit("green", "Figure {}: Plotting cycles {} and all channels".format(
                self.figure_number,
                ",".join(map(str, selected_cycles_list))
                ))
            self.figure_number += 1
            plt.show()
            plt.close()
        else:
            selected_channels = [int(selected_channels.strip())]
            plt.figure(self.figure_number, figsize=(20, 15))
            for channel_number in selected_channels:
                for cycle in selected_cycles_list:
                    # get mass data
                    mass = 1
                    if len(self._model.mass_data) > 0:
                        mass = self._model.mass_data[channel_number - 1]
                    # get selected cycle data
                    cycle_data = data[data['Cycle'] == cycle]
                    # get voltage
                    voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
                    # get current
                    current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].values/mass
                    plt.plot(voltage_cycle, current_cycle, 'b', linewidth=2.0, label='Charge')

            plt.ylim(bottom=y_min, top=y_max)  # set the y-axis limits
            plt.xlim(left=x_min, right=x_max)  # set the x-axis limits
            # update status bar
            self.task_bar_message.emit("green", "Figure {}: Plotting cycles {} and channel {}".format(
                self.figure_number,
                ",".join(map(str, selected_cycles_list)),
                *selected_channels))
            self.figure_number += 1
            plt.show()
            plt.close()

    @pyqtSlot(str)
    def file_name_changed(self, name, file_type):
        # TODO: Validate if the file
        valid = False
        if file_type == "medusa":
            data, valid = self.validate_medusa_file(name, file_type)
        elif file_type == "mass":
            data, valid = self.validate_mass_file(name)
        elif file_type == "x_y":
            data, valid = validate_x_y_file(name)
        elif file_type == "config":
            data, valid = validate_config_file(name)
        # resistances_header = pd.read_csv(name, header=6, nrows=0)
        # resistances_values = pd.read_csv(name, skiprows=4, nrows=1)
        # self._model.resistances = resistances_values

        # update model
        if valid:
            self._model.file_name = (name, data, file_type)


    def get_unique_cycles(self, data):
        return data.Cycle.unique()

    def get_all_cycles(self):
        return self._model.medusa_data.Cycle.unique()

    def validate_limit(self, min, max):
        if not (min and max):
            return True
        # min has to be greater than max
        if min > max:
            self.task_bar_message.emit("red", "maximum limit has to be greater than minimum limit")
            return False
        return True

    def zoom_factory(self, ax, base_scale=2.):
        def zoom_fun(event):
            # get the current x and y limits
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
            cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
            xdata = event.xdata  # get event x location
            ydata = event.ydata  # get event y location
            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print
                event.button
            # set new limits
            ax.set_xlim([xdata - cur_xrange * scale_factor,
                         xdata + cur_xrange * scale_factor])
            ax.set_ylim([ydata - cur_yrange * scale_factor,
                         ydata + cur_yrange * scale_factor])
            plt.draw()  # force re-draw

        fig = ax.get_figure()  # get the figure of interest
        # attach the call back
        fig.canvas.mpl_connect('scroll_event', zoom_fun)

        # return the function
        return zoom_fun

    def validate_medusa_file(self, name, file_type):
        columns = get_medusa_columns()
        try:
            data = pd.read_csv(name, skiprows=7)
            diff = columns.difference(set(data.columns.values))
            if bool(diff):
                message = "Error: Invalidate {} file format. Heading not found: {}".format(
                    file_type,
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            else:
                return data, True

        except Exception:
            message = "Error: Invalidate {} file format.".format(file_type)
            self.task_bar_message.emit("red", message)
            return [], False

    def validate_mass_file(self, name):
        columns = get_mass_columns()
        try:
            data = pd.read_csv(name, nrows=1)
            if bool(columns.difference(set(data.columns.values))):
                return [], False
            return data.iloc[0, 2:].values, True
        except Exception:
            return [], False