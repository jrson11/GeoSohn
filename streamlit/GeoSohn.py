# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Purpose: To develop python script to manage geotechnical engineering skills
# Author: J.S.
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Contents
#    1. Data (AGS format digitized)
#    2. Site Investigation (CPT + MV + TV)
#    3. Lab Testing
#    4. Shallow Foundation
#    5. Deep Foundation
#    6. Risk Assessment
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Structure
#    A. Functions
#    B. Sidebar (pw + project)
#    C. Main
#    D. Calculation
#    E. Control
#    F. Plot
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

## Setup main streamlit options
#st.set_page_config(layout="wide") # wide / centered 


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Functions
class A():
    a = 10

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Sidebar
    
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Main
selected_analysis = st.selectbox("Select Analysis", ["Digitized Data", "Site Investigation", "Soil Lab Testing", "Shallow Foundation", "Deep Foundation", "Risk Assessment"])
st.image("https://raw.githubusercontent.com/jrson11/GeoSohn/main/docs/images/Canvas_of_Offshore_Geotech(Sep2023).png")

'''
# Initialization
selected_analysis = st.selectbox("Select Analysis", ["Digitized Data", "Site Investigation", "Soil Lab Testing", "Shallow Foundation", "Deep Foundation", "Risk Assessment"])
st.image("https://raw.githubusercontent.com/jrson11/GeoSohn/main/docs/images/Canvas_of_Offshore_Geotech(Sep2023).png")

# Sidebar
pw_input = st.sidebar.text_input('Password = ', '?')
if pw_input == st.secrets['DB_pw']:
  selected_project = st.sidebar.selectbox("Select Project", ["All", "Kaskida", "Argos", "NaKika"])
else:
  selected_project = st.sidebar.selectbox("Select Project", ["None"])

# Main
if selected_analysis == 'Digitized Data':
    data = Data(selected_project)
    data.run()
elif selected_analysis == 'Site Investigation':
    site_investigation = SiteInvestigation(selected_project)
elif selected_analysis == 'Soil Lab Testing':
    soil_lab_testing = SoilLabTesting(selected_project)
elif selected_analysis == 'Shallow Foundation':
    shallow_foundation = ShallowFoundation(selected_project)
'''
