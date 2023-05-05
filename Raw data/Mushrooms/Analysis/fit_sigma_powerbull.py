import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib.pyplot as pp
import pickle
import matplotlib as mp
import matplotlib.colors as cs
import matplotlib.cm as cm
import nutools as nu
import lmfit as lm
from matplotlib import gridspec

# to update changes to numbers.txt . Can mostly be commented out.
exec(open("read_force_distance.py").read())
gridspec_kw={'width_ratios': [0.8, 1.0]}

pp.ion()

config={
'xtick.top':True,
'ytick.right':True,
'xtick.direction':'in',
'ytick.direction':'in',
'xtick.major.size':9,
'ytick.major.size':9,
'xtick.minor.visible':True,
'ytick.minor.visible':True,
'legend.frameon':False,
'legend.fontsize':18,
'axes.titlesize':14,
'font.size':18,
}
mp.rcParams.update(**config)

lims={ 

'sample114.pickle':
{
4:{
                1:(-7.7, -5.9),
                2:(-7.437, -5.9),
                3:(-7.7, -5.9),
                4:(-7.7, -5.9),
                5:(-7.3, -5.9),
  },

16:
  {
                1:(-7.7, -5.9),
                2:(-7.437, -5.9),
                3:(-7.7, -5.9),
                4:(-7.7, -5.9),
                5:(-7.3, -5.9),
  },
},
            
'sample361.pickle':{
        10:
            {
                1:(-8.7, -5.9),
                2:(-8.437, -5.9),
                3:(-8.7, -5.9),
                4:(-8.7, -5.9),
                5:(-8.3, -5.9),
            },

#        15:
#            {
#                1:(-18.7, -4.9),
#                2:(-18.437, -4.9),
#                3:(-18.7, -4.9),
#                4:(-18.7, -4.9),
#                5:(-18.3, -4.9),
#            },
#
        20:
            {
                1:(-8.7, -5.9),
                2:(-8.437, -5.9),
                3:(-8.7, -5.9),
                4:(-8.7, -5.9),
                5:(-8.3, -5.9),
            },

       25:
            {
                1:(-8.7, -5.9),
                2:(-8.437, -5.9),
                3:(-8.7, -5.9),
                4:(-8.7, -5.9),
                5:(-8.3, -5.9),
            },
       30:
            {
                1:(-8.7, -5.9),
                2:(-8.437, -5.9),
                3:(-8.7, -5.9),
                4:(-8.7, -5.9),
                5:(-8.3, -5.9),
            },

        35:
            {
                1:(-8.7, -5.9),
                2:(-8.437, -5.9),
                3:(-8.7, -5.9),
                4:(-8.7, -5.9),
                5:(-8.3, -5.9),
            },

},

'sample441.pickle':
        {12:
            {
                1:(-6.7, -5.9),
                2:(-6.437, -5.9),
                3:(-6.7, -5.9),
                4:(-6.7, -5.9),
                5:(-6.3, -5.9),
            },

        18: 
            {
                1:(-6.4, -5.8),
                2:(-6.437, -5.9),
                3:(-6.7, -5.9),
                4:(-6.7, -5.9),
                5:(-6.05, -5.75),
            },

        24: 
            {
                1:(-6.1, -5.7),
                2:(-6.0, -5.858),
                3:(-5.92, -5.734),
                4:(-5.85, -5.65),
                5:(-6.05, -5.75),
            },

        30: 
            {
                1:(-6.7, -5.9),
                2:(-6.437, -5.9),
                3:(-6.7, -5.9),
                4:(-6.7, -5.9),
                5:(-6.3, -5.9),
            },

        36:
		{
                1:(-6.7, -5.9),
                2:(-6.437, -5.9),
                3:(-6.7, -5.9),
                4:(-6.7, -5.9),
                5:(-6.3, -5.9),
            },

         }, 
}


pickles=[   
            'sample441.pickle', 
            'sample361.pickle', 
            'sample114.pickle'
        ]


floors={ 'sample441.pickle':-6.6, 
        'sample361.pickle':-6.4 , 
        'sample114.pickle':-6.4 }

densities={ 
'sample114.pickle':{
            4:{ 'plotargs':{}         },
            6: { 'plotargs':{}         },
            16: { 'plotargs':{}         },
        },
'sample361.pickle':{
#            7.5: { 'plotargs':{}    }, 
            10:  { 'plotargs':{}    },
            15:  { 'plotargs':{}    }, 
            20:  { 'plotargs':{}    },
            25:  { 'plotargs':{} },  
            30:  { 'plotargs':{}    },
            35:  { 'plotargs':{}    },
        },
'sample441.pickle':{
            #6: { 'plotargs':{}     },
            12:{ 'plotargs':{}      },
            18: { 'plotargs':{}     },
            24: { 'plotargs':{}     },
            30: { 'plotargs':{}  },
            36: { 'plotargs':{}     },
            #42: { 'plotargs':{}    }
        },
}

sets_loaded={}
for p in pickles:
    with open(p, 'rb') as f:
        sets_loaded[p]=pickle.load(f)

