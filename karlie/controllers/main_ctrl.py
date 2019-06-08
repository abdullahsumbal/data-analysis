from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import matplotlib.pyplot as plt
from controllers.helper import *

class MainController(QObject):
    task_bar_message = pyqtSignal(str ,str)
    def __init__(self, model):
        super().__init__()

        self._model = model

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

    # plot normalized current vs voltage
    def plot_norm_volt_cur(self, selected_cycles, selected_channels):

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
            selected_channels = [i for i in range(1, 65)]
            plt.figure(1)
            channel_number = 1
            for row in range(8):
                for col in range(8):
                    for cycle in selected_cycles_list:
                        # get selected cycle data
                        cycle_data = data[data['Cycle'] == cycle]
                        # get voltage
                        voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
                        # get current
                        current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].values

                        # make subplot
                        plt.subplot(8, 8, channel_number)

                        plt.plot(voltage_cycle, current_cycle, 'b', linewidth=2.0, label='Charge')

                    # increment figure number for new plots.
                    channel_number += 1
            plt.show()
            plt.close()
        else:
            selected_channels = [int(selected_channels.strip())]

            for channel_number in selected_channels:
                for cycle in selected_cycles_list:
                    # get selected cycle data
                    cycle_data = data[data['Cycle'] == cycle]
                    # get voltage
                    voltage_cycle = cycle_data.loc[:, 'Vavg (V)'].values
                    # get current
                    current_cycle = cycle_data.loc[:, 'Ch.{}-I (uA)'.format(channel_number)].values
                    plt.plot(voltage_cycle, current_cycle, 'b', linewidth=2.0, label='Charge')
            plt.show()
            plt.close()

    @pyqtSlot(str)
    def file_name_changed(self, name, file_type):
        # TODO: Validate if the file
        data, status = validate_medusa_file(name)
        # resistances_header = pd.read_csv(name, header=6, nrows=0)
        # resistances_values = pd.read_csv(name, skiprows=4, nrows=1)
        # self._model.resistances = resistances_values


        # update model
        if status:
            self._model.file_name = (name, data, file_type)
        else:
            self.task_bar_message.emit("red", "Error: Invalidate {} file format".format(file_type))

    def get_unique_cycles(self, data):
        return data.Cycle.unique()

    def get_all_cycles(self):
        return self._model.medusa_data.Cycle.unique()