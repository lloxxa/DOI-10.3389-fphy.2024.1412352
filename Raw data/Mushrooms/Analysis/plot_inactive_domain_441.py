import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
from sklearn.linear_model import LinearRegression
import pickle
import matplotlib as mp
import os

exec(open("read_force_distance.py").read())

clrs=pp.get_cmap("plasma")
clr=lambda n,mina,maxa: clrs(round(255* ( n / (maxa-mina))  ))
minf=4
maxf=50

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


densities=['sample441.pickle', 'sample361.pickle', 'sample114.pickle']

#
#  density 441
#

sets_loaded={}
for p in densities:
    with open(p, 'rb') as f:
        sets_loaded[p]=pickle.load(f)

dfs=sets_loaded['sample441.pickle']

preload_axs={
#            6:  {'plotargs':{}      }, 
#            12: {'plotargs':{}         },
#            18: {'plotargs':{}         }, 
#            24: {'plotargs':{}         },
#            30: {'plotargs':{}      },  
            36: {'plotargs':{}         },
#            42: {'plotargs':{}         }
        }

def chop_retraction(retraction, ):
    # slice the curve so we'll just have the interesting part to us
    diffs=np.diff(retraction['Normal Force'])
    sth_diffs=np.convolve(diffs, np.ones(5)/5, mode='same')

    adh_idx=np.min(np.where(np.abs(sth_diffs[:])<0.001))
    adh_idx_last=adh_idx+np.min(np.where(np.max(sth_diffs[adh_idx:])==sth_diffs[adh_idx:]))+3
    
    cpd_ret=retraction.iloc[adh_idx:adh_idx_last]
    return cpd_ret

def ret2adh(cpd_ret, L_c, A_att, N_att):
    adhesion=pd.DataFrame()

    adhesion['Normal Force']=cpd_ret['Normal Force']
    adhesion['lambda']=1e-3 * (  cpd_ret.loc[:,'Gap'] - cpd_ret.iloc[0,0] ) / L_c # in m/m, thus unitless
    adhesion['F_mushroom']=( -( cpd_ret['Normal Force'] - cpd_ret.iloc[0,1] ) / N_att ) # in N/mush
    adhesion['sigma']=( -(cpd_ret.loc[:,'Normal Force']-cpd_ret.iloc[0,1])/N_att/A_att ) # in Pa/mush

    return(adhesion)

def stretch_modulus(adhesion, A_att, lims=(0.2,0.5)):
    bounded_idc=adhesion.index[(adhesion['lambda']>lims[0]) & (adhesion['lambda']<lims[1]) ]
    lmbd=np.array(adhesion['lambda'].iloc[bounded_idc])
    sigma=np.array(adhesion['sigma'].iloc[bounded_idc])
    reg = LinearRegression().fit(lmbd.reshape(-1,1), sigma) 
    E=reg.coef_*A_att
    return E 

def cor_frc_finexp(adhesion, E, L_c, L_m, N_att):
    print("N={}".format(N_att))
    print("Lc={}".format(L_c))
    print("Lm={}".format(L_m))
    print("E={}".format(E))

    W=L_m/L_c
    cor_frc=pd.DataFrame()
    cor_frc['lambda']= adhesion['lambda']

    cor_frc['lambda.E']= adhesion['lambda']*float(E)
    cor_frc['sigma_deexp']= -adhesion['Normal Force']/(N_att*float(E)*adhesion['lambda']*(1-np.exp(-adhesion['lambda']/W)))
    cor_frc['lambda_deexp']= adhesion['lambda']/(1-np.exp(-adhesion['lambda']/W))
    cor_frc['log1sigma']= -np.log( cor_frc['sigma_deexp']  )

    positive_idx=cor_frc.index[cor_frc['log1sigma']>0]

    cor_frc['log2lambda_raw']= np.log( cor_frc['lambda.E'].loc[positive_idx] )
    cor_frc['log2sigma_raw']= np.log( cor_frc['log1sigma'].loc[positive_idx] )

    cor_frc['log2lambda']=cor_frc['log2lambda_raw'].loc[cor_frc.index[ cor_frc['log2lambda_raw']>-6.8  ]]
    cor_frc['log2sigma']=cor_frc['log2sigma_raw'].loc[cor_frc.index[ cor_frc['log2lambda_raw']>-6.8  ]]


    #-1*adh[r][:,1]/(normF[r][:,0]*n_feat[r]*E[r]*(1-np.exp(-normF[r][:,0]/(W))  ))]).transpose() for r in runs}
    return(cor_frc)

