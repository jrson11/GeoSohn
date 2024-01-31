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
  loca_BC = st.multiselect('Please select the Box Core locations', list_BC,'n/a')
  loca_PC = st.multiselect('Please select the Piston Core locations', ('n/a','b','c'))
  loca_JPC = st.multiselect('Please select the Jumbo Piston Core locations', ('n/a','b','c'))
  loca_CPT = st.multiselect('Please select the CPT locations', ('n/a','b','c'))

# Membership --------------------------------------------
if password == st.secrets['DB_pw']:
  st.markdown('## Welcome to Database by JS')
  main()
  
else:
  st.markdown('## Sorry, this is confidential')

