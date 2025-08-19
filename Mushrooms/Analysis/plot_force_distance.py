import pickle
import numpy as np
import pandas as pd
import plottools as pt
import matplotlib as mp
import matplotlib.cm as cm
import matplotlib.pyplot as pp
import matplotlib.colors as cs
from matplotlib.lines import Line2D
from matplotlib.ticker import AutoMinorLocator
from sklearn.linear_model import LinearRegression

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
'font.size':18
}

mp.rcParams.update(**config)

fig,[axs2,axs]=pp.subplots(1, 2, figsize=(12,4), sharey='all', sharex='all',)
gridspec_kw={'width_ratios': [0.8, 1]}

densities=['sample441.pickle', 'sample361.pickle', 'sample114.pickle']

clrs=pp.get_cmap("plasma")
clr=lambda n,mina,maxa: clrs(round(255* ( n / (maxa-mina))  ))
minf=4
maxf=50

#
#  density 441
#

sets_loaded={}
for p in densities:
    with open(p, 'rb') as f:
        sets_loaded[p]=pickle.load(f)

dfss={}
dfss[441]=sets_loaded['sample441.pickle']
dfss[361]=sets_loaded['sample361.pickle']
dfss[114]=sets_loaded['sample114.pickle']

preload_axs441={
        
            6:  {'ax':axs, 'plotargs':{   }         }, 
            12: {'ax':axs, 'plotargs':{}         },
            18: {'ax':axs, 'plotargs':{}         }, 
            24: {'ax':axs, 'plotargs':{}         },
            30: {'ax':axs, 'plotargs':{}         },  
            36: {'ax':axs, 'plotargs':{}         },
            42: {'ax':axs, 'plotargs':{}         }

       }

preload_axs361={
            #7.5: { 'plotargs':{'c':'b'}         }, 
            10: { 'ax':axs,  'plotargs':{}         },
            15: { 'ax':axs,  'plotargs':{}         }, 
            20: { 'ax':axs, 'plotargs':{}         },
            25: { 'ax':axs, 'plotargs':{}      },  
            30: { 'ax':axs, 'plotargs':{}         },
            35: { 'ax':axs, 'plotargs':{}         }
        }

preload_axs114={
            4:{ 'ax':axs, 'plotargs':{}         },
            #6: { 'ax':axs, 'plotargs':{}         }, 
            16: { 'ax':axs, 'plotargs':{}         },
        }

densities=  {114:preload_axs114, 361:preload_axs361, 441:preload_axs441}
marks=  {114:'o', 361:'^', 441:'s'}



# figure on the left ("axs2")
[axs2.plot(dfss[441][36]['intervals'][i]['data']['Gap'], dfss[441][36]['intervals'][i]['data']['Normal Force'],
    c=clr(36, minf, maxf), markevery=40, lw=0.8, mfc='None', ms=8, mec='0.2', mew=0.8, marker='s',)
    for i in range(5,30,5)]

axs2.set_ylim((-0.5,0.1))
axs2.legend([Line2D([0],[0],color='0.2', lw=1.0, marker='s', mfc='None', ms=8)],
        ['441\n$f_0$=36 N'], loc='center left', handletextpad=0.2)
axs2.set_xlabel('$d$ (mm)')
axs2.set_ylabel('$F$ (N)')
pt.annotate_xaxis(5.8, axs2, '$d_0$', lw=1, fs=18, height=0.04 )
pt.annotate_xaxis(10.5, axs2, '$d_\\mathrm{lin}$', lw=1, fs=18, height=0.04 )
pt.annotate_xaxis(17.1, axs2, '$d_\\mathrm{max}$', lw=1, fs=18, height=0.04 )

# build legend for left figure



# basic formatting, move to library
axs.locator_params(axis='x', nbins=4)
axs.locator_params(axis='y', nbins=4)


# figure on the right ("axs")


for density in densities:
    preload_axs=densities[density]
    dfs=dfss[density]
    for preload in preload_axs:
        [preload_axs[preload]['ax'].plot(dfs[preload]['intervals'][i]['data']['Gap'], dfs[preload]['intervals'][i]['data']['Normal Force'], 
            c=clr(preload,minf,maxf), markevery=40, lw=0.8, mfc='None', ms=8, mec='0.2', mew=0.8, marker=marks[density], 
            **preload_axs[preload]['plotargs']) for i in range(20,25,5)]

axs.set_xlim((3.6, 21))
axs.set_ylim((-0.51,0.09))
axs.set_xlabel('$d$ (mm)')
#axs.set_ylabel('$F$ (N)')
cb=fig.colorbar(cm.ScalarMappable(norm=cs.Normalize(maxf,minf), cmap=clrs), 
        ax=axs, ticks=[10,20,30,40], pad=0.01)
cb.ax.tick_params(direction='out')


# build legend for right figure
legend_lines=[

            Line2D([0],[0],color='0.2', lw=1.0, marker='o', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='^', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='s', mfc='None', ms=8),

            ]
axs.legend(legend_lines, [114,361,441])





fig.tight_layout()
fig.savefig('f_d.pdf')

