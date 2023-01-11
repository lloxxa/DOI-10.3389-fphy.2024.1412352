# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:41:45 2022

@author: Helmendach
"""

import pandas as pd
import glob
import matplotlib.pyplot as pp
import numpy as np
import warnings
import matplotlib as mp
warnings.filterwarnings('ignore', '.*divide.*', )
warnings.filterwarnings('ignore', '.*invalid value.*', )
#Substracts the average of the last 50 data points from every datapoint. Detachment is complete for these 50 points so the adhesive force is 0.
def baseline(df):
    df['Normal Force [N]']=df['Normal Force [N]']-df.tail(50)['Normal Force [N]'].mean()
    return df

#Isolates part of the curve between the start of the retraction and complete detachment
def schaar(df,threshold1=0.0, threshold2=0.0005):
    idx=np.min(np.where(df.loc[:,'Normal Force [N]']<threshold1))
    df3=df.iloc[(idx+50):]
    idx2=np.min(np.where(np.abs(df3.loc[:,'Normal Force [N]'])<threshold2))
    df=df.iloc[idx:(idx+idx2+50)]
    return df
#Calculates the strain with strain=1 when the cups detach
def calcstrain(df):
    df=df.assign(Gap=df.loc[:,'Gap [mm]']-df.loc[:, 'Gap [mm]'].iloc[0])
    df=df.assign(strain=df.loc[:,'Gap']/df.loc[:,'Gap'].iloc[-1])
    return df
#multiplies the normal force by `1 and places this in a new column
def flip(df):
    df=df.assign(normalforce=df.loc[:,'Normal Force [N]']*-1 )
    df=df.assign(rstress= df['normalforce']/np.max(df['normalforce']))
    return df
#Calculates work of adhesion by integration
def calcwork(df):
    work=np.trapz(df.loc[:,'normalforce'], df.loc[:,'Gap [mm]'])
    return work


#calculates x and y values for the linearized Weibull distribution. Not combined with weibfit so these can be used to find the right domain for fitting
def weibull(df):
    x1=np.array(df['strain'].iloc[5:15])
    y1=np.array(df['normalforce'].iloc[5:15])
    slope=np.polyfit(x1, y1, 1)
    [coeff, intercept]=slope
    df=df.assign(Yweib=np.log(np.log((coeff*df.loc[:,'strain'])/df.loc[:,'normalforce'])))
    df=df.assign(Xweib=(np.log(coeff*df['strain'])))
    return df
    
#fits the linearized weibull distribution. Returns fit parameters or dataframe
def weibfit(df, grens, output='pars', **kwargs):  
    x1=np.array(df['strain'].iloc[5:15])
    y1=np.array(df['normalforce'].iloc[5:15])
    slope=np.polyfit(x1, y1, 1)
    [coeff, intercept]=slope
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df=df.dropna()
    domein=np.min(np.where(df['Xweib']>(grens)))
    df=df.iloc[domein:]
    if len(df)==0 :
        print('No fit')
        return 'No fit'
    else:
        Weibull=np.polyfit(df.loc[:,'Xweib'],df.loc[:,'Yweib'], 1)
        [coeff2,intercept2]=Weibull
        sigma= np.exp(-intercept2/coeff2)
        Ylijn=np.poly1d(Weibull)
        wpar=[sigma, coeff2, coeff]
        df=df.assign(tstress= ((coeff*df.loc[:,'strain'])/np.exp(np.exp(Ylijn(df['Xweib'])))))
        if output=='df':
            return df
        elif output=='pars':
            return wpar
        elif output=='ylijn':
            return Ylijn
        else:
            print('Indicate desired output (pars for Weibull parameters en df for dataframe)')
            return wpar
        
#returns a theoretical force-distance curve using the weibull parameters from the weibfit() function
def tbull(bereik, kwargs):
    curve=kwargs[2]*bereik*np.exp(-(kwargs[2]*bereik/kwargs[0])**kwargs[1])
    return curve

#sorting algorithm that finds the discrete detachment events in a curve and the corresponding number of features
def quantum(df, limit=-0.01, fpc=-0.02):
    df=df.assign(gradient= np.diff(df['normalforce'], prepend=2))
    df=df.assign(xgrad=np.gradient(df['Gap [mm]']))
    df=df[df['xgrad']<0.01]
    dots=[]
    avcount=0
    forces=[]
    cumforce=0
    avalanche=False 
    for i in df['gradient']:
        if -0.1<i<=limit and avalanche==False:
            avalanche=True
            avcount+=1
            cumforce+=i
        elif -0.1<i<=limit and avalanche==True:
            avcount+=1
            cumforce+=i
        elif (i>limit or i<-0.1) and avalanche==True:
            avalanche=False
            dots.append(avcount)
            avcount=0
            forces.append(cumforce)
            cumforce=0
        else:
            continue 
        

    apr={num/fpc for num in forces}
    quant=np.around(np.array(list(apr)))
    quanta=[[x for x in quant if x!=0]]

    a_set = set()
    for i in quanta:
        a_set.update(set(i))
    return quanta
