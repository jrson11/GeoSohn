# =============================================================================
# Name: MCMC_soil_layers.py
# Authour: Jung.Sohn
# Date: 07Jan24
# All rights reserved
# =============================================================================
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
import streamlit as st
from scipy.stats import norm

# 문제점(07Jan24): --> 해결완료(10Jan24)
# nk 값이 바뀔 때 플로팅에서 업데이트가 안됨.
# 코드 자체의 문제가 아니라 Streamlit 에 적용시킬때의 문제

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()


# Title
st.title("Stratigraphic Soil Layer Modeling")
st.write('- Purpose: Uncertainty quantification')
st.write('- Method: MCMC calibration')

# =============================================================================
# Import raw data
st.subheader(':floppy_disk: Step 1: Import vertical soil data')

df_Raw = pd.read_csv('https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_MCMC_soil_layers/UW_PCPT_Robertson2010.csv')
st.write('Imported data: Unit Weight derived from in-situ CPT (Robertson,2010)')
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
st.write("- Average value of X:", xavg)
st.write("- Interval of depth Z:", dz)

# =============================================================================
# Make Initial stratigraphy model

## Setup
#nk = 5  # No. of layers  
nk = int(st.number_input("No. of soil layers", min_value=2, value=5, step=1))
x1_ini = np.ones(nk)*xavg*0.95       # X value at Top of each layer 
x2_ini = np.ones(nk)*xavg*1.05       # X value at Bottom of each layer  
zi_ini = list(np.linspace(0,nq-1,nk+1).astype(int))     # depth index
zq_ini = zq[zi_ini]
std_diff_zi_ini = np.std(np.diff(zi_ini))   # To use in Bayesian prior

## Define FWD
def FWD(zq,zi,x1,x2):
    zi1 = zi[0:-1]    # depth index of Top layer
    zi2 = zi[1:]      # depth index of Bottom layer    
    z1 = []
    z2 = []
    x_dummy = []
    z_dummy = []
    for i in range(len(x1)): # To check each layer
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
    
    # 1st plot shows raw data and interpolation result
    ax[0].plot(df_Raw[x_header],df_Raw[z_header],'.', label='Raw data',alpha=0.2)  
    ax[0].plot(xq,zq,'k--', label='Interpolated')
    ax[0].set_title('Observed vertical profile')
    
    # 2nd plot shows the first soil layer model as initial guess
    ax[1].plot(xq,zq,'k--', label='Interpolated')
    ax[1].plot(xq_ini,zq,'r--', label='Initial guess')
    ax[1].set_title('Initial stratigraphic model')
    
    # Add patch to the 2nd plot
    for j in range(nk):
        width = xmax-xmin
        height = zq[zi_ini[j+1]]-zq[zi_ini[j]]
        ax[1].add_patch(patches.Rectangle((xmin,zq[zi_ini[j]]),width,height,color='C'+str(j),alpha=0.1))
        
    # Label    
    for i in range(2):
        ax[i].set_xlim([xmin,xmax])
        ax[i].set_ylim([zmax,0])
        ax[i].set_xlabel(x_header)
        ax[i].set_ylabel(z_header)
        ax[i].grid(linestyle='dotted')
        ax[i].minorticks_on()
        ax[i].legend(loc=3, fancybox=True, shadow=True, fontsize=10, ncol=1)
    
    # Finalize
    plt.tight_layout()
    return fig

if st.button('1st click: plot initial model'):
    fig=fig_ini_UW()
    st.pyplot(fig)


# =============================================================================
# MCMC
st.subheader(':desktop_computer: Step 2: Execute MCMC simulation')

## Setup
#ns = int(0.5e4)   # No. of iteration
ns = int(st.number_input("No. of iterations", min_value=1000, value=5000, step=1000))
nb = int(ns/2)  # burn-in point (draft)
cv = 0.001

# 세션 상태 초기화
def memory_MCMC(ns,nk,x1_ini,x2_ini,zi_ini,zq_ini):
    st.session_state.MCx1 = np.zeros([ns,nk])
    st.session_state.MCx2 = np.zeros([ns,nk])
    st.session_state.MCzi = np.zeros([ns,nk+1]).astype(int)
    st.session_state.MCzq = np.zeros([ns,nk+1])
    st.session_state.MCyErr = np.zeros(ns)

    st.session_state.MCx1[0] = x1_ini
    st.session_state.MCx2[0] = x2_ini
    st.session_state.MCzi[0] = zi_ini
    st.session_state.MCzq[0] = zq_ini
    st.session_state.MCyErr[0] = np.linalg.norm(xq_ini - xq_obs)

    return st.session_state.MCx1,st.session_state.MCx2,st.session_state.MCzi,st.session_state.MCzq,st.session_state.MCyErr

