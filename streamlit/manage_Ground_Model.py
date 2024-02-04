import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(layout="wide")
import altair as alt

# =======================================================
# 컨피덴셜
# password = st.text_input('Password?', 'password')

# =======================================================
# 서브펑션 
def map_altair(df_LOCA):
  ## 지도 범위 설정
  min_NATN = min(df_LOCA['LOCA_NATN_ft'])
  max_NATN = max(df_LOCA['LOCA_NATN_ft'])
  min_NATE = min(df_LOCA['LOCA_NATE_ft'])
  max_NATE = max(df_LOCA['LOCA_NATE_ft'])

  ## 플롯
  base = alt.Chart(df_LOCA).mark_point(opacity=1.0).encode(
      x=alt.X('LOCA_NATE_ft', scale=alt.Scale(domain=(min_NATE-1e3,max_NATE+1e3))), 
      y=alt.Y('LOCA_NATN_ft', scale=alt.Scale(domain=(min_NATN-1e3,max_NATN+1e3))), 
      color=('LOCA_TYPE_x'),
      shape=('LOCA_TYPE_x'),
      tooltip=['LOCA_ID_x','LOCA_FDEO_ft']
      ).properties(width=800, height=600).interactive()

  # Display the chart using Streamlit
  st.altair_chart(base, use_container_width=True)

def map_pyplot(df_LOCA):
  ## 지도 범위 설정
  min_NATN = min(df_LOCA['LOCA_NATN_ft'])
  max_NATN = max(df_LOCA['LOCA_NATN_ft'])
  min_NATE = min(df_LOCA['LOCA_NATE_ft'])
  max_NATE = max(df_LOCA['LOCA_NATE_ft'])
  
  ## 플롯
  fig,ax = plt.subplots(figsize=(9,4), dpi=200)
  ax.set_facecolor('aquamarine')
  #
  ii = df_LOCA['LOCA_TYPE_x'] == 'BC'
  ax.plot(df_LOCA.loc[ii,'LOCA_NATE_ft'],df_LOCA.loc[ii,'LOCA_NATN_ft'],'s',label='BC')
  ii = df_LOCA['LOCA_TYPE_x'] == 'PC'
  ax.plot(df_LOCA.loc[ii,'LOCA_NATE_ft'],df_LOCA.loc[ii,'LOCA_NATN_ft'],'+',label='PC')
  ii = df_LOCA['LOCA_TYPE_x'] == 'JPC'
  ax.plot(df_LOCA.loc[ii,'LOCA_NATE_ft'],df_LOCA.loc[ii,'LOCA_NATN_ft'],'p',label='JPC')
  ii = df_LOCA['LOCA_TYPE_x'] == 'CPT'
  ax.plot(df_LOCA.loc[ii,'LOCA_NATE_ft'],df_LOCA.loc[ii,'LOCA_NATN_ft'],'x',label='CPT')
  
  ## 텍스팅
  for i in range(len(df_LOCA)):
    ax.text(df_LOCA.loc[i,'LOCA_NATE_ft']+1e2,df_LOCA.loc[i,'LOCA_NATN_ft'],df_LOCA.loc[i,'LOCA_ID_x'][-3:], fontsize=6)

  ## 라벨
  ax.set_xlabel("Easting (ft)")
  ax.set_ylabel("Northing (ft)")
  ax.grid(linestyle='dotted')
  ax.minorticks_on()
  ax.legend(loc=3, fancybox=True, shadow=True, fontsize=10, ncol=1)
  ax.axis('equal')
  fig.suptitle('Map with equal scale in x&y axes')
  #
  st.pyplot(fig)


def plot_su(df_IVAN, switch_Nkt, Nkt, slope_CPT_line):
  ## Setup
  zmax_ft = max(df_IVAN['IVAN_DPTH_ft'])
  zmax_m = max(df_IVAN['IVAN_DPTH_m'])

  ## Plot
  fig,ax = plt.subplots(1,2, figsize=(9,7), dpi=200)

  ax[0].plot(df_IVAN['IVAN_TV_ksf'],df_IVAN['IVAN_DPTH_ft'], 'x', label='TV')
  ax[0].plot(df_IVAN['IVAN_MV_ksf'],df_IVAN['IVAN_DPTH_ft'], '.', label='MV')
  ax[0].set_ylabel('Depth (ft)')
  ax[0].set_xlabel('su (ksf)')
  ax[0].set_ylim([zmax_ft,0])
  #
  ax[1].plot(df_IVAN['IVAN_TV_kPa'],df_IVAN['IVAN_DPTH_m'], 'x', label='TV')
  ax[1].plot(df_IVAN['IVAN_MV_kPa'],df_IVAN['IVAN_DPTH_m'], '.', label='MV')
  ax[1].set_ylabel('Depth (m)')
  ax[1].set_xlabel('su (kPa)')
  ax[1].set_ylim([zmax_m,0])

  ## 라벨벨
  for j in range(2):
    ax[j].grid(linestyle='dotted')
    ax[j].minorticks_on()
    ax[j].legend(loc=1, fancybox=True, shadow=True, fontsize=10, ncol=1)

  ## 추세선 추가
  if switch_Nkt == True:
    ax[1].plot([0,zmax_m*slope_CPT_line/Nkt],[0,zmax_m],'k-')

  st.pyplot(fig)

