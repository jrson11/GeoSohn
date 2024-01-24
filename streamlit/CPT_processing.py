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

st.dataframe(df_Raw)

df_CPT = pd.DataFrame()
df_CPT['LOCA_ID'] = df_Raw.loc[2:,'LOCA_ID']
df_CPT['Depth_m'] = df_Raw.loc[2:,'SCPT_DPTH']
df_CPT['qc_MPa'] = df_Raw.loc[2:,'SCPT_RES']
df_CPT['fs_kPa'] = df_Raw.loc[2:,'SCPT_FRES']
df_CPT['u2_kPa'] = df_Raw.loc[2:,'SCPT_PWP2']
df_CPT['qt_MPa'] = df_Raw.loc[2:,'SCPT_QT']
df_CPT['qnet_MPa'] = df_Raw.loc[2:,'SCPT_QNET']

st.dataframe(df_CPT)
