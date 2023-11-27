import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

## Setup main streamlit options
#st.set_page_config(layout="wide") # wide / centered 


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# Main

# Sidebar
selected_project = st.sidebar.selectbox("Select Project", ["None", "Kaskida", "Argos", "NaKika"])

# Main content
selected_option = st.selectbox("Select Option", ["Data", "Site Investigation", "Soil Lab Testing", "Foundation Design"])
