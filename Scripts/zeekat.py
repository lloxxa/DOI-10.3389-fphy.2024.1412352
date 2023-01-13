# -*- coding: utf-8 -*-
"""
The zeekat module contains functions used for the analysis of data obtained by rheometry on millimeter-sized suction cups made from polydimethylsiloxane. 

Functions
---------

baseline(df): 
Establishes a baseline for the measured force based on measurements where the sample is completelyt detached from its countersurface.

schaar(df, thresold1, threshold2): i
Isolates part of dataset where the sample detaches from the countersurface.

calcstrain(df): 
Calculates strain from the gap in mm. 

flip(df): 
Multiplies force by -1 to flip the curve. Defines adhesion force as a positive force.

calcwork(df): 
Calculates work of adhesion by integrating force-distance curve.

Weibull(df):
Calculates x and y values for the linearized Weibull distribution so data can be fit by linear regression.


weibfit(df, grens, output):
Fits data to linearized Weibull distribution on a certain domain specified by 'grens' keyword argument. If output is 'pars', it will return the fit parameters. If the output is 'df', it will return the dataframe.

tbull(bereik):
Returns a theoretical force-distance curve using the fit parameters from the weibfit() function. 

quantum(df):
Sorting algorithm that finds the discrete detachment events in a curve and calculates the corresponding number of cups. Returns list with a number of cups for each detachment event.
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore', '.*divide.*', )
warnings.filterwarnings('ignore', '.*invalid value.*', )

def baseline(df):
    """
    Substracts the average of the last 50 data points from every datapoint to establish a baseline. Detachment is complete for these 50 points so the adhesive force is 0.
    
    Arguments
    ---------
    df: Dataframe containing the relevant data to be baselined.
    """
    df['Normal Force [N]']=df['Normal Force [N]']-df.tail(50)['Normal Force [N]'].mean()
    return df


def schaar(df,threshold1=0.0, threshold2=0.0005):
    """
    Isolates part of the curve between the start of the retraction and complete detachment.
    
    Arguments
    ---------
    df: Dataframe containing the relevant data to be isolated.
    
    threshold1: A threshold force which signifies the lowest force value for which detachment has started. Any data before this point is sliced out. Default 0. 
    
    threshold2: A threshold force which signifies the highest force value for which detachment has ended. Any data after this point is sliced out. Default 0.0005. 
    """
    idx=np.min(np.where(df.loc[:,'Normal Force [N]']<threshold1))
    df3=df.iloc[(idx+50):]
    idx2=np.min(np.where(np.abs(df3.loc[:,'Normal Force [N]'])<threshold2))
    df=df.iloc[idx:(idx+idx2+50)]
    return df

def calcstrain(df):
    """
    Calculates the strain from distance with strain=1 when the cups detach
    
    Arguments
    ---------
    df: Dataframe containing the relevant data.
    """
    df=df.assign(Gap=df.loc[:,'Gap [mm]']-df.loc[:, 'Gap [mm]'].iloc[0])
    df=df.assign(strain=df.loc[:,'Gap']/df.loc[:,'Gap'].iloc[-1])
    return df

def flip(df):
    """
    Multiplies the normal force by -1 and places this in a new column.
    
    Arguments
    ---------
    df: Dataframe containing the relevant data.
    """
    df=df.assign(normalforce=df.loc[:,'Normal Force [N]']*-1 )
    df=df.assign(rstress= df['normalforce']/np.max(df['normalforce']))
    return df

def calcwork(df):
    """
    Calculates work of adhesion by integration. Returns work of adhesion.
    
    Arguments
    ---------
    df: Dataframe containing the relevant data.
    """
    work=np.trapz(df.loc[:,'normalforce'], df.loc[:,'Gap [mm]'])
    return work

def weibull(df):
    """
    Calculates x and y values for the linearized Weibull distribution. Not combined with weibfit so these can be used to find the right domain for fitting
    
    Arguments
    ---------
    df: Dataframe containing the relevant data.
    """
    #calculates Young's modulus using the datapoints between the 5th and fifteenth datapoint
    x1=np.array(df['strain'].iloc[5:15])
    y1=np.array(df['normalforce'].iloc[5:15])
    slope=np.polyfit(x1, y1, 1)
    [coeff, intercept]=slope
    #assigns two columns with x- and y values of linearized Weibull distribution
    df=df.assign(Yweib=np.log(np.log((coeff*df.loc[:,'strain'])/df.loc[:,'normalforce'])))
    df=df.assign(Xweib=(np.log(coeff*df['strain'])))
    return df

def weibfit(df, grens, output='pars', **kwargs):  
    """
       
    Fits the linearized weibull distribution. Returns fit parameters or dataframe.
    
    Arguments
    ---------
    df: Dataframe containing the relevant data.
    grens: Point from whereon the data will be fit. Expressed as the x-value of the linearized Weibull distr.: ln(modulus*strain).
    output: Determines output of function. 'pars' will return fit parameters, 'df' will return dataframe and 'ylijn' will return a theoretical curve. Default 'pars'.
    """
    #calculates Young's modulus
    x1=np.array(df['strain'].iloc[5:15])
    y1=np.array(df['normalforce'].iloc[5:15])
    slope=np.polyfit(x1, y1, 1)
    [coeff, intercept]=slope
    #drops all inf values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df=df.dropna()
    #finds the domain to be used for fitting using the domain limit 'grens'
    domein=np.min(np.where(df['Xweib']>(grens)))
    df=df.iloc[domein:]
    if len(df)==0 :
        print('No fit')
        return 'No fit'
    else:
        #linear fit using Xweib en Yweib columns
        Weibull=np.polyfit(df.loc[:,'Xweib'],df.loc[:,'Yweib'], 1)
        [coeff2,intercept2]=Weibull
        sigma= np.exp(-intercept2/coeff2)
        #defines theoretical linear Weibull disitrbution using fit pars
        Ylijn=np.poly1d(Weibull)
        wpar=[sigma, coeff2, coeff]
        #assigns column with theoretical force-distance data based on the fit
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
        

def tbull(bereik, kwargs):
    """
    Returns a theoretical force-distance curve using the weibull parameters from the weibfit() function
    
    Arguments
    ---------
    bereik: Range of x-values for which the curve is computed.
    kwargs: Fit parameters from weibfit() function.
    """
    curve=kwargs[2]*bereik*np.exp(-(kwargs[2]*bereik/kwargs[0])**kwargs[1])
    return curve


def quantum(df, limit=-0.01, fpc=-0.02):
    """
    Sorting algorithm that finds the discrete detachment events in a curve and calculates the corresponding number of cups. Returns list with a number of cups for each detachment event.
    
    Arguments
    ---------
    df: Dataframe containing the relevant data.
    limit: If the difference between subsequent data points is lower than this limit, the data points are considered to be part of a detachment event.
    fpc: Force per cup. The force difference for one detachment event is divided by this value to find the number of features that detached in that specific event. 
    """
    #assigns column with force differences between subsequent data points
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
