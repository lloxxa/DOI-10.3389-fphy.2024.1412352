# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 10:30:27 2023

@author: Helmendach
"""

import zeekat as zk
import pandas as pd
import glob
import matplotlib.pyplot as pp
import numpy as np
import matplotlib as mp 
from scipy.optimize import curve_fit

#Function that cuts off data before the pull-off force is reached
def catas(df):
    piek=np.min(np.where(df['normalforce']==df['normalforce'].max()))
    df=df.iloc[piek:]
    return df

#Exponential decay function to fit the detachment quantum distribution
def fit(x, A, beta):
    return (A*np.exp(-beta*x))

#Configures plotting parameters
config={'xtick.top':True,
'ytick.right':True,
'xtick.direction':'in',
'ytick.direction':'in',
'xtick.major.size':9,
'ytick.major.size':9,
'xtick.minor.visible':False,
'ytick.minor.visible':True,
'legend.frameon':False,
'legend.fontsize':18,
'font.size':20,
}

mp.rcParams.update(**config) 
#Isolates relevant data
lijst=glob.glob(r"\*")
frames={naam: pd.read_csv(naam) for naam in lijst if int(naam.split('_')[-1][:-4])%4==3}
baselined={naam: zk.baseline( frames[naam] ) for naam in frames}
geknipt={naam: zk.schaar(baselined[naam], 0, 0.01)for naam in baselined}
geknipt={naam: zk.schaar(baselined[naam])for naam in baselined}
#multiplies data by -1, calculates strain
geflipt={naam: zk.flip(geknipt[naam]) for naam in geknipt}
cat={naam: catas(geflipt[naam]) for naam in geflipt}
#finds detachment quanta
distr={naam: zk.quantum(cat[naam], limit=-0.015, fpc=-0.02) for naam in cat}

#combines all lists of detachment quanta
lijst=[]
for naam in distr:
     for i in distr[naam]:
         for j in i:
             lijst.append(j)
#Makes dataframe with frequency per detachment quantum                 
freq=set(lijst)
df1 = pd.Series(lijst).value_counts().sort_index().reset_index().reset_index(drop=True)
df1.columns = ['Element', 'Frequency']
#Finds the total number of detached features
numcup=sum(df1['Element']*df1['Frequency'])
#calculates probability density per detachment quantum
df1=df1.assign(prob=(df1['Element']*df1['Frequency'])/(numcup))
#Fits data using exponential decay function
popt, pcov=curve_fit(fit, xdata=df1['Element'], ydata=df1['prob'], p0=[1, 1])      
xspace=np.arange(1,40, 0.01)

#Makes bar chart with fit function
fig, ax=pp.subplots()
ax.set_ylim(0,0.5)
ax.set_xlim(0,40)
ax.bar(df1['Element'], df1['prob'])
ax.set_xlabel('Detachment quantum')
ax.set_ylabel('P(n)')
ax.plot(xspace, fit(xspace, *popt), color='r')