def plot_CPT(df_SCPT, switch_CPT_line, slope_CPT_line):
  ## 셋업
  zmax_ft = max(df_SCPT['SCPT_DPTH_ft'])
  zmax_m = max(df_SCPT['SCPT_DPTH_m'])
  qmax_ksf = max(df_SCPT['SCPT_QNET_ksf'])
  qmax_kPa = max(df_SCPT['SCPT_QNET_kPa'])

  ## 위치별로 분류
  loca_list = df_SCPT['LOCA_ID_x'].unique()
  n_loca = len(loca_list)
  
  ## 플로팅
  fig,ax = plt.subplots(1,2, figsize=(9,7), dpi=200)
  
  for i in range(n_loca):
    loca_name = loca_list[i]
    ii = loca_name == df_SCPT['LOCA_ID_x']
    ax[0].plot(df_SCPT.loc[ii,'SCPT_QNET_ksf'],df_SCPT.loc[ii,'SCPT_DPTH_ft'], '.', label=loca_name)
    ax[1].plot(df_SCPT.loc[ii,'SCPT_QNET_kPa'],df_SCPT.loc[ii,'SCPT_DPTH_m'], '.', label=loca_name)
  
  ## 라벨
  ax[0].set_ylabel('Depth (ft)')
  ax[0].set_xlabel('qnet (ksf)')
  ax[0].set_ylim([zmax_ft,0])
  ax[0].set_xlim([0,qmax_ksf])
  #
  #ax[1].plot(df_SCPT['SCPT_QNET_kPa'],df_SCPT['SCPT_DPTH_m'], '.', label='qnet')
  ax[1].set_ylabel('Depth (m)')
  ax[1].set_xlabel('qnet (kPa)')
  ax[1].set_ylim([zmax_m,0])
  ax[1].set_xlim([0,qmax_kPa])

  for j in range(2):
    ax[j].grid(linestyle='dotted')
    ax[j].minorticks_on()
    ax[j].legend(loc=1, fancybox=True, shadow=True, fontsize=10, ncol=1)

  ## 추세선 추가
  if switch_CPT_line == True:
    ax[1].plot([0,zmax_m*slope_CPT_line],[0,zmax_m],'k-')

  st.pyplot(fig)

def Kaskida():
  st.write('Kaskida')
  filename = 'https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/src_AGS/AGS_Kaskida.xlsx'
  df_PROJ = pd.read_excel(filename, sheet_name='PROJ', header=2)
  df_LOCA = pd.read_excel(filename, sheet_name='LOCA', header=2)
  df_SCPT = pd.read_excel(filename, sheet_name='SCPT', header=2)
  df_IVAN = pd.read_excel(filename, sheet_name='IVAN', header=2)
  return df_PROJ, df_LOCA, df_SCPT, df_IVAN

  