A_total=0.025**2

pars_dens={}
cor_frcs={}
for dens in pickles:
    preload_axs=densities[dens]
    dfs=sets_loaded[dens]
    retractions={}
    cpd_ret={}
    fits={}
    adhesion={}
    pars={}
    cor_frc={}
    for preload in [preload for preload in preload_axs if np.any( dfs[preload]['N_attached'] )]:
        pars[preload]={}
        
        # only load preloads that have N_attached specified, ignore the rest
        retractions[preload]={i/5: dfs[preload]['intervals'][i]['data'].loc[:,['Gap', 'Normal Force']] \
                for i in range(5,30,5)}
    
        pars[preload]['A_att']={ret: A_total*dfs[preload]['N_attached'].iloc[0,int(ret-1)]/dfs[preload]['N_total'] 
                for ret in retractions[preload]}
    
        # find the relevant region
        cpd_ret[preload]={ret: nu.chop_retraction(retractions[preload][ret]) for ret in retractions[preload]}
    
        pars[preload]['L_c']={ret: 1e-3*(np.max(cpd_ret[preload][ret]['Gap'])-np.min(cpd_ret[preload][ret]['Gap']))
                    for ret in cpd_ret[preload]}
    
        # transform to sigma_adhesion vs. strain
        adhesion[preload]={ret: nu.ret2adh(cpd_ret[preload][ret], pars[preload]['L_c'][ret],  \
                pars[preload]['A_att'][ret], dfs[preload]['N_attached'].iloc[0,int(ret-1)] ) 
                for ret in cpd_ret[preload]}
    
        # obtain modulus level
        pars[preload]['moduli']={ret: nu.stretch_modulus(adhesion[preload][ret],  \
                pars[preload]['A_att'][ret]) for ret in cpd_ret[preload]  }
    
    
        cor_frc[preload]={ret: nu.cor_frc_finexp(adhesion[preload][ret], pars[preload]['moduli'][ret], 
                pars[preload]['L_c'][ret], float(dfs[preload]['L_m']),  
                dfs[preload]['N_attached'].iloc[0,int(ret-1)], floors[dens] ) 
                for ret in adhesion[preload]  }
        
        pars[preload]['pow_law']={ret: nu.get_power(cor_frc[preload][ret], (-1.5,-0.05))\
                for ret in cor_frc[preload]}
#
#        pars[preload]['reg']={ret: 
#            nu.reg_Weibull(cor_frc[preload][ret], pars[preload]['moduli'][ret], 
#                pars[preload]['L_c'][ret], float(dfs[preload]['L_m']), lims=lims[dens][preload][ret]) 
#            for ret in adhesion[preload]}
#
#        pars[preload]['m']={ret: round(pars[preload]['reg'][ret]['slope'], 2) 
#                for ret in adhesion[preload]}
#        pars[preload]['sigma_0']={ret:np.exp(-pars[preload]['reg'][ret]['intercept']/pars[preload]['reg'][ret]['slope']) 
#                for ret in adhesion[preload]}

    cor_frcs[dens]=cor_frc
    pars_dens[dens]=pars


fig1, (ax1,ax2,ax3)=pp.subplots(1,3,figsize=(12,6))#, gridspec_kw=gridspec_kw)# sharey='row', sharex='row')
axs={'sample441.pickle':ax1, 'sample361.pickle':ax2, 'sample114.pickle':ax3}
ax1.set_ylabel('$\\frac{F}{N}$', fontsize=22)
[ax.set_xlabel('$\lambda \\xi $', fontsize=22) for ax in (ax1,ax2,ax3)]

clrs=pp.get_cmap("inferno")
clr=lambda n,mina,maxa: clrs(round(255* ( n / (maxa-mina))  ))
minf=4
maxf=50

marks=  {'sample114.pickle':'o', 'sample361.pickle':'^', 'sample441.pickle':'s'}
retmap=lambda ret: 0.5 if ret==1 else 0.5
markmap= {1:'o',2:'s',3:'^',4:'P',5:'<'}
#fitpars={
#        'pickle441.pickle':{
#            "pow_shift":[]


f_N_pow = lambda E, lamb, alpha: 10**E*lamb**alpha
Weibull_decay = lambda lamb, E, sigma_0,m: np.exp(-( lamb*E/sigma_0 )**m)

########### RIGHTHAND PANEL
powerbull = lambda lambd, pow_amp, alpha, E, sigma_0, m: 10**pow_amp*lambd**alpha*np.exp( -( lambd*E/sigma_0 )**m )
model = lm.Model(powerbull)

