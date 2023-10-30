import streamlit as st

# Initialization ----------------------------------------
st.markdown('# GeoSohn Apps by Jung')

## Sidebar
password = st.sidebar.text_input('Password?', 'password')

if password == st.secrets['db_password']:
  #st.text('Ask Jung for the pw')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','TBD'])
else:
  #st.text('This is for only bp teams')
  selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','GoM_Kaskida'])


'''
# Main --------------------------------------------------
def main():
  st.write('Assa')

# Membership --------------------------------------------
if password == st.secrets['db_password']:
  st.markdown('## Welcome to KUPEA')
  main()
  
else:
  st.markdown('## Please join KUPEA')
'''
