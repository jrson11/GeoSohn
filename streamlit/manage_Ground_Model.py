import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

# =======================================================
# 컨피덴셜
# password = st.text_input('Password?', 'password')

# =======================================================
# 서브펑션 
def map_altair(df_LOCA):
  base = alt.Chart(df_LOCA).mark_point(opacity=0.8).encode(
      x=alt.X('LOCA_NATE_ft'), 
      y=alt.Y('LOCA_NATN_ft'),  
      color=('LOCA_TYPE_x'),
      shape=('LOCA_TYPE_x'),
      tooltip=['LOCA_ID_x','LOCA_FDEO_ft']
      ).properties(width=900, height=600).interactive()

  # Display the chart using Streamlit
  st.altair_chart(base, use_container_width=True)

def Kaskida():
  st.write('Kaskida')
  filename = 'https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/src_AGS/AGS_Kaskida(01Dec23).xlsx'
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
    ii = df_LOCA['LOCA_TYPE_x'] == 'BC';  list_LOCA_BD = list(df_LOCA.loc[ii,'LOCA_ID_x'])
    ii = df_LOCA['LOCA_TYPE_x'] == 'PC';  list_LOCA_PC = list(df_LOCA.loc[ii,'LOCA_ID_x'])
    ii = df_LOCA['LOCA_TYPE_x'] == 'JPC';  list_LOCA_JPC = list(df_LOCA.loc[ii,'LOCA_ID_x'])
    ii = df_LOCA['LOCA_TYPE_x'] == 'CPT';  list_LOCA_CPT = list(df_LOCA.loc[ii,'LOCA_ID_x'])


  ## ---------------------------------------------------------
  ## 지도
  st.markdown('#### :floppy_disk: 2. MAP')
  if project =="n/a":  # 아무것도 선택 안됐을 때는 메세지만 보이도록
    st.markdown('#### --> Please select one of projects')
  else:  # 프로젝트가 선택 되었을 시에는 펑션 실행
    map_altair(df_LOCA)

  
  ## ---------------------------------------------------------
  ## 수직 지하 프로파일
  st.markdown('#### :floppy_disk: 3. Soil Profiles')
  if project =="n/a":  # 아무것도 선택 안됐을 때는 메세지만 보이도록
    st.markdown('#### --> Please select one of projects')
  else:  # 프로젝트가 선택 되었을 시에는 펑션 실행
    loca_BC = st.multiselect('Please select the Box Core (**BC**)', list_LOCA_BD)
    loca_PC = st.multiselect('Please select the Piston Core (**PC**)', list_LOCA_PC)
    loca_JPC = st.multiselect('Please select the Jumbo Piston Core (**JPC**)', list_LOCA_JPC)
    loca_CPT = st.multiselect('Please select the **CPT**', list_LOCA_CPT)

  
  ## ---------------------------------------------------------
  ## 평면 지역 분할
  st.markdown('#### :floppy_disk: 4. Soil Province')
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

