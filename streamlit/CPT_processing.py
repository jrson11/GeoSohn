# =============================================================================
# Name: CPT_processing.py
# Authour: Jung.Sohn
# Date: 24Jan24
# All rights reserved
# =============================================================================

import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
#from scipy.stats import multivariate_normal as mvn
#from scipy.stats import norm
import streamlit as st

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

# Title
st.title("In-situ CPT data processing")
st.write('- Purpose: To estimate Gmax from CPT data')
st.write('- Method: Empirical equations based on Robertson2010')


# =============================================================================
# Import raw data
st.subheader(':floppy_disk: Step 1: Import in-situ CPT data')

df_Raw = pd.read_csv('https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_CPTs_Fugro_TNW/TNW_20200508_FNLM_AGS4.0_V02_F-SCPT_052.csv')
st.write('Imported data: Unit Weight derived from in-situ CPT')

#st.dataframe(df_Raw)

df_CPT = pd.DataFrame()
df_CPT['LOCA_ID'] = df_Raw.loc[2:,'LOCA_ID']
df_CPT['Depth_m'] = df_Raw.loc[2:,'SCPT_DPTH']
df_CPT['qc_MPa'] = df_Raw.loc[2:,'SCPT_RES']
df_CPT['fs_kPa'] = df_Raw.loc[2:,'SCPT_FRES']
df_CPT['u2_kPa'] = df_Raw.loc[2:,'SCPT_PWP2']
df_CPT['qt_MPa'] = df_Raw.loc[2:,'SCPT_QT']
df_CPT['qnet_MPa'] = df_Raw.loc[2:,'SCPT_QNET']

#st.dataframe(df_CPT)


loca_list = list(df_CPT['LOCA_ID'].unique())
n_loca = len(loca_list)


loca = st.selectbox("Pick the location: ", loca_list)
UW = st.number_input("Soil density: ", min_value=10, value=18, step=1)


# =============================================================================
# Soil Classification 
def cal_UW_Robertson2010(gw,Rf,qc):
    gamma = gw * (0.27*np.log10(Rf) + 0.36*np.log10(qc/Patm) + 1.236) 
    gamma[np.where(Rf == 0)[0]] = np.nan
    return np.array(gamma) # [kN/m3]

#uw = cal_UW_Robertson2010(gw,Rf,qc)
#bd = uw/g # soil bulk density [g/cc]

def cal_UW_Mayne2012(fs):
    fs_kPa = fs*1e3
    gamma = 26 - 14/(1+(0.5*np.log10(fs_kPa+1))**2)
    return np.array(gamma) # [kN/m3]

def Ic_Robertson1990():
## Ic (Robertson, 1990) / ## Ic (Robertson and Wride, 1998)
# Reference: https://geotech40.blogspot.com/

#    SBT zone 1: sensitive fine-grained
#    SBT zone 2: CLAY - organic soil
#    SBT zone 3: CLAYs: clay to silty clay
#    SBT zone 4: SILT mixtures: clayey silt & silty clay
#    --------------------------------------------------- Ic = 2.60
#    SBT zone 5: SAND mixture: silty sand to sandy silt
#    SBT zone 6: SANDs: clean sands to silty sands
#    SBT zone 7: Dense sand to gravelly sand
#    SBT zone 8: Stiff sand to clayey sand
#    SBT zone 9: Stiff fine-grained (overconsolidated)

    qt = qc + (1-alpha_CPT)*u2
    qn = qt - sv_tot
    Qt = qn/sv_eff
    Fr = np.array([a/(b-c)*100 for a,b,c in zip(fs,qc,sv_tot)])
    Ic = np.array([np.sqrt((3.47-np.log10(x))**2 + (np.log10(y)+1.22)**2) for x,y in zip(Qt,Fr)])
    Ic_soil = []
    for i in range(len(z)):
        if Ic[i] > 3.60 and Ic[i] <=4.0:
            Ic_soil.append(2) # peats
        elif Ic[i] > 2.95 and Ic[i] <=3.60:
            Ic_soil.append(3) # CLAY
        elif Ic[i] > 2.60 and Ic[i] <=2.95:
            Ic_soil.append(4) # SILT
        elif Ic[i] > 2.05 and Ic[i] <=2.60:
            Ic_soil.append(5) # SAND mix
        elif Ic[i] > 1.31 and Ic[i] <=2.05:
            Ic_soil.append(6) # SAND clean
        elif Ic[i] > 1.00 and Ic[i] <=1.31:
            Ic_soil.append(7) # SAND gravel
        else:
            Ic_soil.append(np.nan)

