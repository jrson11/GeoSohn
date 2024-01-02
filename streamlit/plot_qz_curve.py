import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def elastic_settlement(load, area, modulus_of_elasticity, length):
    stress = load / area
    settlement = stress * length / modulus_of_elasticity
    return settlement

# Streamlit app
st.title("Load-Settlement Curve Generator for Axial Pile Analysis")

# User inputs
area = st.number_input("Cross-sectional area of the pile (m²)", min_value=0.0, value=1.0, step=0.1)
modulus_of_elasticity = st.number_input("Modulus of elasticity of the soil (N/m²)", min_value=1e6, value=50e6, step=1e6)
length = st.number_input("Length of the pile (m)", min_value=0.0, value=10.0, step=0.1)
max_load = st.number_input("Maximum axial load to consider (N)", min_value=1e5, value=1e6, step=1e5)

# Generate and plot Q-Z curve
if st.button('Generate Load-Settlement Curve'):
    loads = np.linspace(0, max_load, 100)
    settlements = [elastic_settlement(load, area, modulus_of_elasticity, length) for load in loads]
    
    plt.figure()
    plt.plot(settlements, loads)
    plt.xlabel('Settlement (m)')
    plt.ylabel('Axial Load (N)')
    plt.title('Load-Settlement Curve for Pile')
    plt.grid(True)
    st.pyplot(plt)

# Instructions to run the script
st.markdown("""
To run this script:
1. Save this code in a Python file, e.g., `load_settlement_app.py`.
2. Open a terminal and navigate to the directory containing the file.
3. Run the app using the command `streamlit run load_settlement_app.py`.
4. The app should open in your default web browser.
""")
