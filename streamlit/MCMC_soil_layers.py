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

if st.button('Generate initial model plot'):
    fig=fig_ini_UW()
    st.pyplot(fig)