def Isbt_Robertson2010():
## Isbt (Robertson, 2010)
    Isbt = np.array([((3.47-np.log10(x/(Patm)))**2 + (np.log10(y)+1.22)**2)**0.5 for x,y in zip(qc,Rf)])
    Isbt_soil = []
    for i in range(len(z)):
        if Isbt[i] > Isbt_val and Isbt[i] <= 4.0:
            Isbt_soil.append(4)
        elif Isbt[i] > 1 and Isbt[i] <= Isbt_val:
            Isbt_soil.append(5)
        else:
            Isbt_soil.append(np.nan)

def cal_Vs_Mayne2007(fs):
    fs_kPa = fs*1e3 # [kPa]
    Vs = 51.6*np.log(fs_kPa) + 18.5
    return Vs
#Vs_M = cal_Vs_Mayne2007(fs)

def cal_Vs_Robertson2009(Ic,qt,sv):
    alpha = 10**(0.55*Ic+1.68) # [m2/s2]
    Vs = (alpha*(qt-sv)/Patm)**0.5
    return Vs
#Vs_R = cal_Vs_Robertson2009(Ic,qt,sv_tot)

def cal_Gmax_Mayne1993(sbt,qc):
    # https://www.astm.org/DIGITAL_LIBRARY/JOURNALS/GEOTECH/PAGES/GTJ10267J.htm
    qc_kPa = qc*1e3
    Gmax = 0.00287*qc_kPa**1.335 # only for CLAY
    #
    ii = (sbt <= 4) # CLAY
    Gmax[~ii] = np.nan
    #
    return Gmax

def cal_Gmax_Mayne2007(sbt,qn):
    Gmax_CLAY = 50*qn
    Gmax_SILT = 50*Patm*(qn/Patm)**0.8
    Gmax_SAND = 50*Patm*(qn/Patm)**0.6
    Gmax = np.zeros(len(qn))
    ii = (sbt <= 3) # Clay
    Gmax[ii] = Gmax_CLAY[ii].copy()
    ii = (sbt == 4) # Silt
    Gmax[ii] = Gmax_SILT[ii].copy()
    ii = (sbt >= 5) # Sand
    Gmax[ii] = Gmax_SAND[ii].copy()
    return Gmax


# Other empirical equations ==================================================

## All: Su
def cal_su(qt,sv_t):
    Nkt_low = 10
    Nkt_high = 18
    #
    su_lb = (qt-sv_t)/Nkt_high
    su_ub = (qt-sv_t)/Nkt_low
    #
    return su_lb,su_ub

def cal_su_Vs_Clay(sbt,Vs):
    su_kPa = (Vs/7.93)**1.59
    #
    ii = (sbt <= 4) # CLAY
    su_kPa[~ii] = np.nan
    #
    su = su_kPa/1e3
    return su

## SAND/CLAY: phi
def cal_phi_Robertson1983(sbt,qc,sv_e):
    tan_phi = 1/2.68 * (np.log10(qc/sv_e) + 0.29)
    phi_rad = np.arctan(tan_phi)
    phi_deg = phi_rad*180/np.pi
    #
    #ii = (sbt >= 5) # SAND
    #phi_deg[~ii] = np.nan
    #
    return phi_deg

def cal_phi_Mayne2001(sbt,fs,sv_t):
    # Not sure where this came from....but Asitha used it.
    phi_deg = 30.8*(np.log10(fs/sv_t) + 1.26) # only for CLAY
    #
    ii = (sbt <= 4) # CLAY
    phi_deg[~ii] = np.nan
    #
    return phi_deg
    
def cal_phi_Mayne2007(sbt,qt,sv_e):
    q_t1 = (qt/Patm) * (Patm/sv_e)**0.5
    phi = 17.6 + 11.0*np.log10(q_t1)  # only for SAND
    #
    ii = (sbt >= 5) # SAND
    phi[~ii] = np.nan
    #
    return phi


## SAND/CLAY: K0
def cal_K0_Kulhawy1990(sbt,qc,qn,sv_e):
    K0 = 0.1*(qn/sv_e)
    # Note: There is some more for SAND based on OCR.
    OCR_SAND = 1 # This cannot be correct, but let's try for now.
    K_D = 2*OCR_SAND**(1/1.56)
    #
    ii = (sbt >= 5) # SAND
    K0[ii] = 0.359 + 0.071*K_D - 0.00093*(qc[ii]/sv_e[ii])
    # 
    return K0

def cal_K0_Mayne1995():
    K0 = 0
    return K0
K0_M1995 = cal_K0_Mayne1995()

def cal_K0_Mayne2007_Eq26(qt,sv_e):
    OCR = 1 # Not sure this part
    K0 = 0.192*(qt/Patm)**0.22 * (Patm/sv_e)**0.31 * OCR**0.27
    return K0
#




