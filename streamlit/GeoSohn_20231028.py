import streamlit as st

# Initialization ----------------------------------------
st.markdown('# GeoSohn Apps by Jung')

## Sidebar
password = st.sidebar.text_input('Password?', 'password')

#if password == st.secrets['db_password']:
if password == 'bpbp':
  st.sidebar.text('This is for only bp teams')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','GoM_Kaskida'])
else:
  st.sidebar.text('Ask Jung for the pw')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','TBD'])



