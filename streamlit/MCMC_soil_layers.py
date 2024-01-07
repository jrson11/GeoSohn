# =============================================================================
# Name: MCMC_soil_layers.py
# Authour: Jung.Sohn
# Date: 05Jan24
# All rights reserved
# =============================================================================
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
import streamlit as st

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

# Title
st.title("MCMC simulation for stratigraphic model of soil layers")

# =============================================================================
# Import raw data
df_Raw = pd.read_csv('https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_MCMC_soil_layers/UW_PCPT_Robertson2010.csv')
cols = df_Raw.columns   # DataFrame show have two columns, i.e., Z and X
z_header = cols[0]
x_header = cols[1]
zmin = min(df_Raw[z_header])  
zmax = max(df_Raw[z_header])  
xavg = round(np.mean(df_Raw[x_header]))  
xmin = round(min(df_Raw[x_header])*0.9)  
xmax = round(max(df_Raw[x_header])*1.1)  

## Interporation
dz = 0.2  # interval of depth  
zq = np.arange(dz,zmax,dz)    # interpolated depth 
xq = np.interp(zq, df_Raw[z_header], df_Raw[x_header])    # interpolated data  
nq = len(zq)    # No. of interpolated points

## Streamlit
st.write("Average value of X:", xavg)
st.write("Interval of depth Z:", dz)

# =============================================================================
# Make Initial stratigraphy model

## Setup
#nk = 5  # No. of layers  
nk = int(st.number_input("No. of soil layers", min_value=2, value=5, step=1))
x1_ini = np.ones(nk)*xavg*0.95       # X value at Top of each layer 
x2_ini = np.ones(nk)*xavg*1.05       # X value at Bottom of each layer  
zi_ini = list(np.linspace(0,nq-1,nk+1).astype(int))     # depth index

## Define FWD
def FWD(zq,zi,x1,x2):
    zi1 = zi[0:-1]    # depth index of Top layer
    zi2 = zi[1:]      # depth index of Bottom layer    
    z1 = []
    z2 = []
    x_dummy = []
    z_dummy = []
    for i in range(nk): # To check each layer
        z1.append(round(zq[zi1[i]],3))
        z2.append(round(zq[zi2[i]],3))
        x_dummy.append(x1[i])
        x_dummy.append(x2[i])
        z_dummy.append(round(zq[zi1[i]],3))
        z_dummy.append(round(zq[zi2[i]-1],3))
    z_dummy[-1] = zq[-1]
    yq = np.interp(zq, z_dummy, x_dummy)
    return yq

xq_ini = FWD(zq,zi_ini,x1_ini,x2_ini)
xq_obs = xq

## Plot to check
def fig_ini_UW():
    fig,ax = plt.subplots(1,2, figsize=(9,6), dpi=100)
    #
    ax[0].plot(df_Raw[x_header],df_Raw[z_header],'.', label='Raw data',alpha=0.2)  
    ax[0].plot(xq,zq,'k--', label='Interpolated')
    ax[0].set_title('Observed vertical profile')
    
    ax[1].plot(xq,zq,'k--', label='Interpolated')
    ax[1].plot(xq_ini,zq,'r--', label='Initial guess')
    ax[1].set_title('Initial stratigraphic model')
    
    # Label    
    for i in range(2):
        ax[i].set_xlim([xmin,xmax])
        ax[i].set_ylim([zmax,0])
        ax[i].set_xlabel('UW (kN/m2)')
        ax[i].set_ylabel('Depth (m)')
        ax[i].grid(linestyle='dotted')
        ax[i].minorticks_on()
        ax[i].legend(loc=3, fancybox=True, shadow=True, fontsize=10, ncol=1)
    
    # Add patch
    for j in range(nk):
        width = xmax-xmin
        height = zq[zi_ini[j+1]]-zq[zi_ini[j]]
        ax[1].add_patch(patches.Rectangle((xmin,zq[zi_ini[j]]),width,height,color='C'+str(j),alpha=0.1))
    
    plt.tight_layout()
    return fig

if st.button('1st click:Generate initial model plot'):
    fig=fig_ini_UW()
    st.pyplot(fig)


# =============================================================================
# MCMC

## Setup
ns = int(2e4)   # No. of iteration
nb = int(1e4)  # burn-in point (draft)
cv = 0.001
MCx1 = np.zeros([ns,nk])
MCx2 = np.zeros([ns,nk])
MCzi = np.zeros([ns,nk+1]).astype(int)
MCzq = np.zeros([ns,nk+1])
MCyErr = np.zeros(ns)

