import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
import pickle
import matplotlib as mp
import nutools as nu


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


pickles=[ 'sample361.pickle']

#
#  density 361 
#

sets_loaded={}
for p in pickles:
    with open(p, 'rb') as f:
        sets_loaded[p]=pickle.load(f)

densities={ 
'sample361.pickle':{
            7.5: { 'plotargs':{'c':'b'}    }, 
            10:  { 'plotargs':{'c':'k'}    },
            15:  { 'plotargs':{'c':'r'}    }, 
            20:  { 'plotargs':{'c':'g'}    },
            25:  { 'plotargs':{'c':'gray'} },  
            30:  { 'plotargs':{'c':'m'}    },
            35:  { 'plotargs':{'c':'y'}    },
        },
}

A_total=0.025**2

overwrite_Lc=True

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
    
        # overwrite L_c
        if overwrite_Lc:
            pars[preload]['L_c']={ret: 1e-3*(np.max(cpd_ret[preload][ret]['Gap'])-np.min(cpd_ret[preload][ret]['Gap']))
                    for ret in cpd_ret[preload]}
        else:
            pars[preload]['L_c']={ret: float(dfs[preload]['L_c']) for ret in cpd_ret[preload]}
    
        # transform to sigma_adhesion vs. strain
        adhesion[preload]={ret: nu.ret2adh(cpd_ret[preload][ret], pars[preload]['L_c'][ret],  \
                pars[preload]['A_att'][ret], dfs[preload]['N_attached'].iloc[0,int(ret-1)] ) 
                for ret in cpd_ret[preload]}
    
        # obtain modulus level
        pars[preload]['moduli']={ret: nu.stretch_modulus(adhesion[preload][ret],  \
                pars[preload]['A_att'][ret]) for ret in cpd_ret[preload]  }
    
    
        cor_frc[preload]={ret: nu.cor_frc_finexp(adhesion[preload][ret], pars[preload]['moduli'][ret], 
                pars[preload]['L_c'][ret], float(dfs[preload]['L_m']),  
                dfs[preload]['N_attached'].iloc[0,int(ret-1)] ) 
   	            for ret in adhesion[preload]  }
    cor_frcs[dens]=cor_frc


fig2, (ax1,ax2)=pp.subplots(1,2,figsize=(10,6), sharex='row')
axs={ 'sample361.pickle':ax2, }
ax1.set_ylabel('$\\sigma$', fontsize=22)
ax2.set_ylabel('$\\frac{F}{ N E }$', fontsize=22)
[ax2.set_xlabel('$\lambda$', fontsize=22) for ax in [ax1,ax2]]
[ax2.set_xlabel('$\lambda \\xi $', fontsize=22) for ax in [ax1,ax2]]
ax1.set_xlim((-0.1, 1.2))
ax2.set_ylim((-0.1, 1.05))


for dens in cor_frcs:
	cor_frc=cor_frcs[dens]
	preload_axs=densities[dens]
	for preload in cor_frc:
	    [ax1.plot( cor_frc[preload][ret]['lambda'], cor_frc[preload][ret]['sigma'], 
	        marker='o', ms=8, lw=0, mew=0.4, markevery=1, mfc='None', **preload_axs[preload]['plotargs']  ) 
	        for ret in cor_frc[preload]]
	    [ax2.plot( cor_frc[preload][ret]['lambda_deexp'], cor_frc[preload][ret]['f_by_NE'], 
	        marker='o', ms=4, lw=0, mew=0.2, markevery=2, mfc='None', **preload_axs[preload]['plotargs']  ) 
	        for ret in cor_frc[preload]]


#
# De-exponentialized force versus lambda 
#

ax2.set_title('N$_\\mathrm{total}$=361')
# legend generation
for dens in densities:
    preload_axs=densities[dens]
    [axs[dens].plot([],[], **preload_axs[preload]['plotargs'], marker='o', ms=8, lw=0, mfc='None', 
            label="$f_\\mathrm{{p}}=${}".format(preload)) 
            for preload in preload_axs]
    axs[dens].legend(frameon=False, handletextpad=0.1)

fig2.tight_layout()
fig2.savefig( "inact_domain_3panel.pdf" )
