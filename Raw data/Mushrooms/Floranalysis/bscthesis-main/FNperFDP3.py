# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 10:47:27 2022

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
pad='C:\\Users\\Helmendach\\Documents\\Wageningen Moleculair\\3e jaar\\Thesis@PCC\\Data\\Representatieve curves\\FN loops\\P3\\'
lijst=glob.glob(r"C:\Users\Helmendach\Documents\Wageningen Moleculair\3e jaar\Thesis@PCC\Data\Representatieve curves\FN loops\P3\*")
frames={naam: pd.read_csv(naam) for naam in lijst if int(naam.split('_')[-1][:-4])%4==3}
baselined={naam: zk.baseline( frames[naam] ) for naam in frames}
geknipt={naam: zk.schaar(baselined[naam])for naam in baselined}
geflipt={naam: zk.flip(geknipt[naam]) for naam in geknipt}
metstress= {naam: zk.calcstress(geflipt[naam], 80) for naam in geflipt}
metstrain={naam: zk.calcstrain(metstress[naam]) for naam in metstress}
fit={naam: zk.weibull(metstrain[naam]) for naam in metstrain}

Pdrie={pad+'Eco_P3_FN1.0_v_onespeed_Interval_7.csv':{'grens':8.5},
       pad+'Eco_P3_FN1.1_v_onespeed_Interval_7.csv':{'grens':9.1},
       pad+'Eco_P3_FN10_v_onespeed_Interval_7.csv':{'grens':9.2},
       pad+'Eco_P3_FN2_v_onespeed_Interval_7.csv':{'grens':9.4},
       pad+'Eco_P3_FN4_v_onespeed_Interval_7.csv':{'grens':9.3},
       pad+'Eco_P3_FN6_v_onespeed_Interval_7.csv':{'grens':9.6},
       pad+'Eco_P3_FN8_v_onespeed_Interval_7.csv':{'grens':8.5}
       }

knipfit={naam: zk.weibfit(fit[naam], output='pars', **Pdrie[naam]) for naam in fit}
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

plotargs={
    pad+'Eco_P3_FN1.0_v_onespeed_Interval_7.csv':{'c' : cmap(0), 'label':'1.0 N',  'marker':'o', 'mfc':'w', 'mec':'k', 'markersize':8},                                                                                                                                                                 
    pad+'Eco_P3_FN1.1_v_onespeed_Interval_7.csv':{'c' : cmap(0.1),'label':' 1.1 N', 'marker':'^', 'mfc':'w', 'mec':'k', 'markersize':8},
    pad+'Eco_P3_FN10_v_onespeed_Interval_7.csv':{'c': cmap(0.99),'label':'10 N'},
    pad+'Eco_P3_FN2_v_onespeed_Interval_7.csv':{'c': cmap(0.25),'label':'2 N', 'marker':'s', 'mfc':'w', 'mec':'k', 'markersize':8},
    pad+'Eco_P3_FN4_v_onespeed_Interval_7.csv' : {'c':cmap(0.4),'label':'4 N'},
    pad+'Eco_P3_FN6_v_onespeed_Interval_7.csv':  {'c':cmap(0.6),'label':'6 N'},
    pad+'Eco_P3_FN8_v_onespeed_Interval_7.csv':  {'c':cmap(0.8), 'label':'8 N', 'marker':'P', 'mfc':'w', 'mec':'k', 'markersize':8},
    }
plotargs2={
    pad+'Eco_P3_FN1.0_v_onespeed_Interval_7.csv':{'c' : cmap(0), 'label':'1.0 N'},                                                                                                                                                                 
    pad+'Eco_P3_FN1.1_v_onespeed_Interval_7.csv':{'c' : cmap(0.1),'label':' 1.1 N'},
    pad+'Eco_P3_FN10_v_onespeed_Interval_7.csv':{'c': cmap(0.99),'label':'10 N'},
    pad+'Eco_P3_FN2_v_onespeed_Interval_7.csv':{'c': cmap(0.3),'label':'2 N'},
    pad+'Eco_P3_FN4_v_onespeed_Interval_7.csv' : {'c':cmap(0.4),'label':'4 N'},
    pad+'Eco_P3_FN6_v_onespeed_Interval_7.csv':  {'c':cmap(0.6),'label':'6 N'},
    pad+'Eco_P3_FN8_v_onespeed_Interval_7.csv':  {'c':cmap(0.8), 'label':'8 N'},
    }
fig, ax =pp.subplots()
ax.set_title('P3')
ax.set_ylabel('Stress (Pa)')
ax.set_xlabel('Strain')
ax.locator_params(axis='x', nbins=5)
ax.locator_params(axis='y', nbins=5)
[ax.scatter(metstrain[naam]['strain'], metstrain[naam]['stress'], s=0.7, **plotargs2[naam]) for naam in metstrain if (float(naam.split('_')[2][2:])==1.1)|(float(naam.split('_')[2][2:])==1.0)|(float(naam.split('_')[2][2:])==2)|(float(naam.split('_')[2][2:])==8)]
[ax.plot(rang, theoretisch[naam], markevery=10, **plotargs[naam]) for naam in theoretisch if (float(naam.split('_')[2][2:])==1.1)|(float(naam.split('_')[2][2:])==1.0)|(float(naam.split('_')[2][2:])==2)|(float(naam.split('_')[2][2:])==8)]
#maakt colorbar
norm = mp.colors.Normalize(vmin=0.0, vmax=10)
sm = pp.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) 
cbar=pp.colorbar(sm, ticks=[10, 8, 6, 4, 2, 0], label='Preload (N)')
for t in cbar.ax.get_yticklabels():
     t.set_fontsize(20)
     
legend_lines=[

            Line2D([0],[0],color='0.2', lw=1.0, marker='o', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='^', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='s', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='P', mfc='None', ms=8)
            ]
ax.legend(legend_lines, [1.0, 1.1, 2, 8])
pp.show()