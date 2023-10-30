import streamlit as st

# =======================================================
# Initialization 
# =======================================================

## Sidebar ----------------------------------------------
password = st.sidebar.text_input('Password?', 'password')

#if password == st.secrets['db_password']:
if password == 'idk':
  st.sidebar.text('This is for only bp teams')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','GoM_Kaskida'])
else:
  st.sidebar.text('Ask Jung for the pw')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','TBD'])

## Main --------------------------------------------------
st.markdown('# GeoSohn Apps by Jung')
#st.set_page_config(layout="wide") # wide / centered 

if selected_app == 'Mudmat_Moments':
  st.markdown('## Mudmat Moments')
  
# Display two columns
col1, col2 = st.columns(2)
#
with col1:
  st.text('col1')
with col2:
  st.text('col2')
  tab0,tab1,tab2,tab3,tab4 = st.tabs(['1-Structural_Coordinates','2-Structural_Loads','3-','4-','5-'])

  with tab0:
    B = st.text_input('Width in x-axis (m) = ', value=10)
    L = st.text_input('Length in y-axis (m) = ', value=5)
    coordinates = st.selectbox('positive in z-axis', ['Upward','Downward'])
    #st.text(str(B))
    #st.text(str(L))

