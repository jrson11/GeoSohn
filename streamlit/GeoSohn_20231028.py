import streamlit as st

# =======================================================
# Initialization 
# =======================================================

## Sidebar ----------------------------------------------
password = st.sidebar.text_input('Password?', 'password')

#if password == st.secrets['db_password']:
if password == 'bpbp':
  st.sidebar.text('This is for only bp teams')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','GoM_Kaskida'])
else:
  st.sidebar.text('Ask Jung for the pw')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','TBD'])

## Main --------------------------------------------------
st.markdown('# GeoSohn Apps by Jung')

  
# Display two columns
col1, col2 = st.columns(2)
#
with col1:
  st.text('col1')
with col2:
  st.text('col2')
  tab0,tab1,tab2,tab3,tab4,tab5 = st.tabs(['A.Map','B.Plasticity','C.Field.Su',"3.$S_u/σ'_{vc}$",'4.Norm.DSS','5.Est.DSS'])


