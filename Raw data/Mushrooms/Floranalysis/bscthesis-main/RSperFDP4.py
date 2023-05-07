# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 09:33:16 2022

@author: Helmendach
"""

import zeekat as zk
import pandas as pd
import glob
import matplotlib.pyplot as pp
import numpy as np
import warnings
import matplotlib as mp 
from matplotlib.lines import Line2D  
pad='C:\\Users\\Helmendach\\Documents\\Wageningen Moleculair\\3e jaar\\Thesis@PCC\\Data\\Representatieve curves\\Retraction speed\\P4\\'
lijst=glob.glob(r"C:\Users\Helmendach\Documents\Wageningen Moleculair\3e jaar\Thesis@PCC\Data\Representatieve curves\Retraction speed\P4\*")
frames={naam: pd.read_csv(naam) for naam in lijst if int(naam.split('_')[-1][:-4])%4==3}
baselined={naam: zk.baseline( frames[naam] ) for naam in frames}
geknipt={naam: zk.schaar(baselined[naam],0, 0.01)for naam in baselined}
geflipt={naam: zk.flip(geknipt[naam]) for naam in geknipt}
metstress= {naam: zk.calcstress(geflipt[naam], 42) for naam in geflipt}
metstrain={naam: zk.calcstrain(metstress[naam]) for naam in metstress}
fit={naam: zk.weibull(metstrain[naam]) for naam in metstrain}

Pvier={pad+'Eco_P4_FN4_v_retrSpd10_onespeed_Interval_7.csv':{'grens':9.0},
       pad+'Eco_P4_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'grens':9.3},
       pad+'Eco_P4_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'grens':9.6},
       pad+'Eco_P4_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'grens':9.3},
       pad+'Eco_P4_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'grens':9.1},
       pad+'Eco_P4_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'grens':9.4},
       pad+'Eco_P4_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'grens':9.2},
       pad+'Eco_P4_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'grens':9.3},
       pad+'Eco_P4_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'grens':9.2},
       pad+'Eco_P4_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'grens':9.0},
       pad+'Eco_P4_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'grens':9.0},
       pad+'Eco_P4_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'grens':9.0}
       }

knipfit={naam: zk.weibfit(fit[naam], output='pars', **Pvier[naam]) for naam in fit}
rang=np.arange(0,1,0.01)
theoretisch={naam: zk.tbull(rang, knipfit[naam]) for naam in knipfit}
#vanaf hier is alles voor het maken van 1 plot
#dict met parameters voor de plot en legenda
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
#maakt algemene pars van data in dict
mp.rcParams.update(**config)
#maakt kleurenmap 
cmap=pp.get_cmap('plasma_r')
#algemene deel van string naar filepath
plotargs={pad+'Eco_P4_FN4_v_retrSpd10_onespeed_Interval_7.csv': {'c' : cmap(0.01),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd30_onespeed_Interval_7.csv':{'c' : cmap(0.1),'label':' 1.1 N','marker':'o', 'mfc':'w', 'mec':'k', 'markersize':8},
       pad+'Eco_P4_FN4_v_retrSpd50_onespeed_Interval_7.csv':{'c' : cmap(0.15),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd100_onespeed_Interval_7.csv':{'c' : cmap(0.2),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd200_onespeed_Interval_7.csv':{'c' : cmap(0.3),'label':' 1.1 N',  'marker':'^', 'mfc':'w', 'mec':'k', 'markersize':8},
       pad+'Eco_P4_FN4_v_retrSpd300_onespeed_Interval_7.csv':{'c' : cmap(0.35),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd500_onespeed_Interval_7.csv':{'c' : cmap(0.4),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd1000_onespeed_Interval_7.csv':{'c' : cmap(0.5),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd1500_onespeed_Interval_7.csv':{'c' : cmap(0.65),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd2000_onespeed_Interval_7.csv':{'c' : cmap(0.8),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd2500_onespeed_Interval_7.csv':{'c' : cmap(0.9),'label':' 1.1 N'},
       pad+'Eco_P4_FN4_v_retrSpd3000_onespeed_Interval_7.csv':{'c' : cmap(0.99),'label':' 1.1 N', 'marker':'s', 'mfc':'w', 'mec':'k', 'markersize':8},
       }

plotargs2={pad+'Eco_P4_FN4_v_retrSpd10_onespeed_Interval_7.csv': {'c' : cmap(0.01),'label':' 1.1 N'},
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
ax.set_title('P4')
ax.set_ylabel('Stress (Pa)')
ax.set_xlabel('Strain')
ax.locator_params(axis='x', nbins=5)
ax.locator_params(axis='y', nbins=5)
[ax.scatter(metstrain[naam]['strain'], metstrain[naam]['stress'], s=0.7, **plotargs2[naam]) for naam in metstrain if (float(naam.split('_')[4][7:])==30)|(float(naam.split('_')[4][7:])==200)|(float(naam.split('_')[4][7:])==3000)]
[ax.plot(rang, theoretisch[naam], markevery=10, **plotargs[naam]) for naam in theoretisch if (float(naam.split('_')[4][7:])==30)|(float(naam.split('_')[4][7:])==200)|(float(naam.split('_')[4][7:])==3000)]
#maakt colorbar
norm = mp.colors.Normalize(vmin=0.0, vmax=3000)
sm = pp.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) 
cbar=pp.colorbar(sm, ticks=[3000, 2000, 1000, 0], label='Retraction speed (µm/s)')
for t in cbar.ax.get_yticklabels():
     t.set_fontsize(20)
     
legend_lines=[

            Line2D([0],[0],color='0.2', lw=1.0, marker='o', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='^', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='s', mfc='None', ms=8),
            ]
ax.legend(legend_lines, [30, 200, 3000])
pp.show()

#if (float(naam.split('_')[4][7:])==10)|(float(naam.split('_')[4][7:])==200)|(float(naam.split('_')[4][7:])==2500)