def reg_Weibull(cor_frc, E, L_c, L_m):
    bounded=pd.DataFrame()
    bounded_idc=cor_frc.index[(cor_frc['log2sigma']>-1.5) & (cor_frc['log2sigma']<0.3) ]
    bounded['log2lambda']=cor_frc['log2lambda'].loc[bounded_idc]
    bounded['log2sigma']=cor_frc['log2sigma'].loc[bounded_idc]
    reg_log=LinearRegression().fit( np.array(bounded['log2lambda']).reshape(-1,1), np.array(bounded['log2sigma'])  )
    reg_slp=reg_log.coef_[0]
    reg_icpt=reg_log.intercept_
    y_model=reg_icpt+reg_slp*bounded['log2lambda']

    sigma_0=np.exp( -reg_icpt/reg_slp )
    sigma_deexp_model=np.exp(-( cor_frc['lambda']*E/( sigma_0  )  )**reg_slp)#*( 1 - np.exp(-cor_frc['lambda'] / (L_m/L_c) )  )  
       #E*cor_frc['lambda']* 

    return({'slope':reg_slp, 'intercept':reg_icpt, 'x_model':bounded['log2lambda'], 'y_model':y_model, 'sigma_deexp_model':sigma_deexp_model})

A_total=0.025**2
retractions={}
cpd_ret={}
fits={}
adhesion={}
pars={}
cor_frc={}

overwrite_Lc=True

# this really ought to go into a library
for preload in [preload for preload in preload_axs if np.any( dfs[preload]['N_attached'] )]:
    pars[preload]={}
    
    # only load preloads that have N_attached specified, ignore the rest
    retractions[preload]={i/5: dfs[preload]['intervals'][i]['data'].loc[:,['Gap', 'Normal Force']] \
            for i in range(5,30,5)}

    pars[preload]['A_att']={ret: A_total*dfs[preload]['N_attached'].iloc[0,int(ret-1)]/dfs[preload]['N_total'] 
            for ret in retractions[preload]}

    # find the relevant region
    cpd_ret[preload]={ret: chop_retraction(retractions[preload][ret]) for ret in retractions[preload]}

    # overwrite L_c
    if overwrite_Lc:
        pars[preload]['L_c']={ret: 1e-3*(np.max(cpd_ret[preload][ret]['Gap'])-np.min(cpd_ret[preload][ret]['Gap']))
                for ret in cpd_ret[preload]}
    else:
        pars[preload]['L_c']={ret: float(dfs[preload]['L_c']) for ret in cpd_ret[preload]}

    # transform to sigma_adhesion vs. strain
    adhesion[preload]={ret: ret2adh(cpd_ret[preload][ret], pars[preload]['L_c'][ret],  \
            pars[preload]['A_att'][ret], dfs[preload]['N_attached'].iloc[0,int(ret-1)] ) 
            for ret in cpd_ret[preload]}

    # obtain modulus level
    pars[preload]['moduli']={ret: stretch_modulus(adhesion[preload][ret],  \
            pars[preload]['A_att'][ret]) for ret in cpd_ret[preload]  }


    cor_frc[preload]={ret: cor_frc_finexp(adhesion[preload][ret], pars[preload]['moduli'][ret], 
            pars[preload]['L_c'][ret], float(dfs[preload]['L_m']),  
            dfs[preload]['N_attached'].iloc[0,int(ret-1)] ) 
            for ret in adhesion[preload]  }


#fig, ax=pp.subplots(figsize=(8,6))
#fig2, ax2=pp.subplots(figsize=(8,6))

ax2=pp.gca()
fig2=pp.gcf()
c='C4'

for preload in cor_frc:
    # data
#    [ax.plot( cor_frc[preload][ret]['log2lambda'], cor_frc[preload][ret]['log2sigma'], 
#        marker='o', ms=8, lw=0, mew=0.4, markevery=3, mfc='None', **preload_axs[preload]['plotargs']  ) 
#        for ret in cor_frc[preload]]
    [ax2.plot( cor_frc[preload][ret]['lambda_deexp'], adhesion[preload][ret]['sigma'], 
        marker='o', ms=4, lw=0, mew=0.2, markevery=2, mfc='None', 
        c=c,  **preload_axs[preload]['plotargs'], ) 
        for ret in cor_frc[preload]]


#
# De-exponentialized force versus lambda 
#

ax2.set_xlim((0.0, 1.15))
ax2.set_ylim((-2, 15))
ax2.set_xlabel('$\lambda \\xi $', fontsize=22)
ax2.set_ylabel('$\\frac{F}{\lambda N E}$', fontsize=22)
ax2.set_title('N$_\\mathrm{total}$=441')
# legend generation
[ax2.plot([],[], **preload_axs[preload]['plotargs'], marker='o', ms=8, lw=0, mfc='None', 
        c=c, label="$f_\\mathrm{{pre}}=${} L$_m$={}".format(preload,float(dfs[preload]['L_m'])))
        for preload in preload_axs]
ax2.legend(frameon=False)

fig2.savefig("inact_domain_441.pdf")
