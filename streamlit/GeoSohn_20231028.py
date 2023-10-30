import streamlit as st

# Initialization ----------------------------------------
st.markdown('# GeoSohn Apps by Jung')
password = st.sidebar.text_input('Password?', 'password')

selected_app = st.sidebar.selectbox("Select an App", ['Mudmat_Moments','TBD'])


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
