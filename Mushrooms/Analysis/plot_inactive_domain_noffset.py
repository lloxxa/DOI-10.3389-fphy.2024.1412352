import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
import matplotlib.pyplot as pp
import pickle
import matplotlib as mp
import matplotlib.colors as cs
import matplotlib.cm as cm
import nutools as nu
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


pickles=[   
            'sample441.pickle', 
            'sample361.pickle', 
            'sample114.pickle'
        ]

#
#  density 361 
#

sets_loaded={}
for p in pickles:
    with open(p, 'rb') as f:
        sets_loaded[p]=pickle.load(f)

densities={ 
'sample114.pickle':{
#            4:{ 'plotargs':{}         },
#            #6: { 'plotargs':{}         },
            16: { 'plotargs':{}         },
        },
'sample361.pickle':{
#            7.5: { 'plotargs':{}    }, 
#            10:  { 'plotargs':{}    },
#            15:  { 'plotargs':{}    }, 
#            20:  { 'plotargs':{}    },
#            25:  { 'plotargs':{} },  
#            30:  { 'plotargs':{}    },
            35:  { 'plotargs':{}    },
        },
'sample441.pickle':{
            #6: { 'plotargs':{}     },
#            12:{ 'plotargs':{}      },
#            18: { 'plotargs':{}     },
#            24: { 'plotargs':{}     },
#            30: { 'plotargs':{}  },
            36: { 'plotargs':{}     },
            #42: { 'plotargs':{}    }
        },
}

A_total=0.025**2

lims={ 


'sample114.pickle':{

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

floors={ 'sample441.pickle':-6.6, 
        'sample361.pickle':-6.4 , 
        'sample114.pickle':-6.4 }

overwrite_Lc=True

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
                dfs[preload]['N_attached'].iloc[0,int(ret-1)], floors[dens] ) 
                for ret in adhesion[preload]  }

        print("density:{}, preload:{}".format(dens, preload))
        pars[preload]['reg']={ret: 
            nu.reg_Weibull(cor_frc[preload][ret], pars[preload]['moduli'][ret], 
                pars[preload]['L_c'][ret], float(dfs[preload]['L_m']), lims=lims[dens][preload][ret]) 
            for ret in adhesion[preload]}

        pars[preload]['m']={ret: round(pars[preload]['reg'][ret]['slope'], 2) 
                for ret in adhesion[preload]}
        pars[preload]['sigma_0']={ret:np.exp(-pars[preload]['reg'][ret]['intercept']/pars[preload]['reg'][ret]['slope']) 
                for ret in adhesion[preload]}

    cor_frcs[dens]=cor_frc
    pars_dens[dens]=pars


fig2, (ax2, ax1)=pp.subplots(1,2,figsize=(12,6), gridspec_kw=gridspec_kw)# sharey='row', sharex='row')
axs={'sample441.pickle':ax1, 'sample361.pickle':ax1, 'sample114.pickle':ax1}
ax1.set_ylabel('$\\frac{F}{N E}$', fontsize=22)
[ax.set_xlabel('$\lambda \\xi $', fontsize=22) for ax in (ax1,)]
ax1.set_xlim((-0.1, 1.2))
ax1.set_ylim((-0.1, 1.55))


clrs=pp.get_cmap("inferno")
clr=lambda n,mina,maxa: clrs(round(255* ( n / (maxa-mina))  ))
minf=4
maxf=50

marks=  {'sample114.pickle':'o', 'sample361.pickle':'^', 'sample441.pickle':'s'}
#offset= {'sample114.pickle':0.6, 'sample361.pickle':0.3, 'sample441.pickle':0.0}
offset= {'sample114.pickle':0.0, 'sample361.pickle':0.0, 'sample441.pickle':0.0}
retmap=lambda ret: 1 if ret==0.5 else 0.5
msmap=lambda ret: 6 if ret==2 else 1


########### RIGHTHAND PANEL
for dens in cor_frcs:
    cor_frc=cor_frcs[dens]
    preload_axs=densities[dens]
    for preload in cor_frc:
    #    [ax.plot( cor_frc[preload][ret]['log2lambda'], cor_frc[preload][ret]['log2sigma'], 
    #        marker='o', ms=8, lw=0, mew=0.4, markevery=3, mfc='None', **preload_axs[preload]['plotargs']  ) 
    #        for ret in cor_frc[preload]]
        nu.mrks.reset()
        [axs[dens].plot( cor_frc[preload][ret]['lambda_deexp'], cor_frc[preload][ret]['f_by_NE']+offset[dens], 
            marker=nu.mrks.next(), markevery=20, ms=msmap(ret), lw=retmap(ret), mew=0.8, mec='0.05', mfc='None', 
            c=clr(preload,minf,maxf), 
            **preload_axs[preload]['plotargs']  ) 
            for ret in cor_frc[preload]]

        [axs[dens].plot( cor_frc[preload][ret]['lambda_deexp'], 
            pars_dens[dens][preload]['reg'][ret]['sigma_model']+offset[dens], 
            c=clr(preload,minf,maxf), lw=0 ) for ret in pars_dens[dens][preload]['reg']]


