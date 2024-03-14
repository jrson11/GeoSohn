# Author: Jung.Sohn@bp.com
# Date: 03/01/2024
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px # 초급

# ====================================================================
## 셋업

# 페이지 설정을 wide 모드로 설정
st.set_page_config(layout="wide")

# 비번 확인
password = st.sidebar.text_input('Password?')


# ====================================================================
## 서브펑션

def bp_map(project):
  st.header(project)
  from sub_bp_maps import project_maps
  project_maps(project)
  
def bp_mudmat_bearing_capacity(project):
  st.header(project)

  if project == "example_CLAY":
    from sub_mudmat_bearing_capacity_14Mar24_v2 import eg_clay_bearing_capacity
    eg_clay_bearing_capacity()
  else:
    from sub_mudmat_bearing_capacity_14Mar24_v2 import main
    main(project)

def bp_mudmat_settlement(project):
  st.header(project)

def API_ISO(project):
  st.header(project)
  from sub_API_ISO import API_ISO_code
  API_ISO_code(project)


# ====================================================================
## 메인

## 조건문
if password == st.secrets['DB_pw']:
  st.markdown("#### Thanks for joining :blue[Jung]'s database. Please click one of below icons.")

  # ---------------------------------------------------------------------------
  # 열을 나눠서 아이콘 버튼 추가
  col1, col2, col3, col4 = st.columns(4)

  with col1: # Map 
    on_icon1 = st.toggle(':world_map: bp Maps')
    if on_icon1:
      area = st.sidebar.selectbox(':floppy_disk: Please select an area', ['n/a', '08_Egypt', '09_GoM', '15_Trinadad', '16_Senegal'])

      if area == '09_GoM':
        project = st.sidebar.selectbox(':floppy_disk: Please select a project', ['n/a','Kaskida','ASWX','NaKika','Tiber'])
      elif area == '08_Egypt':
        project = st.sidebar.selectbox(':floppy_disk: Please select a project', ['n/a','Raven_WND'])
      elif area == '15_Trinadad':
        project = st.sidebar.selectbox(':floppy_disk: Please select a project', ['n/a','Ginger','Coconut','Jupiter'])
      elif area == '16_Senegal':
        project = st.sidebar.selectbox(':floppy_disk: Please select a project', ['n/a','Deepwater','MidHub','??'])
      else:
        project = 'n/a'


  with col2: # Plaxis
    on_icon2 = st.toggle(':computer: PLAXIS3D Python script')  
      
  with col3: # Mudmat: Bearing Capacity 
    on_icon3 = st.toggle(':fire: Mudmat: Bearing Capacity')
    if on_icon3:
      example = st.sidebar.selectbox(':floppy_disk: Please select a project', ['example_CLAY','10inchFTA_Tortue','Raven_WND'])


  with col4: # Mudmat: Settlement 
    on_icon4 = st.toggle(':rocket: Mudmat: Settlement')
    if on_icon4:
      project = st.sidebar.selectbox(':floppy_disk: Please select a project', ['example_CLAY','10inchFTA_Tortue'])


  # ---------------------------------------------------------------------------
  # 열을 나눠서 아이콘 버튼 추가
  col5, col6, col7, col8 = st.columns(4)

  with col5:
    on_icon5 = st.toggle(':test_tube: Fugro: Lab Data Interpretation')
    
  with col6:
    on_icon6 = st.toggle(':alembic: NGI: Lab Data Interpretation')
    
  with col7:
    on_icon7 = st.toggle(':book: API and ISO')
    if on_icon7:
      code = st.sidebar.selectbox(':floppy_disk: Please select a code', ['API_2A','API_2A_WSD/LRFD','API_2GEO','ISO_19901-4'])
  
  with col8:
    on_icon8 = st.toggle(':building_construction: AGS4 converter')
  
  # ---------------------------------------------------------------------------
  # 열이 끝나고 서브펑션을 실행
  st.write('---------------------------------------')
  
  if on_icon1:
    bp_map(project)
  elif on_icon2:
    st.subheader('TBD')
  elif on_icon3:
    bp_mudmat_bearing_capacity(example)
  elif on_icon4:
    st.subheader('TBD')
  elif on_icon5:
    st.subheader('TBD')
  elif on_icon6:
    st.subheader('TBD')
  elif on_icon7:
    API_ISO(code)
  elif on_icon8:
    st.subheader('TBD')
  else:
    st.image('https://cdn.freelogovectors.net/wp-content/uploads/2023/05/bp_logo-freelogovectors.net_.png')


# ====================================================================
else: # 패스워드가 틀렸을 경우
  st.markdown('## Sorry \n #### Please get in touch with :blue[Jung] to get permission to access geotechnical web applications.')
