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

  loca = st.multiselect('Please select the locations to check', ('a','b','c'))
  st.write('You selected:', loca)

# Membership --------------------------------------------
if password == st.secrets['DB_pw']:
  st.markdown('## Welcome to Database by JS')
  main()
  
else:
  st.markdown('## Sorry, this is confidential')

