# Name: GeoSohn.py
# Purpose: To develop web app for geo engineers
# Author: Jung.Sohn
# All rights reserved.

import streamlit as st
#
import mudmat_moments as mm

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
st.markdown('# GeoSohn Web Apps')

if selected_app == 'Mudmat_Moments':
  # Display two columns
  col1, col2 = st.columns(2)
  #
  with col1:
    st.text('Data')
    tab1,tab2,tab3 = st.tabs(['1-Structural_Coordinates','2-Structural_Loads','3-'])
    
    with tab1:
      B = st.text_input('B in x-axis(m) = ',10)
      L = st.text_input('L in y-axis(m) = ',5)
      Zcoord = st.selectbox('Positive in z-axis',['Down','Up'])
      Origin = st.selectbox('Origin location',['Center','Left bottom','Right bottom'])
                            
    with tab2:
      st.text('tab2')
  
  with col2:
    st.text('Plots')




else:
  st.text('Choose an app')