if 'MCx1' not in st.session_state:
    st.session_state.MCx1 = np.zeros([ns,nk])
    st.session_state.MCx2 = np.zeros([ns,nk])
    st.session_state.MCzi = np.zeros([ns,nk+1]).astype(int)
    st.session_state.MCzq = np.zeros([ns,nk+1])
    st.session_state.MCyErr = np.zeros(ns)

    st.session_state.MCx1[0] = x1_ini
    st.session_state.MCx2[0] = x2_ini
    st.session_state.MCzi[0] = zi_ini
    st.session_state.MCzq[0] = zq[zi_ini]
    st.session_state.MCyErr[0] = np.linalg.norm(xq_ini - xq_obs)
#st.write("No. of MCMC iteration:", ns)

## Function
def lglkl(Y_obs,Y_mdl,sig):
    n = len(Y_obs)
    logLK = -n/2*np.log(2*np.pi*sig**2) + -1/(2*sig**2)*sum((Y_obs-Y_mdl)**2)
    return logLK

## Iteration
def run_MCMC(MCx1,MCx2,MCzi,MCzq,MCyErr):
    naccept = 0
    nreject = 0
    for i in range(ns-1):
        j = i+1 # FYI, counting should start from 2nd index (1)
    
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
        std_diff_zi_prp = np.std(np.diff(zi_prp))
        std_diff_zi_cur = np.std(np.diff(zi_cur))
        log_pri_prp = np.log(norm.pdf(std_diff_zi_prp, std_diff_zi_ini, 5))
        log_pri_cur = np.log(norm.pdf(std_diff_zi_cur, std_diff_zi_ini, 5))
        logr_pri = log_pri_prp - log_pri_cur
        #logr_pri = 0
    
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
            #print('Iteration Number = '+str(j)+' -Accept: bay_alpha = '+str(round(bay_alpha,2)))
        else:   # reject
            MCx1[j] = x1_cur
            MCx2[j] = x2_cur
            MCzi[j] = zi_cur
            MCzq[j] = zq[zi_cur]
            MCyErr[j] = np.linalg.norm(xq_cur - xq_obs)
            nreject = nreject + 1
            #print('Iteration Number = '+str(j)+' -Reject: bay_alpha = '+str(round(bay_alpha,2)))
        print('Iteration Number = '+str(j)+' / '+str(ns))

    return MCx1,MCx2,MCzi,MCzq,MCyErr

if st.button('2nd click: run MCMC iteration'):
    #MCx1,MCx2,MCzi,MCzq,MCyErr = run_MCMC(MCx1,MCx2,MCzi,MCzq,MCyErr)
    st.session_state.MCx1, st.session_state.MCx2, st.session_state.MCzi, st.session_state.MCzq, st.session_state.MCyErr = memory_MCMC(ns,nk,x1_ini,x2_ini,zi_ini,zq_ini)
    st.session_state.MCx1, st.session_state.MCx2, st.session_state.MCzi, st.session_state.MCzq, st.session_state.MCyErr = run_MCMC(st.session_state.MCx1, st.session_state.MCx2, st.session_state.MCzi, st.session_state.MCzq, st.session_state.MCyErr)
    st.write('MCMC completed')

## Plot to check
st.subheader(':chart_with_upwards_trend: Step 3: Check convergence')

def fig_y_err():
    fig,ax = plt.subplots(2,1, figsize=(9,6), dpi=100)
    
    # 1st plot shows decreasing misfit error during MCMC iteration
    ax[0].plot(st.session_state.MCyErr/st.session_state.MCyErr[0]*100)
    ax[0].plot([nb,nb],[min(st.session_state.MCyErr/st.session_state.MCyErr[0]*100),100],'r--', label='Burn-in period')
    ax[0].set_ylabel('Misfit error (%)')
    ax[0].legend(loc=0, fancybox=True, shadow=True, fontsize=10, ncol=1)
    
    # 2nd plot shows convergence of variable at each layer
    ax[1].plot(st.session_state.MCx1, '-')
    ax[1].plot([nb,nb],[st.session_state.MCx1.min().min(),st.session_state.MCx1.max().max()],'r--', label='Burn-in period')
    ax[1].set_ylabel('Properties of each layer')
    
    # Label
    for i in range(2):
        ax[i].set_xlabel('Iterations')
        ax[i].grid(linestyle='dotted')
        ax[i].minorticks_on()
        
    # Finalize
    plt.tight_layout()
    return fig

if st.button('3nd click: plot convergence'):
    fig=fig_y_err()
    st.pyplot(fig)

    
# =============================================================================
# Post-processing
st.subheader(':bar_chart: Step 4: Plot the results')

## Average after burn-in point
x1_mean = np.mean(st.session_state.MCx1[nb:], axis=0)
x2_mean = np.mean(st.session_state.MCx2[nb:], axis=0)
zi_mean = np.mean(st.session_state.MCzi[nb:], axis=0).astype(int)
zq_mean = np.mean(st.session_state.MCzq[nb:], axis=0)
xq_mean = FWD(zq,zi_mean,x1_mean,x2_mean)

## Std after burn-in point
x1_std = np.std(st.session_state.MCx1[nb:], axis=0)
x2_std = np.std(st.session_state.MCx2[nb:], axis=0)
zi_std = np.std(st.session_state.MCzi[nb:], axis=0)
zq_std = np.std(st.session_state.MCzq[nb:], axis=0)


