from PyQt5.QtCore import QObject, pyqtSlot
import pandas as pd
import csv
import matplotlib.pyplot as plt

class MainController(QObject):
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

    def plot_volt_cur(self):
        data = self._model.file_data
        cycle1_data = data[data['Cycle']==1]
        cycle2_data = data[data['Cycle']==2]
        voltage_cycle_1 = cycle1_data.loc[:,'Vavg (V)'].values
        current_cycle_1 = cycle1_data.loc[:,'Ch.1-I (uA)'].values
        voltage_cycle_2 = cycle2_data.loc[:,'Vavg (V)'].values
        current_cycle_2 = cycle2_data.loc[:,'Ch.1-I (uA)'].values
        plt.figure(1)
        ax = plt.subplot(111)
        chargePlot = ax.plot(voltage_cycle_1, current_cycle_1, 'b', linewidth = 2.0, label = 'Charge')
        dischargePlot = ax.plot(voltage_cycle_2, current_cycle_2, 'r', linewidth = 2.0, label = 'Discharge')
        # Positions the legend to the top right corner outside the plot

        f = self.zoom_factory(ax, base_scale=1)
        plt.show()
        plt.close()

    @pyqtSlot(str)
    def file_name_changed(self, name, file_type):
        # TODO: Validate if the file

        # load in pandas
        # name = "C:/Users/Sumbal/Documents/atom/data-analysis/matthew/KP0182A.csv"
        # data = pd.read_csv(name, skiprows=7)
        # self._model.file_data = data
        #
        # resistances_header = pd.read_csv(name, header=6, nrows=0)
        # resistances_values = pd.read_csv(name, skiprows=4, nrows=1)
        # self._model.resistances = resistances_values
        # update model

        # update model
        self._model.file_name = (name, file_type)


    def test_plot(self, data):
        cycle1 = data[data['Cycle']==1]
        ch1_cycle1 = cycle1[['Ch.1-I (uA)']]
        time_cycle1 = cycle1[['Time(h)']]

        cycle2 = data[data['Cycle']==2]
        ch1_cycle2 = cycle1[['Ch.1-I (uA)']]
        time_cycle2 = cycle1[['Time(h)']]

        charge = []
        discharge = []
        for i in range(0, len(ch1_cycle1) - 2, 2):
            charge.append(0.5*(ch1_cycle1.iloc[i,0] + ch1_cycle1.iloc[i+1, 0]) * (time_cycle1.iloc[i+1,0] - time_cycle1.iloc[i,0]))


        for i in range(0, len(ch1_cycle2) - 2, 2):
            discharge.append(0.5*(ch1_cycle2.iloc[i,0] + ch1_cycle2.iloc[i+1, 0]) * (time_cycle2.iloc[i+1,0] - time_cycle2.iloc[i,0]))

        print(discharge)

        plt.plot(charge,'x')
        plt.show()
        plt.plot(discharge,'o')
        plt.show()