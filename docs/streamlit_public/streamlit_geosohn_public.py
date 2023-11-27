import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

## Setup main streamlit options
#st.set_page_config(layout="wide") # wide / centered 


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Functions

    
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Main


# Main content
selected_option = st.selectbox("Select Analysis", ["Digitized Data", "Site Investigation", "Soil Lab Testing", "Shallow Foundation", "Deep Foundation", "Risk Assessment"])


# Sidebar
pw = st.sidebar = text_input('Password = ', '?')
if pw == st.secrets['DB_pw']:
  selected_project = st.sidebar.selectbox("Select Project", ["None", "Kaskida", "Argos", "NaKika"])
else:
  selected_project = st.sidebar.selectbox("Select Project", ["None"])