## SAND: Dr ------------------------------------------------------------------
def cal_Dr_Jamiolkowski2001(sbt,qt,sv_e):
    q_t1 = (qt/Patm) * (Patm/sv_e)**0.5
    bx = 0.675
    # Reference was cited by Mayne 2014
    #   high compressibility SAND: bx=0.525
    #   medium compressibility SAND: bx=0.625
    #   low compressibility SAND: bx=0.825
    Dr = 100*(0.268*np.log(q_t1) - bx)
    #
    ii = (sbt >= 5) # SAND
    Dr[~ii] = np.nan
    #
    return Dr

def cal_Dr_Jamiokowski2003_dry(sbt,qc,smean):
    Dr = (1.0/0.0295)*np.log(qc/2.494 / smean/100)**0.46
    #
    ii = (sbt >= 5) # SAND
    Dr[~ii] = np.nan
    #
    return Dr

def cal_Dr_ratio_Jamiokowski2003_sat(sbt,qc,sv_e):
    qc_kPa = qc*1e3
    Dr_ratio = (((-1.87 + 2.32*np.log(1e3*qc_kPa/(100*sv_e)**0.5))/100) + 1)
    #
    ii = (sbt >= 5) # SAND
    Dr_ratio[~ii] = np.nan
    #
    return Dr_ratio
def cal_Dr_Mayne2014(sbt,qt,sv_e):
    OCR = 1 # Not sure this part
    q_t1 = (qt/Patm) * (Patm/sv_e)**0.5
    Dr = 100 * (q_t1/(305*OCR**0.2))**0.5
    return Dr


## CLAY: preconsolidation + OCR ----------------------------------------------
def cal_OCR_Robertson2009(sbt,Qt):
    OCR = 0.25*Qt**1.25
    #
    ii = (sbt <= 4) # CLAY
    OCR[~ii] = np.nan
    return OCR

def cal_sp_Mayne2014(sbt,Ic,qn):
    m = 1.0-0.28/(1+(Ic/2.65**25))
    qn_kPa = qn*1e3
    sp_kPa = 0.33*(qn_kPa)**m
    #
    #ii = (sbt <= 4) # CLAY
    #sp_kPa[~ii] = np.nan
    #
    return np.round(sp_kPa)/1e3


def cal_St_Robertson2009(sbt,Fr):
    St = 7.1/Fr
    #
    ii = (sbt <= 4) # CLAY
    St[~ii] = np.nan
    #
    return St

## SILT: K0 ------------------------------------------------------------------
def cal_K0_Robertson2015(sbt,ocr):
    K0 = 0.5*ocr**0.5
    #
    ii = (sbt == 5) # SILT
    K0[~ii] = np.nan
    #
    return K0

# Plotting to check ==========================================================

def plot_fig_1_CPTdata():
    fig,ax = plt.subplots(1,5, figsize=(11,6), dpi=200)    
    ax[0].plot(qc,z, color='C0',label='qc')
    ax[1].plot(fs,z, color='C0',label='fs')
    ax[2].plot(u2,z, color='C0',label='u2')
    ax[3].plot(Rf,z, color='C0',label='Rf')
    ax[4].plot(Bq,z, color='C0',label='Bq')
    #
    ax[0].set_ylabel("Depth [m]",size=ls)
    ax[0].set_xlabel("Cone resistance [MPa]",size=ls)
    ax[1].set_xlabel("Friction [MPa]",size=ls)
    ax[2].set_xlabel("Pore pressure [MPa]",size=ls)
    ax[3].set_xlabel("Friction ratio [%]",size=ls)
    ax[4].set_xlabel("Pore pressure ratio [-]",size=ls)
    #
    ax[3].set(ylim=(zmax,0),xlim=(0,6.5))
    ax[3].set(xticks=([0,2,6]))
    ax[3].yaxis.grid(which="minor",linestyle='dotted')
    ax[3].add_patch(patches.Rectangle((0,0),2,zmax,facecolor='goldenrod',alpha=0.4))
    ax[3].add_patch(patches.Rectangle((2,0),4,zmax,facecolor='mediumseagreen',alpha=0.4))
    ax[3].add_patch(patches.Rectangle((6,0),0.5,zmax,facecolor='sienna',alpha=al))
    ax[3].text(1.05, 9.8, "SAND", va='bottom', rotation=90, size=ts, color="black")
    ax[3].text(3.05, 9.8, "CLAY or SILT", va='bottom', rotation=90, size=ts, color="black")
    ax[3].text(6.05, 9.8, "Glauconite", va='bottom', rotation=90, size=ts, color="black")
    #
    for i in range(5):
        ax[i].set(ylim=(zmax,0))
        ax[i].legend(loc='upper center', bbox_to_anchor=(0.5, 0), fancybox=True, shadow=False)
        ax[i].grid(linestyle='dotted')
        ax[i].minorticks_on()
        ax[i].xaxis.set_ticks_position('top')
        ax[i].xaxis.set_label_position('top')
        ax[i].yaxis.grid(which="minor",linestyle='dotted')
    #
    fig.suptitle("CPT data: "+file_CPT, y=1, size=1.2*ls)