#
# De-exponentialized force versus lambda 
#

# build legend for right figure
legend_lines=[

            Line2D([0],[0],color='0.2', lw=1.0, marker='o', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='^', mfc='None', ms=8),
            Line2D([0],[0],color='0.2', lw=1.0, marker='s', mfc='None', ms=8),

            ]
ax1.legend(legend_lines, [114,361,441])


# add text to explain the offset
ax1.text(-0.05,0.22,'+0.3')
ax1.text(-0.05,0.50,'+0.6')
ax1.yaxis.set_label_coords(0.0,0.55)
pp.setp(ax1.yaxis.get_label(), backgroundcolor="white")



# new fig

axs={'sample441.pickle':ax2, 'sample361.pickle':ax2, 'sample114.pickle':ax2}
ax2.set_ylabel('$m^{-1} \log{ ( \log{ ( - \\frac{F}{\lambda N E (1-\exp{(-\lambda W^{-1})}) } ) } ) }   $', fontsize=22)
ax2.set_xlabel('$\log{ E \lambda }$', fontsize=22)
#ax2.set_xlim((-6.5, -5.50))
#ax2.set_ylim((-0.6, 0.15))



marks=  {'sample114.pickle':'o', 'sample361.pickle':'^', 'sample441.pickle':'s'}
retmap=lambda ret: 1 if ret==1 else 0.5
#msmap=lambda ret: 8 if ret==5 else 0

for dens in cor_frcs:
    cor_frc=cor_frcs[dens]
    preload_axs=densities[dens]
    for preload in cor_frc:
    #    [ax.plot( cor_frc[preload][ret]['log2lambda'], cor_frc[preload][ret]['log2sigma'], 
    #        marker='o', ms=8, lw=0, mew=0.4, markevery=3, mfc='None', **preload_axs[preload]['plotargs']  ) 
    #        for ret in cor_frc[preload]]
        nu.mrks.reset()
        [axs[dens].plot( cor_frc[preload][ret]['log2lambda'], 
            (cor_frc[preload][ret]['log2sigma']),
            marker=nu.mrks.next(), markevery=1, ms=8, mew=retmap(ret), lw=0, mfc='None', 
            mec=clr(preload,minf,maxf),label=int(ret),
            **preload_axs[preload]['plotargs']  ) 
            for ret in cor_frc[preload]]
        [axs[dens].plot( pars_dens[dens][preload]['reg'][ret]['x_model'], 
            (pars_dens[dens][preload]['reg'][ret]['y_model']),
            c=clr(preload,minf,maxf), lw=retmap(ret)/2 ) for ret in pars_dens[dens][preload]['reg']]

#ax2.legend()

## build legend for right figure
#legend_lines=[
#
#            Line2D([0],[0],color='0.2', lw=1.0, marker='o', mfc='None', ms=8),
#            Line2D([0],[0],color='0.2', lw=1.0, marker='^', mfc='None', ms=8),
#            Line2D([0],[0],color='0.2', lw=1.0, marker='s', mfc='None', ms=8),
#
#            ]
#
#ax2.legend( legend_lines, [114,361,441] )

# colorbar
cb=fig2.colorbar(cm.ScalarMappable(norm=cs.Normalize(maxf,minf), cmap=clrs), 
                ax=ax1, ticks=[10,20,30,40], pad=0.01)
cb.ax.tick_params(direction='out')


fig2.tight_layout()
fig2.savefig("log2.pdf")


fig3,ax3=pp.subplots()
axs={'sample441.pickle':ax3, 'sample361.pickle':ax3, 'sample114.pickle':ax3}
marks=  {'sample114.pickle':'o', 'sample361.pickle':'^', 'sample441.pickle':'s'}
retmap=lambda ret: 1 if ret==1 else 0
#msmap=lambda ret: 8 if ret==5 else 0

for dens in cor_frcs:
    cor_frc=cor_frcs[dens]
    preload_axs=densities[dens]
    for preload in cor_frc:
    #    [ax.plot( cor_frc[preload][ret]['log2lambda'], cor_frc[preload][ret]['log2sigma'], 
    #        marker='o', ms=8, lw=0, mew=0.4, markevery=3, mfc='None', **preload_axs[preload]['plotargs']  ) 
    #        for ret in cor_frc[preload]]
        [axs[dens].plot( cor_frc[preload][ret]['lambda'], 
            (cor_frc[preload][ret]['sigma']),
             markevery=2, marker=nu.mrks.next(), ms=8, mew=retmap(ret), lw=0, mfc='None', mec=clr(preload,minf,maxf),
            **preload_axs[preload]['plotargs']  ) 
            for ret in cor_frc[preload]]
        [axs[dens].plot( np.arange(0.35,0.45,0.01), 
            np.arange(0.35,0.45,0.01)*pars_dens[dens][preload]['moduli'][ret]/pars_dens[dens][preload]['A_att'][ret],
            c=clr(preload,minf,maxf), lw=retmap(ret)/2 ) for ret in pars_dens[dens][preload]['moduli']]

fig3.tight_layout()
