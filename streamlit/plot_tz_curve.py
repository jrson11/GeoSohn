import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def tz_curve(depths, tension, soil_stiffness):
    """
    Generate a T-Z curve for a pile.

    :param depths: Depths along the pile [m]
    :param tension: Tension in the pile [N]
    :param soil_stiffness: Soil stiffness coefficient [N/m2]
    :return: Tuple of depth (z) and corresponding tension (t)
    """
    z = np.array(depths)
    t = tension * np.exp(-soil_stiffness * z)
    return z, t
    
# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

# Streamlit app
st.title("T-Z Curve Generator for Pile Analysis")

# User inputs
depth = st.slider("Depth of the pile (m)", min_value=1.0, max_value=30.0, value=10.0, step=0.5)
tension = st.number_input("Tension in the pile (N)", min_value=0, value=10000, step=1000)
soil_stiffness = st.number_input("Soil stiffness coefficient (N/m²)", min_value=0, value=100, step=10)

# Generate and plot T-Z curve
if st.button('Generate T-Z Curve'):
    depths = np.linspace(0, depth, 100)
    z, t = tz_curve(depths, tension, soil_stiffness)
    
    plt.figure()
    plt.plot(t, z)
    plt.xlabel('Tension (N)')
    plt.ylabel('Depth (m)')
    plt.title('T-Z Curve for Pile')
    plt.gca().invert_yaxis()  # Invert y-axis to show depth increasing downwards
    plt.grid(True)
    st.pyplot(plt)

# Instructions to run the script
st.markdown("""
To run this script:
1. Save this code in a Python file, e.g., `tz_curve_app.py`.
2. Open a terminal and navigate to the directory containing the file.
3. Run the app using the command `streamlit run tz_curve_app.py`.
4. The app should open in your default web browser.
""")
