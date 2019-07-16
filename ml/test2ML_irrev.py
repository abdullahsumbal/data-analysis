import numpy    as np
import matplotlib.pyplot    as plt
from cycler    import cycler
import matplotlib    as mpl
import pandas    as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing    import StandardScaler
from sklearn    import svm

#    Get    the    data
df = pd.read_csv("test2ML_irrev.csv")
#[Optional]    Add    color    labels    to    the    data - 3rd parameter is number of labels
colors    = plt.cm.tab20(np.linspace(0,    1,    4)[0:len(df.label.unique())])
color_dic    = {label:    color    for label,    color    in zip(df.label.unique(),    colors)}
df['color']    = df.label.map(color_dic)

###    Machine    Learning    Fit
#    Make    a    list    of    variables for    machine    learning
names    = ('Manganese',    'Nickel')
variables    = df.loc[:, names]
#    Define    a    Pipeline    that    scales    the    data    and    applies    the    model
reg_irrev = Pipeline([('scl',    StandardScaler()), ('clf',    svm.SVR(kernel='rbf', gamma=0.65))])
#    Fit    the    variables    to    the    PCE
reg_irrev.fit(variables, df.irrev)
#    Get    the    predicted average voltage from    the    model    and    save    it    to    the    DataFrame
df['irrev_pred_svm']    = reg_irrev.predict(variables)
#    Make    a    plot    of    the    real    values    vs    the    predicted
#    Increase    gamma    in    the    pipeline    until    the    data    just    starts    on    to    lay
#    on    the    line.    If    gamma    is    too    high    the    data    can    be    over    fit
fig, ax1    = plt.subplots(1,    1,    clear=True, num='irrev_pred', figsize=(5,    4))
ax1.set_title('Prediction vs Experimental')

for label,    data    in df.groupby('label'):
                plt.plot('irrev',    'irrev_pred_svm',    'o',    color=data['color'].iloc[0], data=data,    label=label)
plt.legend()
plt.autoscale(enable=True)
plt.plot([0, 100], [0, 100],    ls="--",    c=".3")
ax1.set_ylabel('Predicted Irreversible Capacity (%)')
ax1.set_xlabel('Measured Irreversible Capacity (%)')
plt.tight_layout()

#Now plot manganese vs lithium
fig, ax = plt.subplots(1,1)
x_len, y_len = 100, 100
xs = np.linspace(0, 1, x_len)
ys = np.linspace(0, 1, y_len)
xi, yi = names

xm, ym = np.meshgrid(xs, ys)
#vm  = v * np.ones_like(xm)
r    = np.c_[xm.flatten(), ym.flatten()]
#    Compute    the    values    from    the    fit
c    = reg_irrev.predict(r).reshape(x_len, y_len)
#    Make    a    contour    map

cmap  = ax.contour(xs,    ys,    c,    vmin=0,    vmax=7,    cmap='gray_r')
plt.clabel(cmap,    inline=1,    fontsize=10)
#    Make    a    value    map
pmap    = ax.pcolormesh(xs,    ys,    c,    shading='gouraud',  vmin=20,    vmax=45,    cmap='viridis')
#    Plot    the    experimental    points
ax.plot('Manganese',    'Nickel',    'o',    color=data['color'].iloc[0],
                                                                data=data.iloc[0],    mec='k',    mew=0.5,    label=label)
ax.set_ylabel(f'{yi}')
ax.set_xlabel(f'{xi}')
ax.set_title(f'Ternary to-be')
plt.tight_layout()
plt.colorbar(pmap,    ax=ax,    fraction=0.15)
plt.plot([0, 1], [1, 0],    ls="--", c='r')
plt.minorticks_on()
plt.tick_params(axis='both', which='both', grid_color='k', grid_alpha=0.15)
plt.grid(b=True, which='both', axis='both', linestyle='--')
plt.show()
