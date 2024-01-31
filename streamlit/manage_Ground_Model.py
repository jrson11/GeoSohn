import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

# =======================================================
# Confidential
# password = st.text_input('Password?', 'password')

# =======================================================
# 서브펑션 
def map_altair(proj):
  st.write('Show me'+proj)

def Kaskida():
  st.write('Kaskida')
  
# =======================================================
# 메인 
def main():
  project = st.selectbox(':floppy_disk: Please select a project', ('n/a','Kaskida','ASWX','NaKika','Tiber'),'n/a')
  st.write('You selected: ', project)

  list_BC = list(['n/a','b','c'])
  list_PC = list(['n/a','b','c'])
  list_JPC = list(['n/a','b','c'])  
  list_CPT = list(['n/a','b','c'])  
  loca_BC = st.multiselect('Please select the Box Core (**BC**) locations', list_BC,'n/a')
  loca_PC = st.multiselect('Please select the Piston Core (**PC**) locations', list_PC,'n/a')
  loca_JPC = st.multiselect('Please select the Jumbo Piston Core (**JPC**) locations', list_JPC,'n/a')
  loca_CPT = st.multiselect('Please select the **CPT** locations', list_CPT,'n/a')

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

