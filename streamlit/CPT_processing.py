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


