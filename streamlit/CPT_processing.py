# =============================================================================
# Name: CPT_processing.py
# Authour: Jung.Sohn
# Date: 24Jan24
# All rights reserved
# =============================================================================

import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import matplotlib.patches as patches  
#from scipy.stats import multivariate_normal as mvn
#from scipy.stats import norm
import streamlit as st

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

# Title
st.title("In-situ CPT data processing")
st.write('- Because this runs MCMC everytime when I click any buttons below')
st.write('- Purpose: Uncertainty quantification')
st.write('- Method: MCMC calibration based on Bayesian method')


# =============================================================================
# Import raw data
st.subheader(':floppy_disk: Step 1: Import vertical soil data')
