# Name: MCMC
# Authour: Jung.Sohn
# Date: 05Jan24

import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
import streamlit as st

# =============================================================================
# Import raw data
df_Raw = pd.read_csv('https://github.com/jrson11/GeoSohn/blob/main/streamlit/input_MCMC_soil_layers/UW_PCPT_Robertson2010.csv')  

st.dataframe(df_Raw)