tuples={
        'sample114.pickle': {
			preload:{
				ret:(
				('pow_amp', pars_dens['sample114.pickle'][preload]['pow_law'][ret]['shift'], True, -3, -2),
				('alpha', pars_dens['sample114.pickle'][preload]['pow_law'][ret]['alpha'], True, 0.8, 2.0),
				('E', 2.819e-3, False, 1e-3, 3e-3),
				('sigma_0', 3.392e-3, True, 1e-3, 10e-3),
				('m', 2, True, 1, 40)) for ret in (1,2,3,4,5)
            } for preload in (4,6,16,) #densities['sample361.pickle']
		},

        'sample361.pickle': {
			preload:{
				ret:(
				('pow_amp', pars_dens['sample361.pickle'][preload]['pow_law'][ret]['shift'], True, -3, -2),
				('alpha', pars_dens['sample361.pickle'][preload]['pow_law'][ret]['alpha'], True, 0.8, 2.0),
				('E', 2.819e-3, False, 1e-3, 3e-3),
				('sigma_0', 3.392e-3, True, 1e-3, 10e-3),
				('m', 2, True, 1, 40)) for ret in (1,2,3,4,5)
            } for preload in (10,15,20,25,30,35,) #densities['sample361.pickle']
		},
        'sample441.pickle': {
			12:{
				ret:(
				('pow_amp', pars_dens['sample441.pickle'][12]['pow_law'][ret]['shift'], True, -3, -2),
				('alpha', pars_dens['sample441.pickle'][12]['pow_law'][ret]['alpha'], True, 0.8, 2.0),
				('E', 2.819e-3, False, 1e-3, 3e-3),
				('sigma_0', 3.392e-3, True, 1e-3, 10e-3),
				('m', 2, True, 1, 40)) for ret in (1,2,3,4)
            },
            18:{
				ret:(                                      		
     		    ('pow_amp', -2.59538, True, -3, -2),
    			('alpha', 1.437, True, 1, 2.0),
    			('E', 2.819e-3, False, 1e-3, 3e-3),
    			('sigma_0', 3.392e-3, True, 1e-3, 10e-3),
				('m', 10, True, 4, 12)) for ret in (1,2,3,4,5)
			},
            24:{
				ret:(                                      		
    			('pow_amp', -2.59538, True, -3, -2),
    			('alpha', 1.437, True, 1, 2.0),
    			('E', 2.819e-3, False, 1e-3, 3e-3),
    			('sigma_0', 3.392e-3, True, 1e-3, 10e-3),
				('m', 10, True, 4, 12)) for ret in (1,2,3,4,5)
			},
			30:{
				ret:(                                      		
				('pow_amp', -2.59538, True, -3, -2),
				('alpha', 1.437, True, 1, 2.0),
				('E', 2.819e-3, False, 1e-3, 3e-3),
				('sigma_0', 3.392e-3, True, 1e-3, 10e-3),
				('m', 10, True, 4, 12)) for ret in (1,2,3,4,5)
			},
            36:{
				ret:(                                      		
				('pow_amp', -2.59538, True, -3, -2),
				('alpha', 1.437, True, 1, 2.0),
				('E', 2.819e-3, False, 1e-3, 3e-3),
				('sigma_0', 3.392e-3, True, 1e-3, 10e-3),
				('m', 10, True, 4, 12)) for ret in (1,2,3,4,5)
			},
        }
    }
#
results={ dens:{ preload:{ ret: {} for ret in tuples[dens][preload]} for preload in tuples[dens]} for dens in tuples }
for dens in tuples:
    for preload in tuples[dens]:
        for ret in tuples[dens][preload]:
            lambd=cor_frcs[dens][preload][ret]['lambda']
            F=cor_frcs[dens][preload][ret]['F_mushroom']
            p=lm.Parameters()
            p.add_many(*tuples[dens][preload][ret])
            r=model.fit(F,p,lambd=lambd,)
            results[dens][preload][ret]=r
            axs[dens].plot(np.linspace(0,1,1000),
                    model.eval(r.params, lambd=np.linspace(0,1,1000)), 
                    ls='--' ,c=clr(preload,minf,maxf),lw=0.8, label=ret)

for dens in tuples:
    pars=pars_dens[dens]
    cor_frc=cor_frcs[dens]
    preload_axs=densities[dens]
    for preload in tuples[dens]:
        nu.mrks.reset()
        [axs[dens].plot( cor_frc[preload][ret]['lambda'], cor_frc[preload][ret]['F_mushroom'], 
            marker=markmap[ret], markevery=5, ms=4, lw=0, mew=retmap(ret), mec=clr(preload,minf,maxf), mfc='None', 
            c=clr(preload,minf,maxf), 
            **preload_axs[preload]['plotargs'] ) 
            for ret in tuples[dens][preload]]
        
#        [axs[dens].plot( cor_frc[preload][ret]['lambda'].iloc[1:], 
#            f_N_pow(pars[preload]['pow_law'][ret]['shift'],cor_frc[preload][ret]['lambda'].iloc[1:],pars[preload]['pow_law'][ret]['alpha'])*
#            Weibull_decay(cor_frc[preload][ret]['lambda'].iloc[1:], pars[preload]['moduli'][ret], pars[preload]['sigma_0'][ret], pars[preload]['m'][ret]), 
#            c=clr(preload,minf,maxf), ls=':', lw=retmap(ret) ) for ret in tuples[dens][preload]]

fig1.tight_layout()



