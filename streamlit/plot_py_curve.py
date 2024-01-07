import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def api_py_curve(depth, diameter, soil_stiffness, ultimate_stress):
    y = np.linspace(0, 0.1, 100)
    p = soil_stiffness * (depth ** 0.5) * diameter * np.tanh(ultimate_stress * y / (soil_stiffness * (depth ** 0.5) * diameter))
    return y, p

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

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


