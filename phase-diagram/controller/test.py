import ternary
import matplotlib.pyplot as plt

# Creates a ternary set of axes to plot the diagram from python-ternary
figure, tax = ternary.figure(scale=1.0)
tax.boundary()
tax.gridlines(multiple=0.1, color='blue')
tax.ticks(axis = 'blr', linewidth = 1.0, multiple = 0.1, tick_formats = '%.1f', offset = 0.02)

plt.axis('off')
print(
    'Ternary plots generated using the python-ternary library\nMarc Harper et al. (2015). python-ternary: Ternary Plots in Python. Zenodo. 10.5281/zenodo.34938')
tax.show()