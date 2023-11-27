import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

## Setup main streamlit options
#st.set_page_config(layout="wide") # wide / centered 


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Functions

class Data:
    def __init__(self, selected_project):
        self.selected_project = selected_project

    def run(self):
        st.header(f"Imported Data for {self.selected_project}")

        # Load
        file_path = f"https://github.com/jrson11/GeoSohn/edit/main/streamlit/"
        file_K = "AGS_Kaskida_CSV.csv"
        df_K = pd.read_csv(file_path+file_K)

        # Check
        st.dataframe(df_K)



class SiteInvestigation:
    def __init__(self, selected_project):
        self.selected_project = selected_project

class SoilLabTesting:
    def __init__(self, selected_project):
        self.selected_project = selected_project

class ShallowFoundation:
    def __init__(self, selected_project):
        self.selected_project = selected_project
    
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Main

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
