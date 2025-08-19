import numpy as np
import pandas as pd
import matplotlib.pyplot as pp
from sklearn.linear_model import LinearRegression

# better to read this from a file
n_feat={0:237, 1:230, 2:240, 3:224, 4:239}
n_total=441
a_total=0.025**2
L_m=5e-3
L_c=11.2e-3
W=L_m/L_c
m=8
series=pd.read_csv("30_5_F_D.csv", engine='python', names=["d","F"])


runs={i:np.array(series)[i*len(np.array(series))//5:(i+1)*len(np.array(series))//5] for i in range(0,5)}
a={r:n_feat[r]/n_total*a_total for r in runs}


# Force-distance curves as measured
fig,ax=pp.subplots()
[ax.plot(runs[r][:,0], runs[r][:,1], ms=3) for r in runs]
ax.set_xlim((5.6,17.5))
ax.set_ylim((-0.45,0.025))
ax.set_xlabel("$d$ (mm)")
ax.set_ylabel("$F$ (mN)")


min_d_idx={r:np.max(np.where(runs[r][:,0]==np.min(runs[r][:,0]))) for r in runs}
diffs={r:np.diff(runs[r][:,1]) for r in runs}

k=np.ones(5)/5
sth_diffs={r:np.convolve(diffs[r],k, mode='same') for r in runs}
adh_idx={r:min_d_idx[r]+np.min(np.where(np.abs(sth_diffs[r][min_d_idx[r]:])<0.001)) for r in runs}
adh_idx_last={r:adh_idx[r]+np.min(np.where(np.max(sth_diffs[r][adh_idx[r]:])==sth_diffs[r][adh_idx[r]:]))+1 for r in runs}

fig1,ax1=pp.subplots()
[ax1.plot(runs[r][:,0], runs[r][:,1], ms=3) for r in runs]
[ax1.plot(runs[r][min_d_idx[r]+1:,0], sth_diffs[r][min_d_idx[r]:],  ls='-', lw=0.5, c='k') for r in runs]
[ax1.plot(runs[r][adh_idx[r]+1,0], sth_diffs[r][adh_idx[r]], marker='o', ms=8) for r in runs]
[ax1.plot(runs[r][adh_idx_last[r],0], runs[r][adh_idx_last[r],1], marker='o', ms=8) for r in runs]

adh={r:runs[r][adh_idx[r]:adh_idx_last[r]] for r in runs}
S={r:np.vstack( [ (adh[r][:,0]-adh[r][0,0])/L_c*1e-3, -1*(adh[r][:,1]-adh[r][0,1])/n_feat[r] ]).transpose() for r in runs}
normF={r:np.vstack( [ (adh[r][:,0]-adh[r][0,0])/L_c*1e-3, -1*(adh[r][:,1]-adh[r][0,1])/n_feat[r]/a[r] ]).transpose() for r in runs}

fig2,ax2=pp.subplots()

#
# obtain modulus level
#
reg = {r:LinearRegression().fit(normF[r][150:300,0].reshape(-1,1), normF[r][150:300,1]) for r in runs}
E_raw = {r:reg[r].coef_ for r in runs}
E = {r:reg[r].coef_*a[r] for r in runs}
[ax2.plot(normF[r][150:300,0], E_raw[r]*normF[r][150:300,0]+reg[r].intercept_, ':k', label=f'$E_{r}={round(E_raw[r][0],1)}$ Pa') for r in runs]
ax2.legend()
ax2.set_xlabel("$d L_c^{-1}$")
ax2.set_ylabel("$F(AN)^{-1}$ (Pa)")

[ax2.plot(normF[r][:,0], normF[r][:,1]*E[r], ms=2, lw=0, marker='o', markevery=3) for r in runs]
ax2.plot(np.linspace(0,1,100), 6.4*np.linspace(0,1,100)**(1.5), '-k', label="$(\\frac{d}{L_C})^{\\frac{3}{2}}$")

#
# 
#
fig3,ax3=pp.subplots()
corrF={r:np.vstack( [normF[r][:,0]*E[r], -1*adh[r][:,1]/(normF[r][:,0]*n_feat[r]*E[r]*(1-np.exp(-normF[r][:,0]/(W))  ))]).transpose() for r in runs}
[ax3.plot(normF[r][:,0], normF[r][:,0]*corrF[r][:,1]*E[r]) for r in runs]
ax3.set_xlabel("$d L_c^{-1}$")
ax3.set_ylabel("$FN^{-1}(1-\exp{(dL_cL_m^{-1}})^{-1})$")
fig3.tight_layout()

fig4,ax4=pp.subplots()
log1F={r:np.vstack([ corrF[r][:,0], -np.log( corrF[r][:,1] )  ]).transpose() for r in runs}
log2F={r:np.vstack([ np.log(log1F[r][np.where(log1F[r][:,1]>0),0]), np.log(log1F[r][np.where(log1F[r][:,1]>0),1])  ]).transpose() for r in runs}

ax4.set_xlabel("$d L_c^{-1} E$")
ax4.set_ylabel("$\log{(\log{( F(ENd(1-\exp{(dL_cL_m^{-1}})^{-1})  )})}$")

# fit coefficients and intercept
log2F_bounds={r:np.where( log2F[r][:-10,0]>-6.3 ) for r in runs}
reg_log={r:LinearRegression().fit( log2F[r][log2F_bounds[r],0][0].reshape(-1,1), log2F[r][log2F_bounds[r],1][0]  )  for r in runs}
reg_slopes={r:reg_log[r].coef_[0] for r in runs}
reg_icpts={r:reg_log[r].intercept_ for r in runs}

sigma={r:np.exp(-reg_icpts[r]/reg_slopes[r]) for r in runs}
[ax4.plot(np.linspace(-6.3, -5.8), reg_slopes[r]*np.linspace(-6.3, -5.8) + reg_icpts[r], ':k', lw=1) for r in runs]
[ax4.plot(log2F[r][:,0], log2F[r][:,1], 'o', mfc='None', label=f'$\sigma={round(sigma[r]*10000)/10000}$ $m={round(reg_slopes[r])}$') for r in runs]
ax4.legend()

fig5,ax5=pp.subplots()
ax5.plot(normF[1][:,0], E[1][0]*normF[1][:,0] * np.exp(-(E[1][0]*normF[1][:,0]/sigma[1])**reg_slopes[1]) * (1-np.exp(-normF[1][:,0]/W)), ms=2, lw=2, c='blue', label='FBM')
ax5.plot(normF[1][:,0], S[1][:,1])
ax5.legend()


figs={fig1:"fig1.pdf", fig2:"fig2.pdf", fig3:"fig3.pdf", fig4:"fig4.pdf", fig5:"fig5.pdf"}
{f.savefig(figs[f]) for f in figs}

#[pp.close(f) for f in [fig3, fig4]]
