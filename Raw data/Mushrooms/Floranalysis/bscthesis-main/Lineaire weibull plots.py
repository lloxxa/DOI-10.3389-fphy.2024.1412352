# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:01:26 2022

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
knipfit={naam: zk.weibfit(fit[naam], 9, output='df') for naam in fit}
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


fig, ax=pp.subplots()
[ax.plot(fit[naam]['Xweib'], fit[naam]['Yweib']) for naam in fit]
[ax.plot(knipfit[naam]['Xweib'], knipfit[naam]['tyweib']) for naam in knipfit]