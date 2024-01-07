import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

def terzaghi_bearing_capacity(width, length, unit_weight, cohesion, phi, depth):
    """
    Calculate the ultimate bearing capacity using Terzaghi's formula.
    
    :param width: Width of the foundation [m]
    :param length: Length of the foundation [m]
    :param unit_weight: Unit weight of the soil [kN/m3]
    :param cohesion: Cohesion of the soil [kPa]
    :param phi: Angle of internal friction [degrees]
    :param depth: Depth of foundation [m]
    :return: Ultimate bearing capacity [kPa]
    """
    Nc = (np.tan(np.radians(45 + phi / 2))) ** 2
    Nq = np.tan(np.radians(phi)) ** 2 * np.exp(np.pi * np.tan(np.radians(phi)))
    Ny = (1.5 * (Nq - 1) * np.tan(np.radians(phi)))

    q_ult = cohesion * Nc + (unit_weight * depth) * Nq + 0.5 * unit_weight * width * Ny
    return q_ult

def elastic_settlement(q_applied, width, modulus_of_elasticity, poisson_ratio):
    """
    Calculate the settlement of a shallow foundation using the elastic theory.
    
    :param q_applied: Applied load per unit area [kPa]
    :param width: Width of the foundation [m]
    :param modulus_of_elasticity: Modulus of elasticity of the soil [kPa]
    :param poisson_ratio: Poisson's ratio of the soil
    :return: Settlement [mm]
    """
    settlement = (1 - poisson_ratio ** 2) * q_applied * width / (modulus_of_elasticity * np.pi)
    return settlement * 1000  # Convert to mm



# Streamlit app
st.title("Shallow Foundation Analysis")

# User inputs for bearing capacity
st.subheader("Bearing Capacity Analysis")
width = st.number_input("Width of the foundation (m)", min_value=0.0, value=2.0, step=0.1)
length = st.number_input("Length of the foundation (m)", min_value=0.0, value=2.0, step=0.1)
unit_weight = st.number_input("Unit weight of the soil (kN/m³)", min_value=0.0, value=18.0, step=1.0)
cohesion = st.number_input("Cohesion of the soil (kPa)", min_value=0.0, value=15.0, step=1.0)
phi = st.number_input("Angle of internal friction (degrees)", min_value=0.0, value=30.0, step=1.0)
depth = st.number_input("Depth of foundation (m)", min_value=0.0, value=1.0, step=0.1)

# User inputs for settlement analysis
st.subheader("Settlement Analysis")
q_applied = st.number_input("Applied load per unit area (kPa)", min_value=0.0, value=150.0, step=10.0)
modulus_of_elasticity = st.number_input("Modulus of elasticity of the soil (kPa)", min_value=1e3, value=1e4, step=1e3)
poisson_ratio = st.number_input("Poisson's ratio of the soil", min_value=0.0, max_value=0.5, value=0.3, step=0.05)

# Calculate and display results
if st.button('Calculate Bearing Capacity and Settlement'):
    q_ult = terzaghi_bearing_capacity(width, length, unit_weight, cohesion, phi, depth)
    settlement = elastic_settlement(q_applied, width, modulus_of_elasticity, poisson_ratio)
    
    st.write(f"Ultimate Bearing Capacity: {q_ult:.2f} kPa")
    st.write(f"Expected Settlement: {settlement:.2f} mm")

