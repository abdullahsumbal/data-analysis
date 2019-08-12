import sys
import matplotlib.pyplot as plt
from impedance.circuits import Randles, CustomCircuit
import matplotlib
import pandas as pd
matplotlib.use("TkAgg")

randles = Randles(initial_guess=[.01, .005, .1, .001, 200])
randlesCPE = Randles(initial_guess=[.01, .005, .1, .9, .001, 200], CPE=True)


customCircuit = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200],
                              circuit='R_0-p(R_1,C_1)-p(R_1,C_1)-W_1')

print(randles)

import numpy as np

# data = np.genfromtxt('data2.csv', delimiter=',')
columns = ['freq/Hz', 'Re(Z)/Ohm', '-Im(Z)/Ohm']
data = pd.read_csv("test/test_01_1_C01.txt", sep="\t", usecols=columns)

frequencies = data["freq/Hz"].values
Z = data['Re(Z)/Ohm'].values - 1j*data['-Im(Z)/Ohm'].values

print(frequencies)
print(Z)

# keep only the impedance data in the first quandrant
frequencies = frequencies[np.imag(Z) < 0]
Z = Z[np.imag(Z) < 0]



randles.fit(frequencies, Z)
# randlesCPE.fit(frequencies, Z)
# customCircuit.fit(frequencies, Z)

# print(customCircuit)

import matplotlib.pyplot as plt
from impedance.plotting import plot_nyquist

f_pred = np.logspace(5,-2)

randles_fit = randles.predict(f_pred)
# randlesCPE_fit = randlesCPE.predict(f_pred)
# customCircuit_fit = customCircuit.predict(f_pred)

fig, ax = plt.subplots(figsize=(5,5))

plot_nyquist(ax, frequencies, Z)
plot_nyquist(ax, f_pred, randles_fit, fmt='-')
plt.show()
# plot_nyquist(ax, frequencies, Z)
# plot_nyquist(ax, f_pred, randlesCPE_fit, fmt='-')
# plt.show()
# plot_nyquist(ax, frequencies, Z)
# plot_nyquist(ax, f_pred, customCircuit_fit, fmt='-')
# plt.show()
# # plt.scatter(frequencies, Z)
#
# plt.show()

