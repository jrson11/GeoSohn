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
# A. Functions
class ImportData:
    def __init__(self, file):
        self.PROJ = pd.read_excel(file, sheet_name="PROJ", header=2)
        self.LOCA = pd.read_excel(file, sheet_name="LOCA", header=2)
        self.GEOL = pd.read_excel(file, sheet_name="GEOL", header=2)
        self.SCPT = pd.read_excel(file, sheet_name="SCPT", header=2)

# Note: Use the raw file URL on GitHub to get the correct file content
url_Kaskida = "https://github.com/jrson11/GeoSohn/raw/main/streamlit/src_AGS/AGS_Kaskida(24Nov23).xlsx"
df_Kaskida = ImportData(url_Kaskida)

## Project Kaskida
#df_Kaskida = ImportData("https://github.com/jrson11/GeoSohn/blob/main/streamlit/src_AGS/AGS_Kaskida(24Nov23).xlsx")
#df_NaKika = ImportData("./src_AGS/AGS_NaKika(24Nov23).xlsx")
#df_Argos = ImportData("./src_AGS/AGS_Argos(24Nov23).xlsx")

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# B. Sidebar
pw_input = st.sidebar.text_input('Password = ', '?')
if pw_input == st.secrets['DB_pw']:
  selected_project = st.sidebar.selectbox("Select Project", ["All", "Kaskida", "Argos", "NaKika"])
else:
  selected_project = st.sidebar.selectbox("Select Project", ["None"])
    
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# C. Main

## Intro
selected_analysis = st.selectbox("Select Analysis", ["Data", "Site Investigation", "Lab Testing", "Shallow Foundation", "Deep Foundation", "Risk Assessment"])
st.image("https://raw.githubusercontent.com/jrson11/GeoSohn/main/docs/images/Canvas_of_Offshore_Geotech(Sep2023).png")

## Analysis
#if selected_analysis = 'Data':
#    data = DATA(selected_project)

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# D. Calculation

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# E. Control

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# F. Plot


