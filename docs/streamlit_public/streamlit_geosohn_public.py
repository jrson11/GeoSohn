import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

## Setup main streamlit options
#st.set_page_config(layout="wide") # wide / centered 


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Main


# Main content
selected_option = st.selectbox("Select Analysis", ["Digitized Data", "Site Investigation", "Soil Lab Testing", "Shallow Foundation", "Deep Foundation", "Risk Assessment"])


# Sidebar
selected_project = st.sidebar.selectbox("Select Project", ["None", "Kaskida", "Argos", "NaKika"])