def plot_fig_2_CPTsoil():
    fig,ax = plt.subplots(1,5, figsize=(11,6), dpi=200)
    ax[0].plot(qc,z, color='C0',label='qc')
    ax[1].plot(uw,z, color='C1',label='Robertson, 2010')
    ax[1].plot(uw_M,z, '--',color='C0',label='Mayne, 2012')
    ax[2].plot(sv_tot,z, color='C0',label='σ_v_total')
    ax[2].plot(sv_eff,z, '--',color='C0',label='σ_v_effective')
    ax[3].plot(Ic,z,color='yellow',linewidth=lw, label='Ic: Robertson, 1990')
    ax[4].plot(Isbt,z,color='yellow',linewidth=lw, label='Isbt: Robertson, 2010')
    #
    ax[0].set_ylabel("Depth [m]",size=ls)
    ax[0].set_xlabel("Cone resistance [MPa]",size=ls)
    ax[1].set_xlabel("Unit weight [kN/m3]",size=ls)
    ax[2].set_xlabel("In-situ stress [MPa]",size=ls)
    ax[3].set_xlabel("Soil Behavior Type [-]",size=ls)
    ax[4].set_xlabel("Soil Behavior Type [-]",size=ls)
    #
    ax[1].set(xlim=(16,23))
    ax[2].set(xlim=(0,round(max(sv_tot[~np.isnan(sv_tot)]))))
    ax[3].set(ylim=(zmax,0),xlim=(1,4))
    ax[3].set(xticks=([1.3,2.0,2.6,4]))
    ax[3].add_patch(patches.Rectangle((0,0),1.31,zmax,facecolor='darkorange',alpha=al))
    ax[3].add_patch(patches.Rectangle((1.31,0),0.74,zmax,facecolor='darkgoldenrod',alpha=al))
    ax[3].add_patch(patches.Rectangle((2.05,0),0.55,zmax,facecolor='mediumseagreen',alpha=al))
    ax[3].add_patch(patches.Rectangle((2.60,0),0.35,zmax,facecolor='seagreen',alpha=al))
    ax[3].add_patch(patches.Rectangle((2.95,0),0.65,zmax,facecolor='steelblue',alpha=al))
    ax[3].add_patch(patches.Rectangle((3.6,0),0.4,zmax,facecolor='sienna',alpha=al))
    ax[3].text(1.05, 9.8, "gravel - dense sand", va='bottom', rotation=90, size=ts, color="black")
    ax[3].text(1.55, 9.8, "clean sand - silty sand", va='bottom', rotation=90, size=ts, color="black")
    ax[3].text(2.22, 9.8, "silty sand - sandy silt", va='bottom', rotation=90, size=ts, color="black")
    ax[3].text(2.65, 9.8, "clayey silt - silty clay", va='bottom', rotation=90, size=ts, color="black")
    ax[3].text(3.2, 9.8, "silty clay - clay", va='bottom', rotation=90, size=ts, color="black")
    ax[3].text(3.65, 9.8, "peat", va='bottom', rotation=90, size=ts, color="black")
    #
    ax[4].set(ylim=(zmax,0),xlim=(1,4))
    ax[4].set(xticks=([1.0,Isbt_val,4]))
    ax[4].add_patch(patches.Rectangle((0,0),Isbt_val,zmax,facecolor='darkgoldenrod',alpha=al))
    ax[4].add_patch(patches.Rectangle((Isbt_val,0),4-Isbt_val,zmax,facecolor='seagreen',alpha=al))
    ax[4].text(1.5, 9.8, "SAND", va='bottom', rotation=90, size=ts, color="black")
    ax[4].text(3.0, 9.8, "CLAY", va='bottom', rotation=90, size=ts, color="black")
    #
    for i in range(5):
        ax[i].set(ylim=(zmax,0))
        ax[i].legend(loc='upper center', bbox_to_anchor=(0.5, 0), fancybox=True, shadow=False)
        ax[i].grid(linestyle='dotted')
        ax[i].minorticks_on()
        ax[i].xaxis.set_ticks_position('top')
        ax[i].xaxis.set_label_position('top')
        ax[i].yaxis.grid(which="minor",linestyle='dotted')
    #
    fig.suptitle("CPT soil type: "+file_CPT, y=1, size=1.2*ls)
