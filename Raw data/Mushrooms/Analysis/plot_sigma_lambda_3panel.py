import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
import pickle
import matplotlib as mp
import nutools as nu
import plottools as pt

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


pickles=['sample441.pickle', 'sample361.pickle', 'sample114.pickle']

#
#  density 361 
#

sets_loaded={}
for p in pickles:
    with open(p, 'rb') as f:
        sets_loaded[p]=pickle.load(f)

densities={ 
'sample114.pickle':{
            4:{ 'plotargs':{'c':'k'}         },
            #6: { 'plotargs':{'c':'r'}         },
            16: { 'plotargs':{'c':'g'}         },
        },
'sample361.pickle':{
            7.5: { 'plotargs':{'c':'b'}    }, 
            10:  { 'plotargs':{'c':'k'}    },
            15:  { 'plotargs':{'c':'r'}    }, 
            20:  { 'plotargs':{'c':'g'}    },
            25:  { 'plotargs':{'c':'gray'} },  
            30:  { 'plotargs':{'c':'m'}    },
            35:  { 'plotargs':{'c':'y'}    },
        },
'sample441.pickle':{
            #6: { 'plotargs':{'c':'b'}     },
            12:{ 'plotargs':{'c':'k'}      },
            18: { 'plotargs':{'c':'r'}     },
            24: { 'plotargs':{'c':'g'}     },
            30: { 'plotargs':{'c':'gray'}  },
            36: { 'plotargs':{'c':'m'}     },
            #42: { 'plotargs':{'c':'y'}    }
        },
}

A_total=0.025**2

overwrite_Lc=True

retractions_all={}
cor_frcs={}
parss={}
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
    retractions_all[dens]=retractions
    parss[dens]=pars




fig2, (ax1, ax2, ax3)=pp.subplots(1,3,figsize=(14,6), sharey='row')
axs={'sample441.pickle':ax3, 'sample361.pickle':ax2, 'sample114.pickle':ax1}
ax1.set_ylabel('$\sigma$ (Pa)', fontsize=22)
[ax.set_xlabel('$\lambda$', fontsize=22) for ax in (ax1,ax2,ax3)]
#[ax.set_ylim((-0.45,0.1)) for ax in (ax1, ax2, ax3)]
#ax2.set_xlim((-0.1, 1.2))
ax1.set_title('N$_\\mathrm{total}$=114')
ax2.set_title('N$_\\mathrm{total}$=361')
ax3.set_title('N$_\\mathrm{total}$=441')
#[ax.yaxis.set_ticklabels([]) for ax in (ax2, ax3)]

for dens in cor_frcs:
    dfs=sets_loaded[dens]
    cor_frc=cor_frcs[dens]
    retractions=retractions_all[dens]
    preload_axs=densities[dens]
    pars=parss[dens]
    for preload in cor_frc:
        [axs[dens].plot( cor_frc[preload][ret]['lambda'], cor_frc[preload][ret]['sigma'], 
            marker='o', ms=4, lw=0, mew=0.5, markevery=1, mfc='None', **preload_axs[preload]['plotargs']  ) 
            for ret in cor_frc[preload]]
        [ pt.annotate_xaxis( float(dfs[preload]['L_m']/pars[preload]['L_c'][1.0]), ax=axs[dens], 
            lbl="$\lambda_m$", c=preload_axs[preload]['plotargs']['c']) ]

    #    [ax.plot( cor_frc[preload][ret]['log2lambda'], cor_frc[preload][ret]['log2sigma'], 
    #        marker='o', ms=8, lw=0, mew=0.4, markevery=3, mfc='None', **preload_axs[preload]['plotargs']  ) 
    #        for ret in cor_frc[preload]]


#
# De-exponentialized force versus lambda 
#

# legend generation
for dens in densities:
    preload_axs=densities[dens]
    [axs[dens].plot([],[], **preload_axs[preload]['plotargs'], marker='o', ms=8, lw=0, mfc='None', 
            label="$f_\\mathrm{{p}}=${}".format(preload)) 
            for preload in preload_axs]
    axs[dens].legend(frameon=False, handletextpad=0.1)

fig2.tight_layout()
fig2.savefig("sigma_lambda_complete_3panel.pdf")
