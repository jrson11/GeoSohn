# Name: GeoSohn.py
# Purpose: To develop web app for geo engineers
# Author: Jung.Sohn
# All rights reserved.

import streamlit as st

## Sidebar ----------------------------------------------
password = st.sidebar.text_input('Password?', 'password')

#if password == st.secrets['db_password']:
if password == 'great':
  st.sidebar.text('This is for only bp teams')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','GoM_Kaskida'])
else:
  st.sidebar.text('Ask Jung for the pw')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','TBD'])

## Main --------------------------------------------------
st.markdown('# GeoSohn Apps by Jung')
#st.set_page_config(layout="wide") # wide / centered 
