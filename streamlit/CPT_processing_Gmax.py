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
import streamlit as st

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

# Title
st.title("In-situ CPT data processing")
st.write('- Purpose: To estimate Gmax from CPT data')
st.write('- Method: Empirical equations based on Robertson2010')


# =============================================================================
# Raw 데이터 가져오기
st.subheader(':floppy_disk: Step 1: Import in-situ CPT data')
df_Info = pd.read_csv('https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_CPTs_Fugro_TNW/TNW_20200508_FNLM_AGS4.0_V02_F-SCPT_052.csv', nrows=2)
col_list = list(df_Info.columns)
df_Raw = pd.read_csv('https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_CPTs_Fugro_TNW/TNW_20200508_FNLM_AGS4.0_V02_F-SCPT_052.csv', skiprows=2)
df_Raw.columns = col_list

## Raw 데이터에서 헤더 빼고 필요한 파라미터만 가져오기
df_CPT = pd.DataFrame()
df_CPT['LOCA_ID'] = df_Raw.loc[:,'LOCA_ID']
df_CPT['Depth_m'] = df_Raw.loc[:,'SCPT_DPTH']
df_CPT['qc_MPa'] = df_Raw.loc[:,'SCPT_RES']
df_CPT['fs_kPa'] = df_Raw.loc[:,'SCPT_FRES']
df_CPT['u2_kPa'] = df_Raw.loc[:,'SCPT_PWP2']
df_CPT['qt_MPa'] = df_Raw.loc[:,'SCPT_QT']
df_CPT['qnet_MPa'] = df_Raw.loc[:,'SCPT_QNET']
df_CPT['Fr_%'] = df_Raw.loc[:,'SCPT_FRR']
df_CPT['Bq_x'] = df_Raw.loc[:,'SCPT_BQ']

## 데이터 갯수 확인
loca_list = list(df_CPT['LOCA_ID'].unique())
n_loca = len(loca_list)

## 원하는 데이터 선택하기
loca = st.selectbox("Pick the location: ", loca_list)
ii = loca == df_CPT['LOCA_ID'] 
st.dataframe(df_CPT[ii])
#
zmax = max(df_CPT.loc[ii,'Depth_m'])
qcmax = 60
fsmax = 1000


## 체크하기 위한 플롯팅
def fig_CPT_raw_data(df_CPT):
    ls = 10     # 라벨사이즈
    al = 0.5    # 투명도
    ts = 8      # 텍스트 사이즈
    loca = df_CPT.loc[0,'LOCA_ID']
    z = df_CPT['Depth_m'] 
    qc = df_CPT['qc_MPa']
    qt = df_CPT['qt_MPa']
    fs = df_CPT['fs_kPa']
    u2 = df_CPT['u2_kPa']
    Rf = df_CPT['Fr_%']
    Bq = df_CPT['Bq_x']
    
    fig,ax = plt.subplots(1,5, figsize=(12,6), dpi=200)    
    ax[0].plot(qc,z, '.',color='C0',label='qc')
    ax[0].plot(qt,z, 'x', color='C1',label='qt')
    ax[1].plot(fs,z, '.',color='C0',label='fs')
    ax[2].plot(u2,z, '.',color='C0',label='u2')
    ax[3].plot(Rf,z, '.',color='C0',label='Rf')
    ax[4].plot(Bq,z, '.',color='C0',label='Bq')
    #
    ax[0].set_ylabel("Depth [m]",size=ls)
    ax[0].set_xlabel("Cone resistance \n [MPa]",size=ls)
    ax[1].set_xlabel("Friction \n [kPa]",size=ls)
    ax[2].set_xlabel("Pore pressure \n [kPa]",size=ls)
    ax[3].set_xlabel("Friction ratio \n [%]",size=ls)
    ax[4].set_xlabel("Pore pressure ratio \n [-]",size=ls)
    #
    ax[0].set(xlim=(0,qcmax))
    ax[1].set(xlim=(0,fsmax))
    ax[3].set(xlim=(0,6.5))
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
        ax[i].legend(loc='upper center', bbox_to_anchor=(0.5, 0), fancybox=True, shadow=True, ncol=3)
        ax[i].grid(which='major',linestyle='-')
        ax[i].grid(which='minor',linestyle='dotted')
        ax[i].minorticks_on()
        ax[i].xaxis.set_ticks_position('top')
        ax[i].xaxis.set_label_position('top')
        #ax[i].yaxis.grid(which="minor",linestyle='dotted')
    
    # 완성
    fig.suptitle("CPT data: "+loca, y=1, size=1.2*ls)
    plt.tight_layout()
    return fig

if st.button('1st click: plot raw data'):
    fig=fig_CPT_raw_data(df_CPT)
    st.pyplot(fig)

UW = st.number_input("Soil density: ", min_value=10, value=18, step=1)

