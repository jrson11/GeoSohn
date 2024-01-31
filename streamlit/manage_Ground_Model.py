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
def map_altair(proj):
  st.write('Show me'+proj)

def Kaskida():
  st.write('Kaskida')
  filename = 'https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/src_AGS/AGS_Kaskida(01Dec23).xlsx'
  df_PROJ = pd.read_excel(filename, sheet_name='PROJ', header=2)
  df_LOCA = pd.read_excel(filename, sheet_name='LOCA', header=2)
  df_SCPT = pd.read_excel(filename, sheet_name='SCPT', header=2)
  df_IVAN = pd.read_excel(filename, sheet_name='IVAN', header=2)
  return df_PROJ, df_LOCA, df_SCPT, df_IVAN

def list_loca(db):
  list_loca = df['LOCA_ID_x'].unique()
  return list_loca
  
# =======================================================
# 메인 
def main():
  project = st.selectbox(':floppy_disk: Please select a project', (['n/a','Kaskida','ASWX','NaKika','Tiber']))
  st.write('You selected: ', project)

  ## 메모리 얼로케이션
  df_PROJ = pd.DataFrame()
  df_LOCA = pd.DataFrame()
  df_IVAN = pd.DataFrame()
  #
  list_BC = list(['n/a','b','c'])
  list_PC = list(['n/a','b','c'])
  list_JPC = list(['n/a','b','c'])  
  list_CPT = list(['n/a','b','c'])  

  ## 프로젝트 선택
  if project == "Kaskida":
    df_PROJ, df_LOCA, df_SCPT, df_IVAN = Kaskida()
  st.dataframe(df_PROJ)
  st.dataframe(df_LOCA)

  ## 자료 리스트 확인
  list_BC = list_loca(df_LOCA)

  loca_BC = st.multiselect('Please select the Box Core (**BC**)', list_BC,'n/a')
  loca_PC = st.multiselect('Please select the Piston Core (**PC**)', list_PC,'n/a')
  loca_JPC = st.multiselect('Please select the Jumbo Piston Core (**JPC**)', list_JPC,'n/a')
  loca_CPT = st.multiselect('Please select the **CPT**', list_CPT,'n/a')



  ## ---------------------------------------------------------
  ## Map
  map_altair(project)

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

