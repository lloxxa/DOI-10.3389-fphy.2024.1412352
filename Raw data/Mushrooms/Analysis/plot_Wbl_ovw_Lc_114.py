import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
from sklearn.linear_model import LinearRegression
import pickle


densities=['sample441.pickle', 'sample361.pickle', 'sample114.pickle']

#
#  density361 
#

sets_loaded={}
for p in densities:
    with open(p, 'rb') as f:
        sets_loaded[p]=pickle.load(f)

dfs=sets_loaded['sample114.pickle']

preload_axs={
            4:{ 'plotargs':{'c':'k'}         },
            #6: { 'plotargs':{'c':'r'}         }, 
            16: { 'plotargs':{'c':'g'}         },
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

def cor_frc_finexp(adhesion, E, L_c, L_m, N_att, floor=-6.4):
    print("N={}".format(N_att))
    print("Lc={}".format(L_c))
    print("Lm={}".format(L_m))
    print("E={}".format(E))

    W=L_m/L_c
    cor_frc=pd.DataFrame()
    cor_frc['lambda']= adhesion['lambda']

    cor_frc['lambda.E']= adhesion['lambda']*float(E)
    cor_frc['sigma_deexp']= -adhesion['Normal Force']/(N_att*float(E)*adhesion['lambda']*(1-np.exp(-adhesion['lambda']/W)))
    cor_frc['log1sigma']= -np.log( cor_frc['sigma_deexp']  )

    positive_idx=cor_frc.index[cor_frc['log1sigma']>0]

    cor_frc['log2lambda_raw']= np.log( cor_frc['lambda.E'].loc[positive_idx] )
    cor_frc['log2sigma_raw']= np.log( cor_frc['log1sigma'].loc[positive_idx] )

    cor_frc['log2lambda']=cor_frc['log2lambda_raw'].loc[cor_frc.index[ cor_frc['log2lambda_raw']>-floor  ]]
    cor_frc['log2sigma']=cor_frc['log2sigma_raw'].loc[cor_frc.index[ cor_frc['log2lambda_raw']>-floor  ]]

    #-1*adh[r][:,1]/(normF[r][:,0]*n_feat[r]*E[r]*(1-np.exp(-normF[r][:,0]/(W))  ))]).transpose() for r in runs}
    return(cor_frc)

def reg_Weibull(cor_frc, E, L_c, L_m):
    bounded=pd.DataFrame()
    bounded_idc=cor_frc.index[(cor_frc['log2sigma']>-1.0) & (cor_frc['log2sigma']<0.3) ]
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

#    fix, ax=pp.subplots()
#    [ax.plot(cor_frc[preload][ret]['log2lambda'], cor_frc[preload][ret]['log2sigma'], marker='o', ms=3) for ret in adhesion[preload]]
#    ax.set_title('{}'.format(preload))

    pars[preload]['reg']={ret: 
            reg_Weibull(cor_frc[preload][ret], pars[preload]['moduli'][ret], 
                pars[preload]['L_c'][ret], float(dfs[preload]['L_m'])) 
            for ret in adhesion[preload]}
    pars[preload]['m']={ret: round(pars[preload]['reg'][ret]['slope']) 
            for ret in adhesion[preload]}
    pars[preload]['sigma_0']={ret:np.exp(-pars[preload]['reg'][ret]['intercept']/pars[preload]['reg'][ret]['slope']) 
            for ret in adhesion[preload]}


fig, ax=pp.subplots(figsize=(8,6))
fig2, ax2=pp.subplots(figsize=(8,6))
fig3, ax3=pp.subplots(figsize=(8,6))

for preload in cor_frc:
    # data
    [ax.plot( cor_frc[preload][ret]['log2lambda'], cor_frc[preload][ret]['log2sigma'], 
        marker='o', ms=8, lw=0, mew=0.4, markevery=3, mfc='None', **preload_axs[preload]['plotargs']  ) 
        for ret in cor_frc[preload]]
    [ax2.plot( adhesion[preload][ret]['lambda'], cor_frc[preload][ret]['sigma_deexp'], 
        marker='o', ms=4, lw=0, mew=0.2, markevery=2, mfc='None', **preload_axs[preload]['plotargs']  ) 
        for ret in cor_frc[preload]]
    [ax3.plot( adhesion[preload][ret]['lambda'], adhesion[preload][ret]['sigma'],
        marker='o', ms=6, lw=0.2, mew=0.2, markevery=2, mfc='None', **preload_axs[preload]['plotargs']  ) 
        for ret in cor_frc[preload]]

    # models
    [ax.plot( pars[preload]['reg'][ret]['x_model'], pars[preload]['reg'][ret]['y_model'], 
        c=preload_axs[preload]['plotargs']['c'], lw=0.5 ) for ret in pars[preload]['reg']]
    [ax2.plot( adhesion[preload][ret]['lambda'], pars[preload]['reg'][ret]['sigma_deexp_model'], 
         c=preload_axs[preload]['plotargs']['c'], lw=0.5 ) for ret in pars[preload]['reg']]

#
# Double logarithm of the de-exponentialized force versus E.lambda
#

ax.set_title('N$_\\mathrm{total}$=114')
ax.set_xlim((-6.0,-5.1))
ax.set_ylim((-3,2))
ax.set_xlabel('$\log{ E \lambda }$', fontsize=22)
ax.set_ylabel('$ \log{ ( \log{ ( - \\frac{F}{\lambda N E (1-\exp{(-\lambda W^{-1})}) } ) } ) }   $', fontsize=22)
# legend generation
[ax.plot([],[], **preload_axs[preload]['plotargs'], marker='o', ms=8, lw=0, mfc='None', 
        label="$f_\\mathrm{{pre}}=${}".format(preload)) 
        for preload in preload_axs]
ax.legend(frameon=False)

#
# De-exponentialized force versus lambda 
#

ax2.set_xlim((0.15, 1.05))
ax2.set_ylim((0, 2.25))
ax2.set_xlabel('$\lambda$', fontsize=22)
ax2.set_ylabel('$\\frac{F}{\lambda N E (1-\exp{(-\lambda W^{-1})})}$', fontsize=22)
ax2.set_title('N$_\\mathrm{total}$=114')
# legend generation
[ax2.plot([],[], **preload_axs[preload]['plotargs'], marker='o', ms=8, lw=0, mfc='None', 
        label="$f_\\mathrm{{pre}}=${}".format(preload)) 
        for preload in preload_axs]
ax2.legend(frameon=False)

#
# Sigma versus lambda
#

#ax3.set_xlim((0.15, 1.05))
#ax3.set_ylim((0, 2.25))
ax3.set_xlabel('$\lambda$', fontsize=22)
ax3.set_ylabel('$\\frac{F}{NA}$ (Pa)', fontsize=22)
ax3.set_title('N$_\\mathrm{total}$=114')
# legend generation
[ax3.plot([],[], **preload_axs[preload]['plotargs'], marker='o', ms=8, lw=0.2, mfc='None', 
        label="$f_\\mathrm{{pre}}=${}".format(preload)) 
        for preload in preload_axs]
ax3.legend(frameon=False)

fig.tight_layout()
fig.savefig("S114_log2sigma.pdf")
fig2.tight_layout()
fig2.savefig("S114_sigma_deexp.pdf")
fig3.tight_layout()
fig3.savefig("S114_sigma_.pdf")# axs.set_ylim((-0.5,0.1))
# axs.set_xlabel('$d$ (mm)')
# axs.set_ylabel('$F$ (N)')
# fig.tight_layout()
# fig.savefig('Sample441.pdf')
# 



