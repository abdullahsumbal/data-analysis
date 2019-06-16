from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import matplotlib.pyplot as plt
from controllers.helper import *
import pandas as pd
import csv
import os


class MainController(QObject):
    task_bar_message = pyqtSignal(str, str)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.figure_number = 1
        self.charges = None
        self.avg_voltages = None

    # general plot function which is reponsible for calling other plot functions.
    def plot(self, selected_cycles, selected_channels, x_limit, y_limit, plot_name, x_y_label_checked):
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

        # changing channel user input into array
        if selected_channels == "all":
            selected_channels_list = [i for i in range(1, 65)]
        else:
            selected_channels_list = [int(selected_channels.strip())]

        # change scale x-axis user input to int
        x_min = scale_user_input_to_float(x_limit[0])
        x_max = scale_user_input_to_float(x_limit[1])
        # change scale y-axis user input to int
        y_min = scale_user_input_to_float(y_limit[0])
        y_max = scale_user_input_to_float(y_limit[1])

        # validate limits
        if not (self.validate_limit(x_min, x_max) and self.validate_limit(y_min, y_max)):
            return

        if len(selected_channels_list) == 1:
            fig, axs = plt.subplots(1, 1, figsize=(20, 15))
        else:
            fig, axs = plt.subplots(8, 8, figsize=(20, 15))

        # plot graph based on plot names
        if plot_name == "norm":
            self.plot_norm_volt_cur(axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data)
        elif plot_name == "charge":
            self.plot_charge_discharge(axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data)
        elif plot_name == "avg_voltage":
            self.plot_avg_voltage(axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data)
        elif plot_name == "capacity":
            self.plot_capacity(axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data)

        # update status bar
        channel_message = "all channels"
        if len(selected_channels_list) == 1:
            channel_message = "channel {}".format(*selected_channels_list)
        message = "Figure {}: Normalize Current and Voltage plot for {} {} and {}".format(
            self.figure_number,
            "cycles" if len(selected_channels_list) > 1 else "cycle",
            ",".join(map(str, selected_cycles_list)),
            channel_message
            )
        self.task_bar_message.emit("green", message)
        self.figure_number += 1
        if len(selected_channels_list) == 1:
            zp = ZoomPan()
            zp.zoom_factory(axs, base_scale=1.2)
            zp.pan_factory(axs)
        fig.suptitle(message, fontsize=25)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        plt.show()
        plt.close()

    # plot normalized current vs voltage
    def plot_capacity(self, axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data):
        self.charges = get_charges(data, selected_channels_list)
        for channel_index in range(len(selected_channels_list)):
            channel_number = selected_channels_list[channel_index]
            for cycle_number in selected_cycles_list:

                # get subplot
                if len(selected_channels_list) == 1:
                    ax = axs
                else:
                    ax = axs[int(channel_index / 8)][channel_index % 8]

                charge = self.charges[channel_number][cycle_number]['charge']
                ax.scatter(charge[-1], cycle_number)

                # put ticks inside
                ax.tick_params(direction='in')
                # set subplot limits
                set_plot_limits(ax, x_min, x_max, y_min, y_max)
                # set subplot title
                set_subplot_tile(ax, x_y_label_checked, self._model.x_y_data, channel_number)

    # plot normalized current vs voltage
    def plot_avg_voltage(self, axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data):
        self.avg_voltages = get_avg_voltage(data, selected_cycles_list, selected_channels_list)
        for channel_index in range(len(selected_channels_list)):
            channel_number = selected_channels_list[channel_index]
            for cycle_number in selected_cycles_list:
                # get subplot
                if len(selected_channels_list) == 1:
                    ax = axs
                else:
                    ax = axs[int(channel_index / 8)][channel_index % 8]
                charge = self.avg_voltages[channel_number][cycle_number]
                ax.scatter(cycle_number, charge)

                # put ticks inside
                ax.tick_params(direction='in')
                # set subplot limits
                set_plot_limits(ax, x_min, x_max, y_min, y_max)
                # set subplot title
                set_subplot_tile(ax, x_y_label_checked, self._model.x_y_data, channel_number)

    # plot normalized current vs voltage
    def plot_charge_discharge(self, axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data):
        self.charges = get_charges(data, selected_channels_list)
        for channel_index in range(len(selected_channels_list)):
            channel_number = selected_channels_list[channel_index]
            for cycle_number in selected_cycles_list:
                # get subplot
                if len(selected_channels_list) == 1:
                    ax = axs
                else:
                    ax = axs[int(channel_index / 8)][channel_index % 8]

                charge = self.charges[channel_number][cycle_number]['charge']
                voltage = self.charges[channel_number][cycle_number]['voltage']
                ax.plot(charge, voltage, linewidth=2.0, label='Charge')

                # put ticks inside
                ax.tick_params(direction='in')
                # set subplot limits
                set_plot_limits(ax, x_min, x_max, y_min, y_max)
                # set subplot title
                set_subplot_tile(ax, x_y_label_checked, self._model.x_y_data, channel_number)

    # plot normalized current vs voltage
    def plot_norm_volt_cur(self, axs, x_min, x_max, y_min, y_max, selected_cycles_list, selected_channels_list, x_y_label_checked, data):

        for channel_index in range(len(selected_channels_list)):
            channel_number = selected_channels_list[channel_index]
            for cycle_number in selected_cycles_list:
                # get subplot
                if len(selected_channels_list) == 1:
                    ax = axs
                else:
                    ax = axs[int(channel_index / 8)][channel_index % 8]
                # get mass data
                mass = 1
                if len(self._model.mass_data) > 0:
                    mass = self._model.mass_data[channel_number - 1]

                # get selected cycle data
                cycle_data = data[data['Cycle'] == cycle_number]
                # get voltage
                voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
                # get current
                current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].values/mass

                ax.plot(voltage_cycle, current_cycle, 'b', linewidth=2.0, label='Charge')

                # put ticks inside
                ax.tick_params(direction='in')
                # set subplot limits
                set_plot_limits(ax, x_min, x_max, y_min, y_max)
                # set subplot title
                set_subplot_tile(ax, x_y_label_checked, self._model.x_y_data, channel_number)

    def validate_cycles_channels(self, selected_cycles, selected_channels):
        # cycle validation
        all_cycles = get_unique_cycles(self._model.medusa_data)
        valid, message = validate_cycles(all_cycles, selected_cycles)
        if not valid:
            self.task_bar_message.emit("red", message)
            return False

        # channel validation
        valid, message = validate_channels(selected_channels)
        if not valid:
            self.task_bar_message.emit("red", message)
            return False

        return True

    def export_csv(self, selected_cycles, selected_channels, csv_file_name):
        # changing cycle user input into array
        if selected_cycles == "all":
            all_cycles = get_unique_cycles(self._model.medusa_data)
            selected_cycles_list = all_cycles.tolist()
        else:
            selected_cycles_list = get_selected_cycles_list(selected_cycles)

        # changing channel user input into array
        if selected_channels == "all":
            selected_channels_list = [i for i in range(1, 65)]
        else:
            selected_channels_list = [int(selected_channels.strip())]

        # get data from model
        data = self._model.medusa_data
        # calculate charges
        self.charges = get_charges(data, selected_cycles_list, selected_channels_list)

        if csv_file_name[-4:] != ".csv":
            csv_file_name += ".csv"

        csv_file_basename = os.path.basename(csv_file_name)

        try:
            with open(csv_file_name, mode='w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                header = ["channels"]
                for cycle_number in selected_cycles_list:
                    temp = "x_{cycle},y_{cycle},charge_{cycle},discharge_{cycle},average_voltage_{cycle}".format(cycle=cycle_number)
                    header += temp.split(",")

                csv_writer.writerow(header)
                for channel_number in selected_channels_list:
                    csv_writer.writerow([str(channel_number)])

            self.task_bar_message.emit("green", "Successfully written to {}".format(csv_file_basename))

        except PermissionError:
            self.task_bar_message.emit("red", "Do not have permission to open file. {} may be in use.".format(csv_file_basename))

    @pyqtSlot(str)
    def file_name_changed(self, name, file_type):
        # TODO: Validate if the file
        valid = False
        if file_type == "medusa":
            data, valid = self.validate_medusa_file(name, file_type)
        elif file_type == "mass":
            data, valid = self.validate_mass_file(name, file_type)
        elif file_type == "x_y":
            data, valid = self.validate_x_y_file(name, file_type)
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

    def validate_x_y_file(self, name, file_type):
        columns = {'channel', 'x', 'y'}
        try:
            data = pd.read_csv(name, nrows=64)
            diff = columns.difference(set(data.columns.values))
            if bool(diff):
                message = "Error: Invalidate {} file format. Heading not found: {}".format(
                    file_type,
                    ",".join(diff))
                self.task_bar_message.emit("red", message)
                return [], False
            else:
                x_count = data['x'].count()
                y_count = data['y'].count()
                channel_count = data['channel'].count()
                if x_count == 64 and y_count == 64 and channel_count == 64 and data.isnull().sum().sum() == 0:
                    data = data.set_index('channel')
                    return data, True
                else:
                    message = "Error: Invalidate {} file format. There should be 64 channels, 64 x values and 64 y values".format(
                        file_type,
                        ",".join(diff))
                    self.task_bar_message.emit("red", message)
                    return [], False

        except Exception as error:
            message = "Error: Invalidate {} file format. {}".format(file_type, error)
            self.task_bar_message.emit("red", message)
            return [], False


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