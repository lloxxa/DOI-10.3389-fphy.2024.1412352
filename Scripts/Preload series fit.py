# -*- coding: utf-8 -*-
"""
Preload series analysis
-----------------------
This script was written to analyze data obtained in an experiment where measurements were taken at different preloads for three different samples on our aritfical suction cup arrays.


This script accepts a folder of CSV files containing one representative curve for each preload.
It will plot the force-distance curves for each preload as well as a model of the curve based on the fiber bundle model using the Weibull distribution.
The fit parameter 'grens' is given for each individual file in a dictionary. Three dictionaries are contained in this file, one for each sample. (limits2 for P2.5, limits3 for P3 and limits4 for P4).
Three dictionaries containing the plot arguments for each curve are also contained in the file. Choose the appropriate one for each sample.
Note that the legend must be manually changed when visualizing different samples. 

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
pad=r'C:\Users\Helmendach\Documents\GitHub\bscthesis\Representative curves\Preload series\P3'
lijst=glob.glob(pad+'\*')
frames={naam: pd.read_csv(naam) for naam in lijst if int(naam.split('_')[-1][:-4])%4==3}
baselined={naam: zk.baseline( frames[naam] ) for naam in frames}
geknipt={naam: zk.schaar(baselined[naam])for naam in baselined}
#multiplies data by -1, calculates strain
geflipt={naam: zk.flip(geknipt[naam]) for naam in geknipt}
metstrain={naam: zk.calcstrain(geflipt[naam]) for naam in geflipt}
#fits data using Weibull dsitribution
fit={naam: zk.weibull(metstrain[naam]) for naam in metstrain}
#Dictionaries contain manually found limits (grens) from where the data will be fit
#dict with limits for dataset with a periodicity of 3mm, labelled P3
limits3={pad+'Eco_P3_FN1.0_v_onespeed_Interval_7.csv':{'grens':0.2},
       pad+'Eco_P3_FN1.1_v_onespeed_Interval_7.csv':{'grens':1.2},
       pad+'Eco_P3_FN10_v_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P3_FN2_v_onespeed_Interval_7.csv':{'grens':1.37},
       pad+'Eco_P3_FN4_v_onespeed_Interval_7.csv':{'grens':1.37},
       pad+'Eco_P3_FN6_v_onespeed_Interval_7.csv':{'grens':1.25},
       pad+'Eco_P3_FN8_v_onespeed_Interval_7.csv':{'grens':1.25}
       }
#dict with limits for datasets with a periodicity of 2.5mm, labelled P2.5
limits2={pad+'Eco_P2.5_FN0.5_v_onespeed_Interval_15.csv':{'grens':0.3},
       pad+'Eco_P2.5_FN0.7_v_onespeed_Interval_31.csv':{'grens':0.6},
       pad+'Eco_P2.5_FN1.0_v_onespeed_Interval_7.csv':{'grens':0.75},
       pad+'Eco_P2.5_FN2.0_v_onespeed_Interval_7.csv':{'grens':1.3},
       pad+'Eco_P2.5_FN4.0_v_onespeed_Interval_7.csv':{'grens':1.65},
       pad+'Eco_P2.5_FN6.0_v_onespeed_Interval_7.csv':{'grens':1.65},
       pad+'Eco_P2.5_FN8.0_v_onespeed_Interval_7.csv':{'grens':1.65},
       pad+'Eco_P2.5_FN10_v_onespeed_Interval_7.csv':{'grens':1.65}
       }
#dict with limits for datasets with a periodicity of 4mm, labelled P4
limits4={r'C:\Users\Helmendach\Documents\Wageningen Moleculair\3e jaar\Thesis@PCC\Data\Representatieve curves\FN loops\P4\Eco_P4_FN0.1_v_newsample_onespeed_Interval_7.csv':{'grens':0},
       pad+'Eco_P4_FN0.2_v_newsample_onespeed_Interval_7.csv':{'grens':0.25},
       pad+'Eco_P4_FN0.3_v_newsample_onespeed_Interval_7.csv':{'grens':0.3},
       pad+'Eco_P4_FN1_v_newsample_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN2_v_newsample_onespeed_Interval_7.csv':{'grens':1.4},
       pad+'Eco_P4_FN4_v_newsample_onespeed_Interval_7.csv':{'grens':1.15},
       pad+'Eco_P4_FN5.2_v_newsample_onespeed_Interval_7.csv':{'grens':1.1},
       pad+'Eco_P4_FN5_v_newsample_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN6_v_newsample_onespeed_Interval_7.csv':{'grens':1}
       }

#fits data and makes a dict with the fit data for each curve.
knipfit={naam: zk.weibfit(fit[naam], output='pars', **limits3[naam]) for naam in fit}
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
#makes colormap
cmap=pp.get_cmap('plasma_r')
#Dict with plot arguments per file
#Dict with plot arguments for datasets with a periodicity of 3mm, labelled P3
plotargs3={
    pad+'Eco_P3_FN1.0_v_onespeed_Interval_7.csv':{'c' : cmap(0), 'label':'1.0 N'},                                                                                                                                                                 
    pad+'Eco_P3_FN1.1_v_onespeed_Interval_7.csv':{'c' : cmap(0.1),'label':' 1.1 N'},
    pad+'Eco_P3_FN10_v_onespeed_Interval_7.csv':{'c': cmap(0.99),'label':'10 N'},
    pad+'Eco_P3_FN2_v_onespeed_Interval_7.csv':{'c': cmap(0.3),'label':'2 N'},
    pad+'Eco_P3_FN4_v_onespeed_Interval_7.csv' : {'c':cmap(0.4),'label':'4 N'},
    pad+'Eco_P3_FN6_v_onespeed_Interval_7.csv':  {'c':cmap(0.6),'label':'6 N'},
    pad+'Eco_P3_FN8_v_onespeed_Interval_7.csv':  {'c':cmap(0.8), 'label':'8 N'},
    }
#Dict with plot arguments for datasets with a periodicity of 2.5mm, labelled P2.5
plotargs2={
    pad+'Eco_P2.5_FN0.5_v_onespeed_Interval_15.csv':{'c' : cmap(0)},
           pad+'Eco_P2.5_FN0.7_v_onespeed_Interval_31.csv':{'c' : cmap(0.1)},
           pad+'Eco_P2.5_FN1.0_v_onespeed_Interval_7.csv':{'c' : cmap(0.25)},
           pad+'Eco_P2.5_FN2.0_v_onespeed_Interval_7.csv':{'c' : cmap(0.35)},
           pad+'Eco_P2.5_FN4.0_v_onespeed_Interval_7.csv':{'c' : cmap(0.5)},
           pad+'Eco_P2.5_FN6.0_v_onespeed_Interval_7.csv':{'c' : cmap(0.7)},
           pad+'Eco_P2.5_FN8.0_v_onespeed_Interval_7.csv':{'c' : cmap(0.9)},
           pad+'Eco_P2.5_FN10_v_onespeed_Interval_7.csv':{'c' : cmap(0.99)},
           }
#Dict with plot arguments for datasets with a periodicity of 4mm, labelled P4
plotargs4={pad+'Eco_P4_FN0.1_v_newsample_onespeed_Interval_7.csv':{'c' : cmap(0)},
       pad+'Eco_P4_FN0.2_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.1)},
       pad+'Eco_P4_FN0.3_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.2)},
       pad+'Eco_P4_FN1_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.3)},
       pad+'Eco_P4_FN2_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.45)},
       pad+'Eco_P4_FN4_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.6)},
       pad+'Eco_P4_FN5.2_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.75)},
       pad+'Eco_P4_FN5_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.8)},
       pad+'Eco_P4_FN6_v_newsample_onespeed_Interval_7.csv':{'c': cmap(0.99)},
       }

fig, ax =pp.subplots()
ax.set_ylabel('Normal Force (N)')
ax.set_xlabel('Strain')
ax.locator_params(axis='x', nbins=5)
ax.locator_params(axis='y', nbins=5)
#Plots both original data and fit. dict comprehension is used to include/exclude some files
[ax.scatter(metstrain[naam]['strain'], metstrain[naam]['normalforce'], s=0.7, **plotargs3[naam]) for naam in metstrain if (float(naam.split('_')[2][2:])==1.1)|(float(naam.split('_')[2][2:])==1.0)|(float(naam.split('_')[2][2:])==2)|(float(naam.split('_')[2][2:])==8)]
[ax.plot(rang, theoretisch[naam], **plotargs3[naam]) for naam in theoretisch if (float(naam.split('_')[2][2:])==1.1)|(float(naam.split('_')[2][2:])==1.0)|(float(naam.split('_')[2][2:])==2)|(float(naam.split('_')[2][2:])==8)]
#Makes colorbar
norm = mp.colors.Normalize(vmin=0.0, vmax=10)
sm = pp.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) 
cbar=pp.colorbar(sm, ticks=[10, 8, 6, 4, 2, 0], label='Preload (N)')
for t in cbar.ax.get_yticklabels():
     t.set_fontsize(20)
#makes legend, chnage the number of lines and colors depending on the included curves and used dataset     
legend_lines=[

            Line2D([0],[0],color=cmap(0), lw=1.0),
            Line2D([0],[0],color=cmap(0.1), lw=1.0),
            Line2D([0],[0],color=cmap(0.25), lw=1.0),
            Line2D([0],[0],color=cmap(0.8), lw=1.0)
            ]
#Makes legend labels, change this depending on included curves and used dataset
ax.legend(legend_lines, ['1.0 N', '1.1 N', '2 N', '8 N'])
pp.show()