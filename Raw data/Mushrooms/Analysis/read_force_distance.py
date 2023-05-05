import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
from sklearn.linear_model import LinearRegression
import pickle

paths114={
            10:"/Users/aljosha/MMI/Sample114/Fn_RawData/2020_03_17_Sample144_v500__5Hz_10Deg_v500_Fn10N.csv",
            16:"/Users/aljosha/MMI/Sample114/Fn_RawData/2020_03_17_Sample144_v500__5Hz_10Deg_v500_Fn16N.csv",
            2:"/Users/aljosha/MMI/Sample114/Fn_RawData/2020_03_17_Sample144_v500__5Hz_10Deg_v500_Fn2N.csv",
            4:"/Users/aljosha/MMI/Sample114/Fn_RawData/2020_03_17_Sample144_v500__5Hz_10Deg_v500_Fn4N.csv",
            6:"/Users/aljosha/MMI/Sample114/Fn_RawData/2020_03_17_Sample144_v500__5Hz_10Deg_v500_Fn6N.csv",
        }

paths361={
            10:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn10N.csv",
            15:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn15N.csv",
            20:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn20N.csv",
            25:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn25N.csv",
            30:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn30N.csv",
            35:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn35N.csv",
            5:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn5N.csv",
            7.5:"/Users/aljosha/MMI/Sample_361/Fn_RawData/2020_03_16_v500_10Deg5Hz_10s_v500_Fn7_5N.csv",
        }

paths441={  
             6:"/Users/aljosha/MMI/Sample441/Fn_RawData/2020_03_17_Sample441_v500_5Hz_10Deg_v500_Fn6_1N.csv",
            12:"/Users/aljosha/MMI/Sample441/Fn_RawData/2020_03_17_Sample441_v500_5Hz_10Deg_v500_Fn12_2N.csv", 
            18:"/Users/aljosha/MMI/Sample441/Fn_RawData/2020_03_17_Sample441_v500_5Hz_10Deg_v500_Fn18_3N.csv",
            24:"/Users/aljosha/MMI/Sample441/Fn_RawData/2020_03_17_Sample441_v500_5Hz_10Deg_v500_Fn24_4N.csv",
            30:"/Users/aljosha/MMI/Sample441/Fn_RawData/2020_03_17_Sample441_v500_5Hz_10Deg_v500_Fn30_5N.csv",
            36:"/Users/aljosha/MMI/Sample441/Fn_RawData/2020_03_17_Sample441_v500_5Hz_10Deg_v500_Fn36_6N.csv",
            42:"/Users/aljosha/MMI/Sample441/Fn_RawData/2020_03_17_Sample441_v500_5Hz_10Deg_v500_Fn42_7N.csv",
        }

def collect_dfs(paths):
    dfs={}
    for preload in paths:
        dfs[preload]={}
        with open(paths[preload]) as f:
            lines=f.readlines()
        
            intervals={}
            n=0
            for l in lines:
                if 'Interval and data points:' in l:
                    splits=l.split(',')
                    interval_no=int(splits[1])
                    interval_npoints=int(splits[2])
                    interval_start=n
                    interval_end=interval_start+interval_npoints
                    intervals[interval_no]={'n_points':interval_npoints, 'int_start':interval_start, 'int_end':interval_end}
                n+=1
        
            for i in intervals:
                columns=lines[intervals[i]['int_start']+1].split(',')[1:]
                columns[-1]=columns[-1][:-2]
                intervals[i]['columns']=columns
        
                units=lines[intervals[i]['int_start']+3].split(',')[1:]
                units[-1]=units[-1][:-2]
                intervals[i]['units']=units
                
                data=lines[intervals[i]['int_start']+4:intervals[i]['int_end']]
                data=[d.split(',')[1:] for d in data] 
                intervals[i]['data']=pd.DataFrame(data, columns=intervals[i]['columns']).replace(r'\n','', regex=True)
                intervals[i]['data']['Normal Force']=pd.to_numeric(intervals[i]['data']['Normal Force'], errors='coerce')
                intervals[i]['data']['Gap']=pd.to_numeric(intervals[i]['data']['Gap'], errors='coerce')
    
            dfs[preload]['intervals']=intervals
    return dfs

densities={"sample441.pickle":paths441, "sample361.pickle":paths361, "sample114.pickle":paths114}

sets={p:collect_dfs(densities[p]) for p in densities}

number_tab=pd.read_csv("numbers.txt")
for dens in densities:
    d=int(dens[6:9])
    for preload in sets[dens]:
        sets[dens][preload]['N_attached']= number_tab.loc[  
            (number_tab['f_preload']==preload) & 
            (number_tab['density']==d) ]\
                .loc[:,['N_1','N_2','N_3','N_4','N_5']]
        sets[dens][preload]['L_c']=number_tab.loc[(number_tab['f_preload']==preload) & 
            (number_tab['density']==d) ]\
                .loc[:,'Lc']
        sets[dens][preload]['L_m']=number_tab.loc[(number_tab['f_preload']==preload) & 
            (number_tab['density']==d) ]\
                .loc[:,'Lm']

        sets[dens][preload]['N_total']=d

for p in densities:
    with open(p, 'wb') as f:
        pickle.dump(sets[p], f)

