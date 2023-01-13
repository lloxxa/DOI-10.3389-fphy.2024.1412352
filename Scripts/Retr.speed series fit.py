# -*- coding: utf-8 -*-
"""
Retraction speed series analysis
-----------------------
This script was written to analyze data obtained in an experiment where measurements were taken at different retraction speeds for three different samples of our aritfical suction cup arrays.


This script accepts a folder of CSV files containing one representative curve for each retraction speed.
It will plot the force-distance curves for each retraction speed as well as a model of the curve based on the fiber bundle model using the Weibull distribution.
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
pad=''
lijst=glob.glob(pad+'\*')
frames={naam: pd.read_csv(naam) for naam in lijst if int(naam.split('_')[-1][:-4])%4==3}
baselined={naam: zk.baseline( frames[naam] ) for naam in frames}
geknipt={naam: zk.schaar(baselined[naam],0, 0.01)for naam in baselined}
#multiplies data by -1, calculates strain
geflipt={naam: zk.flip(geknipt[naam]) for naam in geknipt}
metstrain={naam: zk.calcstrain(geflipt[naam]) for naam in geflipt}
#fits data using Weibull dsitribution
fit={naam: zk.weibull(metstrain[naam]) for naam in metstrain}
#Dictionaries contain manually found limits (grens) from where the data will be fit
#dict with limits for dataset with a periodicity of 3mm, labelled P3
Pdrie={pad+'Eco_P3_FN4_v_retrSpd10_onespeed_Interval_7.csv':{'grens':0.8},
       pad+'Eco_P3_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'grens':1.8},
       pad+'Eco_P3_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P3_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'grens':2},
       pad+'Eco_P3_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'grens':1.4},
       pad+'Eco_P3_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'grens':1.7},
       pad+'Eco_P3_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P3_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P3_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P3_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P3_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P3_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'grens':1.5}
       }
#dict with limits for dataset with a periodicity of 2.5mm, labelled P2.5
Ptwee={pad+'Eco_P2_5_FN4_v_retrSpd10_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P2_5_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'grens':1.8},
       pad+'Eco_P2_5_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P2_5_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'grens':1.8},
       pad+'Eco_P2_5_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'grens':2},
       pad+'Eco_P2_5_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'grens':2},
       pad+'Eco_P2_5_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'grens':1.7},
       pad+'Eco_P2_5_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'grens':1.7},
       pad+'Eco_P2_5_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P2_5_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P2_5_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'grens':1.7},
       pad+'Eco_P2_5_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'grens':1.8}
       }
#dict with limits for dataset with a periodicity of 4mm, labelled P4
Pvier={pad+'Eco_P4_FN4_v_retrSpd10_onespeed_Interval_7.csv':{'grens':0.8},
       pad+'Eco_P4_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'grens':1.2},
       pad+'Eco_P4_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'grens':1.5},
       pad+'Eco_P4_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'grens':1.3},
       pad+'Eco_P4_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'grens':1.2},
       pad+'Eco_P4_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'grens':1},
       pad+'Eco_P4_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'grens':1}
       }
#fits data and makes a dict with the fit data for each curve.
knipfit={naam: zk.weibfit(fit[naam], output='pars', **Pdrie[naam]) for naam in fit}
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
cmap=pp.get_cmap('viridis_r')
#Dict with plot arguments per file
#Dict with plot arguments for datasets with a periodicity of 3mm, labelled P3
plotargs3={pad+'Eco_P3_FN4_v_retrSpd10_onespeed_Interval_7.csv': {'c' : cmap(0.01),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'c' : cmap(0.1),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'c' : cmap(0.15),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'c' : cmap(0.2),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'c' : cmap(0.3),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'c' : cmap(0.35),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'c' : cmap(0.4),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'c' : cmap(0.5),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'c' : cmap(0.65),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'c' : cmap(0.8),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'c' : cmap(0.9),'label':' 1.1 N'},
       pad+'Eco_P3_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'c' : cmap(0.99),'label':' 1.1 N'},
       }
#Dict with plot arguments for datasets with a periodicity of 2.5mm, labelled P2.5
plotargs2={pad+'Eco_P2_5_FN4_v_retrSpd10_onespeed_Interval_7.csv':{'c' : cmap(0.01),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'c' : cmap(0.1),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'c' : cmap(0.15),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'c' : cmap(0.2),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'c' : cmap(0.3),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'c' : cmap(0.35),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'c' : cmap(0.4),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'c' : cmap(0.5),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'c' : cmap(0.65),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'c' : cmap(0.8),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'c' : cmap(0.9),'label':' 1.1 N'},
       pad+'Eco_P2_5_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'c' : cmap(0.99),'label':' 1.1 N'}
       }
#Dict with plot arguments for datasets with a periodicity of 4mm, labelled P4
plotargs4={pad+'Eco_P4_FN4_v_retrSpd10_onespeed_Interval_7.csv': {'c' : cmap(0.01),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'c' : cmap(0.1),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'c' : cmap(0.15),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'c' : cmap(0.2),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'c' : cmap(0.3),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'c' : cmap(0.35),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'c' : cmap(0.4),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'c' : cmap(0.5),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'c' : cmap(0.65),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'c' : cmap(0.8),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'c' : cmap(0.9),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'c' : cmap(0.99),'label':' 1.1 N'},
       }

fig, ax =pp.subplots()
ax.set_ylabel('Normal Force (N)')
ax.set_xlabel('Strain')
ax.locator_params(axis='x', nbins=5)
ax.locator_params(axis='y', nbins=5)
#Plots both original data and fit. dict comprehension is used to include/exclude some files
[ax.scatter(metstrain[naam]['strain'], metstrain[naam]['normalforce'], s=0.7, **plotargs3[naam]) for naam in metstrain if (float(naam.split('_')[4][7:])==10)|(float(naam.split('_')[4][7:])==200)|(float(naam.split('_')[4][7:])==2500)]
[ax.plot(rang, theoretisch[naam], **plotargs3[naam]) for naam in theoretisch if (float(naam.split('_')[4][7:])==10)|(float(naam.split('_')[4][7:])==200)|(float(naam.split('_')[4][7:])==2500)]
#makes colorbar
norm = mp.colors.Normalize(vmin=0.0, vmax=3000)
sm = pp.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) 
cbar=pp.colorbar(sm, ticks=[3000, 2000, 1000, 0], label='Retraction speed (µm/s)')
for t in cbar.ax.get_yticklabels():
     t.set_fontsize(20)
#makes legend, chnage the number of lines and colors depending on the included curves and used dataset          
legend_lines=[

            Line2D([0],[0],color=cmap(0.01), lw=1.0),
            Line2D([0],[0],color=cmap(0.3), lw=1.0),
            Line2D([0],[0],color=cmap(0.9), lw=1.0),
            ]
ax.legend(legend_lines, ['10 µm/s', '200 µm/s', '2500 µm/s'])
pp.show()
