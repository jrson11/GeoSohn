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
  st.title("Manage Ground Model")

# Membership --------------------------------------------
if password == st.secrets['DB_pw']:
  st.markdown('## Welcome to Database by JS')
  main()
  
else:
  st.markdown('## Sorry, this is confidential')

# Title
#st.write('- Purpose: To estimate Gmax from CPT data')
#st.write('- Method: Empirical equations based on Robertson2010')
