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
#trekt gemiddelde van laatste 50 punten af van elk punt
def baseline(df):
    df['Normal Force [N]']=df['Normal Force [N]']-df.tail(50)['Normal Force [N]'].mean()
    return df
#definieert functie die stress per feature uitrekent, voor P2.5-110, P3-80 en P4-42. 
def calcstress(df, features=80):
    df=df.assign(stress=(df.loc[:,'normalforce']/features)/(np.pi*(0.002/2)**2))
    return df
#knipt niet-relevante data van de curve af
def schaar(df,threshold1=0.0, threshold2=0.0005):
    idx=np.min(np.where(df.loc[:,'Normal Force [N]']<threshold1))
    df3=df.iloc[(idx+50):]
    idx2=np.min(np.where(np.abs(df3.loc[:,'Normal Force [N]'])<threshold2))
    df=df.iloc[idx:(idx+idx2+50)]
    return df
#maakt functie die kolom met strain maakt
def calcstrain(df):
    df=df.assign(Gap=df.loc[:,'Gap [mm]']-df.loc[:, 'Gap [mm]'].iloc[0])
    df=df.assign(strain=df.loc[:,'Gap']/df.loc[:,'Gap'].iloc[-1])
    return df
#maakt functie die stress flipt van negatief naar positief, maakt ook meteen een kolom met de genormaliseerde stress
def flip(df):
    df=df.assign(normalforce=df.loc[:,'Normal Force [N]']*-1 )
    df=df.assign(rstress= df['normalforce']/np.max(df['normalforce']))
    return df
#berekent work of adhesion dmv integratie
def calcwork(df):
    work=np.trapz(df.loc[:,'normalforce'], df.loc[:,'Gap [mm]'])
    return work
#maakt functie die elastische modulus berekent
def modulus(df):
    x1=np.array(df['strain'].iloc[0:10])
    y1=np.array(df['stress'].iloc[0:10])
    slope=np.polyfit(x1, y1, 1)
    #slope= np.polyfit(df.loc[:'strain'].iloc[0:10], df.loc[:'stress'].iloc[0:10], 1)
    [coeff, intercept]=slope
    print(coeff)
    return coeff
#berekent modulus en maakt kolommen met y en x voor de lineaire weibull vergelijkingen. 
#niet gecombineerd met weibfit() zodat het df dat deze functie maakt kan worden gebruikt om het juiste domein te vinden
def weibull(df):
    x1=np.array(df['strain'].iloc[5:15])
    y1=np.array(df['stress'].iloc[5:15])
    slope=np.polyfit(x1, y1, 1)
    [coeff, intercept]=slope
    df=df.assign(Yweib=np.log(np.log((coeff*df.loc[:,'strain'])/df.loc[:,'stress'])))
    df=df.assign(Xweib=(np.log(coeff*df['strain'])))
    return df
    
#fit de lineaire weibull vergelijking, dropt alle NaN rijen en returnt de weibull pars of het dataframe 
def weibfit(df, grens, output='pars', **kwargs):  
    x1=np.array(df['strain'].iloc[5:15])
    y1=np.array(df['stress'].iloc[5:15])
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
        df=df.assign(tyweib=(Ylijn(df.loc[:, 'Xweib'])))
        wpar=[sigma, coeff2, coeff]
        df=df.assign(tstress= ((coeff*df.loc[:,'strain'])/np.exp(np.exp(Ylijn(df['Xweib'])))))
        if output=='df':
            return df
        elif output=='pars':
            return wpar
        else:
            print('Geef gewenste output aan (pars voor Weibull parameters en df voor dataframe)')
            return wpar
        
# berekent een theoretische stress-strain curve met output van weibfit(output='pars')
def tbull(bereik, kwargs):
    curve=kwargs[2]*bereik*np.exp(-(kwargs[2]*bereik/kwargs[0])**kwargs[1])
    return curve
