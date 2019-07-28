# from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator, MaxNLocator
# from controllers.helper import *
import pandas as pd
import numpy as np
# import csv
# # import os
# # import json
import matplotlib.pyplot as plt
from impedance.plotting import plot_nyquist

from impedance.circuits import Randles, CustomCircuit

import matplotlib
matplotlib.use( 'tkagg' )

randles = Randles(initial_guess=[.01, .005, .1, .001, 200])
randlesCPE = Randles(initial_guess=[.01, .005, .1, .9, .001, 200], CPE=True)

customCircuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200],
                              circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-W_1')
def set_labels(ax, x_label, y_label, channel_number, config):
    # show axis only on the left and bottom
    # there are more than one plot
    # y axis label on channel 3 plot
    if channel_number == 4:
        ax.set_ylabel(y_label, **config)
        ax.set_xticklabels([])
    #  x axis label on channel
    elif channel_number == 32:
        ax.set_xlabel(x_label, **config)
        ax.set_yticklabels([])
    # only y axis label
    elif channel_number in range(0, 8):
        ax.set_xticklabels([])
    # only show x axis label
    elif channel_number in [16, 24, 32, 40, 48, 56, 64]:
        ax.set_yticklabels([])
    # everything else no label
    elif channel_number != 8:
        ax.set_yticklabels([])
        ax.set_xticklabels([])

data = pd.read_csv('impcombi64(1-64).csv')

zero_index = data.index[data['freq/Hz'] == 1000000].tolist()
number_of_rows = data.shape[0]
cycle_number = 0
cycle_data = []
for index in range(number_of_rows):
    if index in zero_index:
        cycle_number += 1
    cycle_data.append(cycle_number)

data['Channel'] = cycle_data

print(data)

fig, axs = plt.subplots(8, 8,  figsize=[15, 10])

for channel_index in range(64):
    ax = axs[channel_index % 8][int(channel_index / 8)]
    channel_number = channel_index + 1
    channel_data = data[data['Channel'] == channel_number]
    ax.scatter(channel_data.iloc[:35, 2], channel_data.iloc[0:35, 1], s=0.7)
    ax.ticklabel_format(style="sci", scilimits=(0,4))
    # plt.ticklabel_format(useOffset=False)
    ax.tick_params(labelsize=10)

    # ax.set_ylim(bottom=0, top=2500000)  # set the y-axis limits
    # ax.set_xlim(left=0, right=500000)  # set the x-axis limits
    set_labels(ax, 'Re(Z)/Ohm', '-Im(Z)/Ohm', channel_number, {})

plt.subplots_adjust(hspace=0.3, wspace=0.1)
plt.show()
# frequencies = data.iloc[0:58,0].values
# data['Z'] = data.iloc[0:58,1] + 1j*data.iloc[0:58,2]
# Z = data['Z'].values
#
# print(type(Z))
#
# # keep only the impedance data in the first quandrant
# frequencies = frequencies[np.imag(Z) < 0]
# Z = Z[np.imag(Z) < 0]
#
# randles.fit(frequencies, Z)
# randlesCPE.fit(frequencies, Z)
# customCircuit.fit(frequencies, Z)
#
# print(customCircuit)
#
#
# f_pred = np.logspace(5,-2)
#
# randles_fit = randles.predict(f_pred)
# randlesCPE_fit = randlesCPE.predict(f_pred)
# customCircuit_fit = customCircuit.predict(f_pred)
# fig, ax = plt.subplots(figsize=(5,5))
#
# plot_nyquist(ax, frequencies, Z)
# plot_nyquist(ax, f_pred, randles_fit, fmt='-')
# plot_nyquist(ax, f_pred, randlesCPE_fit, fmt='-')
# plot_nyquist(ax, f_pred, customCircuit_fit, fmt='-')
#
# plt.show()
#
