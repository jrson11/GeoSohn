import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

# =======================================================
# Confidential
password = st.text_input('Password?', 'password')

# Main --------------------------------------------------
def main():
  proj = st.selectbox('Please select a project', ('Kaskida','ASWX','NaKika','Tiber'))
  st.write('You selected: ', proj)


  list_BC = list(['n/a','b','c'])
  list_PC = list(['n/a','b','c'])
  list_JPC = list(['n/a','b','c'])  
  list_CPT = list(['n/a','b','c'])  
  loca_BC = st.multiselect('Please select the Box Core (**BC**) locations', list_BC,'n/a')
  loca_PC = st.multiselect('Please select the Piston Core (**PC**) locations', list_PC,'n/a')
  loca_JPC = st.multiselect('Please select the Jumbo Piston Core (**JPC**) locations', list_JPC,'n/a')
  loca_CPT = st.multiselect('Please select the **CPT** locations', list_CPT,'n/a')

# Membership --------------------------------------------
if password == st.secrets['DB_pw']:
  st.markdown('## Welcome to Database by JS')
  main()
  
else:
  st.markdown('## Sorry, this is confidential')

