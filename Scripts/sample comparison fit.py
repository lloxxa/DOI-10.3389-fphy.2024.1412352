# -*- coding: utf-8 -*-
"""
Sample comparison
-----------------
This script was written to compare measurements obtained on different samples, e.g. the three samples with varying feature densities. 


This script accepts a folder of CSV files containing one representative curve for each sample to be considered.
It will plot the force-distance curves for each sample as well as a model of the curve based on the fiber bundle model using the Weibull distribution.
The fit parameter 'grens' is given for each individual file in a dictionary, as well as the plot arguments. 
The script is currently configured for comparing the three samples with different feature densities, but it can also be used for the backing layer experiments. 

Requirements
------------
Zeekat
pandas
glob
matplotlib
matplotlib.pyplot
numpy
matplotlib.lines.Line2D
"""

import zeekat as zk
import pandas as pd
import glob
import matplotlib.pyplot as pp
import numpy as np
import matplotlib as mp 
from matplotlib.lines import Line2D  

#Isolates relevant data
pad='C:\\Users\\Helmendach\\Documents\\Wageningen Moleculair\\3e jaar\\Thesis@PCC\\Data\\Representatieve curves\\Feature density\\'
lijst=glob.glob(pad+'\*')
frames={naam: pd.read_csv(naam) for naam in lijst if int(naam.split('_')[-1][:-4])%4==3}
baselined={naam: zk.baseline( frames[naam] ) for naam in frames}
geknipt={naam: zk.schaar(baselined[naam])for naam in baselined}
#multiplies data by -1, calculates strain
geflipt={naam: zk.flip(geknipt[naam]) for naam in geknipt}
metstrain={naam: zk.calcstrain(geflipt[naam]) for naam in geflipt}
fit={naam: zk.weibull(metstrain[naam]) for naam in metstrain}

#Dictionary contains manually found limits (grens) from where the data will be fit
Pfd={pad+'Eco_P2.5_FN4_v_onespeed_Interval_7.csv':{'grens':1.65},
       pad+'Eco_P3_FN4_v_onespeed_Interval_7.csv':{'grens':1.37},
       pad+'Eco_P4_FN4_v_newsample_onespeed_Interval_7.csv':{'grens':1.15},
       }
#fits data and makes a dict with the fit data for each curve.
knipfit={naam: zk.weibfit(fit[naam], output='pars', **Pfd[naam]) for naam in fit}
rang=np.arange(0,1,0.01)
theoretisch={naam: zk.tbull(rang, knipfit[naam]) for naam in knipfit}
#configures plotting parameters
config={'xtick.top':True,
'ytick.right':True,
'xtick.direction':'in',
'ytick.direction':'in',
'xtick.major.size':9,
'ytick.major.size':9,
'xtick.minor.visible':True,
'ytick.minor.visible':True,
'legend.frameon':False,
'legend.fontsize':18,
'font.size':20,
}

mp.rcParams.update(**config)
#Defines colormap
cmap=pp.get_cmap('winter_r')

#Dict with colors from the colormap to be used for each curve
plotargs={pad+'Eco_P2.5_FN4_v_onespeed_Interval_7.csv':{'c' : cmap(0.2)},
       pad+'Eco_P3_FN4_v_onespeed_Interval_7.csv':{'c' : cmap(0.6)},
       pad+'Eco_P4_FN4_v_newsample_onespeed_Interval_7.csv':{'c' : cmap(0.99)},
       }

fig, ax =pp.subplots()
ax.set_title('')
ax.set_ylabel('Normal Force (N)')
ax.set_xlabel('Strain')
ax.locator_params(axis='x', nbins=5)
ax.locator_params(axis='y', nbins=5)
[ax.scatter(metstrain[naam]['strain'], metstrain[naam]['normalforce'], s=0.7, **plotargs[naam]) for naam in metstrain]
[ax.plot(rang, theoretisch[naam], **plotargs[naam]) for naam in theoretisch]
#makes colorbar
norm = mp.colors.Normalize(vmin=2.0, vmax=4.0)
sm = pp.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) 
cbar=pp.colorbar(sm, ticks=[4,3,2], label='Distance between features (mm)')
for t in cbar.ax.get_yticklabels():
     t.set_fontsize(20)
     
#Makes a legend
legend_lines=[

            Line2D([0],[0],color=cmap(0.2), lw=1.0),
            Line2D([0],[0],color=cmap(0.6), lw=1.0),
            Line2D([0],[0],color=cmap(0.99), lw=1.0),
            ]
ax.legend(legend_lines, ['2.5 mm', '3 mm', '4 mm'])
pp.show()
