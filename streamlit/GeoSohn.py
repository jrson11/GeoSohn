# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Purpose: To develop a Python script to manage geotechnical engineering skills
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
#    B. Setup
#    C. Sidebar (pw + project)
#    D. Main (Calculation + Control + Plot)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

## Setup main streamlit options
st.set_page_config(layout="wide") # wide / centered 


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# A. Functions
class ImportData:
    def __init__(self, file):
        self.PROJ = pd.read_excel(file, sheet_name="PROJ", header=2)
        self.LOCA = pd.read_excel(file, sheet_name="LOCA", header=2)
        self.GEOL = pd.read_excel(file, sheet_name="GEOL", header=2)
        self.SCPT = pd.read_excel(file, sheet_name="SCPT", header=2)


class SiteInvestigation:
    def __init__(self, df_project):
        self.df = df_project
        
    def run(self):
        st.dataframe(self.df.SCPT)
        
class LabTesting:
    def __init__(self, df_project):
        self.df = df_project
        
    def run(self):
        st.dataframe(self.df.IVAN)


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# B. Setup

# Note: Use the raw file URL on GitHub to get the correct file content
url_Kaskida = "./src_AGS/AGS_Kaskida(24Nov23).xlsx"
url_Argos = "./src_AGS/AGS_Argos(24Nov23).xlsx"
url_NaKika = "./src_AGS/AGS_NaKika(24Nov23).xlsx"
df_Kaskida = ImportData(url_Kaskida)
df_Argos = ImportData(url_Argos)
df_NaKika = ImportData(url_NaKika)

# Create a dictionary to store data frames based on project names
project_data = {
    'All': None,
    'Kaskida': df_Kaskida,
    'Argos': df_Argos,
    'NaKika': df_NaKika
}


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# C. Sidebar
selected_project = st.sidebar.selectbox("Select Project", ["All", "Kaskida", "Argos", "NaKika"])

#pw_input = st.sidebar.text_input('Password = ', '?')
#if pw_input == st.secrets['DB_pw']:
#  selected_project = st.sidebar.selectbox("Select Project", ["All", "Kaskida", "Argos", "NaKika"])
#else:
#  selected_project = st.sidebar.selectbox("Select Project", ["None"])

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# D. Main

## Intro
selected_analysis = st.selectbox("Select Analysis", ["AGS Data", "Site Investigation", "Lab Testing", "Shallow Foundation", "Deep Foundation", "Risk Assessment"])

# Display the image for 'All' projects
if selected_project == 'All':
    st.image("https://raw.githubusercontent.com/jrson11/GeoSohn/main/docs/images/Canvas_of_Offshore_Geotech(Sep2023).png")

# Check if the selected project is in the dictionary
elif selected_project in project_data:

    ## Analysis
    selected_df = project_data[selected_project]

    if selected_df:
        if selected_analysis == 'AGS Data':
            st.dataframe(selected_df.PROJ)

        elif selected_analysis == 'Site Investigation':
            SI = SiteInvestigation(selected_df)
            SI.run()