def fig_realizations():
    fig,ax = plt.subplots(1,2, figsize=(9,6), dpi=100)
    
    # 1st plot shows vertical realizations
    ax[0].plot(df_Raw[x_header],df_Raw[z_header],'.', label='Raw data',alpha=0.2)  
    ax[0].plot(xq_ini,zq,'r--', label='Initial guess')
    ax[0].set_title('Estimated stratigraphic model')
    
    # Plot realizations in the 1st plot
    for i in np.arange(nb,ns,50):
        x1_temp = st.session_state.MCx1[nb,:]
        x2_temp = st.session_state.MCx2[nb,:]
        zi_temp = st.session_state.MCzi[nb,:]
        xq_temp = FWD(zq,zi_temp,x1_temp,x2_temp)
        ax[0].plot(xq_temp,zq,color='y',alpha=0.1,linewidth=5)
    ax[0].plot(xq_temp,zq,color='y',label='Realizations',alpha=0.1)
    ax[0].plot(xq_mean,zq,'k-', label='Final estimation')
    ax[0].legend(loc=3, fancybox=True, shadow=True, fontsize=10, ncol=1)
    
    # Label of 1st plot
    ax[0].set_xlabel(x_header)
    ax[0].set_ylabel(z_header)
    ax[0].set_xlim([xmin,xmax])
    ax[0].set_ylim([zmax,0])    
    
    # Add patch in the 1st plot
    for j in range(nk):
        width = xmax-xmin
        height = zq[zi_mean[j+1]]-zq[zi_mean[j]]
        ax[0].add_patch(patches.Rectangle((xmin,zq[zi_mean[j]]),width,height,color='C'+str(j),alpha=0.1))
    
    # 2nd plot shows histogram in vertical direction
    for j in range(nk-1):
        ax[1].hist(st.session_state.MCzq[nb:,j+1], bins=5, density=True, orientation='horizontal',alpha=0.6, color='C'+str(j+1), edgecolor='k', label="layer "+str(j+2));
        ax[1].text(1,zq_mean[j+1],'mean = '+str(round(zq_mean[j+1],2)))
        ax[1].text(2.2,zq_mean[j+1],'std = '+str(round(zq_std[j+1],2)))
    
    # Label of 2nd plot
    ax[1].set_xlabel('Probability Density')
    ax[1].set_ylabel(z_header)
    ax[1].set_title('Histograms of layer depths')
    ax[1].set_ylim([zmax,0])
    ax[1].set_xlim([0,4])
    ax[1].legend(loc=3, fancybox=True, shadow=True, fontsize=10, ncol=1)
    
    # Label 1st and 2nd plots
    for i in range(2):
        ax[i].grid(linestyle='dotted')
        ax[i].minorticks_on()
        
    # Finalize
    plt.tight_layout()
    return fig

st.write("- Visualization")

if st.button('4th click: plot realizations'):
    fig=fig_realizations()
    st.pyplot(fig)


def fig_hist():
    fig,ax = plt.subplots(2,nk, figsize=(9,6), dpi=100)
    
    # sub column number = nk, and raw number = 2 (top and bottom)
    for i in range(nk):
        # Histogram
        ax[0,i].hist(st.session_state.MCx1[nb:,i], bins=10, density=True, alpha=0.6, color='C'+str(i), edgecolor="C0", label=str(i+1)+"th layer");
        ax[1,i].hist(st.session_state.MCx2[nb:,i], bins=10, density=True, alpha=0.6, color='C'+str(i), edgecolor="C0", label=str(i+1)+"th layer");
        
        # Center line
        ax[0,i].plot([x1_mean[i],x1_mean[i]],[0,4],'r--')
        ax[1,i].plot([x2_mean[i],x2_mean[i]],[0,4],'r--')
        
        # Text mean and std
        ax[0,i].set_title(str(i+1)+"th layer")
        ax[0,i].text(x1_mean[i]*0.99,3.5,'mean = '+str(round(x1_mean[i],1)))
        ax[0,i].text(x1_mean[i]*0.99,3.0,'std = '+str(round(x1_std[i],3)))
        ax[1,i].text(x2_mean[i]*0.99,3.5,'mean = '+str(round(x2_mean[i],1)))
        ax[1,i].text(x2_mean[i]*0.99,3.0,'std = '+str(round(x2_std[i],3)))
        
        # Label
        ax[0,i].set_xlabel(x_header+'(Top)')
        ax[1,i].set_xlabel(x_header+'(Bottom)')
        ax[0,i].set_ylim([0,4])
        ax[1,i].set_ylim([0,4])
        
    ax[0,0].set_ylabel('Probability Density')
    ax[1,0].set_ylabel('Probability Density')
        
    plt.tight_layout()
    return fig

st.write("- Statistical analysis")

if st.button('5th click: plot histogram'):
    fig=fig_hist()
    st.pyplot(fig)
