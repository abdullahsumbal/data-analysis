import numpy    as np
import matplotlib.pyplot    as plt
from cycler import cycler
import matplotlib    as mpl
import pandas    as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import r2_score

# Get the data
df = pd.read_csv("test2ML_avgv.csv")
# [Optional]    Add    color    labels    to    the    data - 3rd parameter is number of labels
colors = plt.cm.tab20(np.linspace(0, 1, 8)[0:len(df.label.unique())])
color_dic = {label: color for label, color in zip(df.label.unique(), colors)}
df['color'] = df.label.map(color_dic)

### Machine Learning Fit
# Make a list of variables for machine learning
names = ('Lithium', 'Manganese')
variables = df.loc[:, names]
# Define a Pipeline that scales the data and applies the model
reg_avgv = Pipeline([('scl', StandardScaler()), ('clf', svm.SVR(kernel='rbf', gamma=0.8))])
# Fit the variables to the avgv
reg_avgv.fit(variables, df.avgv)

# get variables
from ternary.helpers import simplex_iterator

variables = []
for (i, j, k) in simplex_iterator(100):
    variables.append([i, j, k])

variables = np.array(variables) / 100

# print(variables.shape)
# Get the predicted average voltage from the model and save it to the DataFrame
pred = reg_avgv.predict(variables[:, 0:2])
# print(pred)

d = {}
for index in range(variables.shape[0]):
    d[(variables[index][0] * 100, variables[index][1] * 100)] = pred[index]

# print(d)
figure, tax = ternary.figure(scale=100)
tax.heatmap(d, style="h", use_rgba=False)
tax.boundary()
tax.gridlines(multiple=10, color="blue")
tax.ticks(axis='blr', linewidth=1.0, fontsize=10, multiple=10, offset=0.02)
tax.left_axis_label("1 - x - y", fontsize=12, offset=0.15)
tax.right_axis_label("y", fontsize=12, offset=0.15)
tax.bottom_axis_label("x", fontsize=12, offset=0.15)
plt.axis('off')
tax.set_title("Heatmap Test: Hexagonal")