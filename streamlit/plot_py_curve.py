import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def api_py_curve(depth, diameter, soil_stiffness, ultimate_stress):
    y = np.linspace(0, 0.1, 100)
    p = soil_stiffness * (depth ** 0.5) * diameter * np.tanh(ultimate_stress * y / (soil_stiffness * (depth ** 0.5) * diameter))
    return y, p

# Streamlit app
st.title("P-Y Curve Generator for Offshore Pile Analysis")

# User inputs
depth = st.number_input("Embedment depth of the pile (m)", min_value=0.0, value=10.0, step=0.1)
diameter = st.number_input("Diameter of the pile (m)", min_value=0.0, value=1.5, step=0.1)
soil_stiffness = st.number_input("Subgrade reaction modulus of the soil (N/m3)", min_value=0, value=50000, step=1000)
ultimate_stress = st.number_input("Ultimate lateral stress of the soil (N/m2)", min_value=0, value=100000, step=1000)

# Generate and plot P-Y curve
if st.button('Generate P-Y Curve'):
    y, p = api_py_curve(depth, diameter, soil_stiffness, ultimate_stress)
    plt.figure()
    plt.plot(y, p)
    plt.xlabel('Lateral Displacement (m)')
    plt.ylabel('Lateral Pressure (N/m)')
    plt.title('P-Y Curve for Offshore Pile')
    plt.grid(True)
    st.pyplot(plt)

# Instructions to run the script
st.markdown("""
To run this script:
1. Save this code in a Python file, e.g., `py_curve_app.py`.
2. Open a terminal and navigate to the directory containing the file.
3. Run the app using the command `streamlit run py_curve_app.py`.
4. The app should open in your default web browser.
""")