# =======================================================
# 메인 
def main():
  project = st.selectbox(':floppy_disk: Please select a project', (['n/a','Kaskida','ASWX','NaKika','Tiber']))

  ## 메모리 얼로케이션
  df_PROJ = pd.DataFrame()
  df_LOCA = pd.DataFrame()
  df_IVAN = pd.DataFrame()

  
  ## ---------------------------------------------------------
  ## 프로젝트 불러오기
  st.markdown('#### :floppy_disk: 1. Imported Data')

  if project == "Kaskida":
    df_PROJ, df_LOCA, df_SCPT, df_IVAN = Kaskida()
  #
  st.dataframe(df_PROJ)
  st.dataframe(df_LOCA)
  
  ## 자료 LOCA 확인
  if project =="n/a":  # 아무것도 선택 안됐을 때는 메세지만 보이도록
    st.markdown('#### --> Please select one of projects')
  else:  # 프로젝트가 선택 되었을 시에는 펑션 실행
    list_LOCA_ID = df_LOCA['LOCA_ID_x']
    ii = df_LOCA['LOCA_TYPE_x'] == 'BC';    list_LOCA_BC = list(df_LOCA.loc[ii,'LOCA_ID_x']);   n_LOCA_BC = len(list_LOCA_BC)
    ii = df_LOCA['LOCA_TYPE_x'] == 'PC';    list_LOCA_PC = list(df_LOCA.loc[ii,'LOCA_ID_x']);   n_LOCA_PC = len(list_LOCA_PC)
    ii = df_LOCA['LOCA_TYPE_x'] == 'JPC';    list_LOCA_JPC = list(df_LOCA.loc[ii,'LOCA_ID_x']);  n_LOCA_JPC = len(list_LOCA_JPC)
    ii = df_LOCA['LOCA_TYPE_x'] == 'CPT';    list_LOCA_CPT = list(df_LOCA.loc[ii,'LOCA_ID_x']);  n_LOCA_CPT = len(list_LOCA_CPT)

  

  ## ---------------------------------------------------------
  ## 사이드바 만들기: 써머리 용
  st.sidebar.markdown('# Project: '+project)
  #
  if project =="n/a":  # 아무것도 선택 안됐을 때는 메세지만 보이도록
    st.sidebar.markdown('#### --> Please select one of projects')
  else:  # 프로젝트가 선택 되었을 시에는 펑션 실행
    st.sidebar.markdown('## Site Investigations')
    st.sidebar.markdown('#### No. of BC: '+str(n_LOCA_BC))
    st.sidebar.markdown('#### No. of PC: '+str(n_LOCA_PC))
    st.sidebar.markdown('#### No. of JPC: '+str(n_LOCA_JPC))
    st.sidebar.markdown('#### No. of CPT: '+str(n_LOCA_CPT))
    #
    st.sidebar.markdown('## Soil Units')


  ## ---------------------------------------------------------
  ## 지도
  st.markdown('#### :floppy_disk: 2. MAP')
  if project =="n/a":  # 아무것도 선택 안됐을 때는 메세지만 보이도록
    st.markdown('#### --> Please select one of projects')
  else:  # 프로젝트가 선택 되었을 시에는 펑션 실행
    map_altair(df_LOCA)
    map_pyplot(df_LOCA)
  
  ## ---------------------------------------------------------
  ## 수직 지하 프로파일
  st.markdown('#### :floppy_disk: 3. Soil Profiles')
  if project =="n/a":  # 아무것도 선택 안됐을 때는 메세지만 보이도록
    st.markdown('#### --> Please select one of projects')
  else:  # 프로젝트가 선택 되었을 시에는 펑션 실행
    col1, col2 = st.columns(2)

    with col1: 
      #### 플로팅 설정 스위치: CPT
      switch_CPT_line = st.toggle('Plot linear line of CPT')
      if switch_CPT_line == True:
        slope_CPT_line = st.slider('slope of CPT line in SI unit = ', min_value=20,max_value=40,value=30)
      #
      switch_Nkt = st.toggle('Plot su from CPT with Nkt')
      if switch_Nkt == True:
        Nkt = st.slider('Nkt = ', min_value=15,max_value=25,value=25)    
      else:
        Nkt = 0
        
    with col2:
      #### 플로팅 설정 스위치: 디폴트가 off 니까 on 하면 하나씩 보여주는걸로
      switch_BC_each = st.toggle('Plot each BC')
      if switch_BC_each == True:
        loca_BC = st.multiselect('Please select the Box Core (**BC**): No. of BC = '+str(n_LOCA_BC), list_LOCA_BC)
      else:
        loca_BC = list_LOCA_BC
      switch_PC_each = st.toggle('Plot each PC')
      if switch_PC_each == True:
        loca_PC = st.multiselect('Please select the Piston Core (**PC**): No. of PC = '+str(n_LOCA_PC), list_LOCA_PC)
      else:
        loca_PC = list_LOCA_PC
      #  
      switch_JPC_each = st.toggle('Plot each JPC')
      if switch_JPC_each == True:
        loca_JPC = st.multiselect('Please select the Jumbo Piston Core (**JPC**): No. of JPC = '+str(n_LOCA_JPC), list_LOCA_JPC)
      else:
        loca_JPC = list_LOCA_JPC
      #  
      switch_CPT_each = st.toggle('Plot each CPT')
      if switch_CPT_each == True:
        loca_CPT = st.multiselect('Please select the **CPT**: No. of CPT = '+str(n_LOCA_CPT), list_LOCA_CPT)
      else:
        loca_CPT = list_LOCA_CPT

    #### 플로팅: 왼쪽에 su, 오른쪽에 CPT
    col1, col2 = st.columns(2)
    with col1:
      plot_CPT(df_SCPT, switch_CPT_line, slope_CPT_line)
    with col2:
      plot_su(df_IVAN, switch_Nkt, Nkt, slope_CPT_line)

  ## ---------------------------------------------------------
  ## 토질실험
  st.markdown('#### :floppy_disk: 4. Soil Lab Testing')

  
  ## ---------------------------------------------------------
  ## 평면 지역 분할
  st.markdown('#### :floppy_disk: 5. Soil Province')
  if project =="n/a":  # 아무것도 선택 안됐을 때는 메세지만 보이도록
    st.markdown('#### --> Please select one of projects')
  else:  # 프로젝트가 선택 되었을 시에는 펑션 실행
    pass


# =======================================================
# Confidential

## 비번확인
password = st.text_input('Password?', 'password')

## 조건문
if password == st.secrets['DB_pw']:
  st.markdown('## Welcome to Database by JS')
  main()
else:
  st.markdown('## Sorry, this is confidential')