## Initial samples
MCx1[0] = x1_ini
MCx2[0] = x2_ini
MCzi[0] = zi_ini
MCzq[0] = zq[zi_ini]
MCyErr[0] = np.linalg.norm(xq_ini - xq_obs)

## Function
def lglkl(Y_obs,Y_mdl,sig):
    n = len(Y_obs)
    logLK = -n/2*np.log(2*np.pi*sig**2) + -1/(2*sig**2)*sum((Y_obs-Y_mdl)**2)
    return logLK


## Iteration
naccept = 0
nreject = 0
for i in range(ns-1):
    j = i+1 # FYI, counting should start from 2nd idex (1)
    
    ## Current model
    x1_cur = MCx1[i]
    x2_cur = MCx2[i]
    zi_cur = list(MCzi[i])
    #
    xq_cur = FWD(zq,zi_cur,x1_cur,x2_cur)
    s_cur = np.std(xq_cur - xq_obs)
    
    ## Propose a candidate model
    # Take old values first
    x1_prp = x1_cur
    x2_prp = x2_cur
    zi_prp = zi_cur

    u = np.random.rand()
    if u < 0.4:     # change one layer X properties
        idx = np.random.randint(0,nk) 
        x1_old = x1_prp[idx]
        x1_new = np.random.normal(x1_old,cv*x1_old)
        x2_old = x2_prp[idx]
        x2_new = np.random.normal(x2_old,cv*x2_old)        
        x1_prp[idx] = x1_new
        x2_prp[idx] = x2_new
        
    elif u < 0.8:   # change one layer Z properties   
        zi_prp = [int(np.random.normal(loc=elem, scale=5)) for elem in zi_cur]
        zi_prp[0] = zi_cur[0]
        zi_prp[-1] = zi_cur[-1]
        zi_prp = np.sort(zi_prp)
            
    else:
        x1_prp = np.random.normal(x1_cur,xavg*cv)
        x2_prp = np.random.normal(x2_cur,xavg*cv)
        
    xq_prp = FWD(zq,zi_prp,x1_prp,x2_prp)
    s_prp = np.std(xq_prp - xq_obs)
    
    ## Bayesian
    ## -- Likelihood
    log_lik_prp = lglkl(xq_prp,xq_obs,s_prp)
    log_lik_cur = lglkl(xq_cur,xq_obs,s_cur)
    logr_lik = log_lik_prp - log_lik_cur
    
    ## -- Prior
    logr_pri = 0
    
    ## -- Posterior
    logr_final = logr_lik + logr_pri
    bay_alpha = min(1,np.exp(logr_final))    
    #bay_alpha = 0.5
    
    ## MH sampling
    u = np.random.rand()
    if u < bay_alpha: # accept
        MCx1[j] = x1_prp
        MCx2[j] = x2_prp
        MCzi[j] = zi_prp
        MCzq[j] = zq[zi_prp]
        MCyErr[j] = np.linalg.norm(xq_prp - xq_obs)
        naccept = naccept + 1
        print('Iteration Number = '+str(j)+' -Accept: bay_alpha = '+str(round(bay_alpha,2)))
    else:   # reject
        MCx1[j] = x1_cur
        MCx2[j] = x2_cur
        MCzi[j] = zi_cur
        MCzq[j] = zq[zi_cur]
        MCyErr[j] = np.linalg.norm(xq_cur - xq_obs)
        nreject = nreject + 1
        print('Iteration Number = '+str(j)+' -Reject: bay_alpha = '+str(round(bay_alpha,2)))

## Plot to check
def fig_y_err():
    fig,ax = plt.subplots(2,1, figsize=(9,6), dpi=100)
    #
    ax[0].plot(MCyErr/MCyErr[0]*100)
    ax[0].plot([nb,nb],[min(MCyErr/MCyErr[0]*100),100],'r--', label='Burn-in period')
    ax[0].set_ylabel('Misfit error (%)')
    ax[0].legend(loc=0, fancybox=True, shadow=True, fontsize=10, ncol=1)
    
    ax[1].plot(MCx1, '-')
    ax[1].plot([nb,nb],[MCx1.min().min(),MCx1.max().max()],'r--', label='Burn-in period')
    ax[1].set_ylabel('Properties of each layer')
    
    for i in range(2):
        ax[i].set_xlabel('Iterations')
        ax[i].grid(linestyle='dotted')
        ax[i].minorticks_on()
    plt.tight_layout()

if st.button('2nd click:Generate iteration plot'):
    fig=fig_y_err()
    st.pyplot(fig)
