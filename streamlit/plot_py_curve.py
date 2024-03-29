import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

# =============================================================
# Streamlit app
st.title("p-y Curve")

depth = st.number_input("Embedment depth of the pile (m)", min_value=0.0, value=10.0, step=0.1)
diameter = st.number_input("Diameter of the pile (m)", min_value=0.0, value=1.5, step=0.1)
soil_stiffness = st.number_input("Subgrade reaction modulus of the soil (N/m3)", min_value=0, value=50000, step=1000)
ultimate_stress = st.number_input("Ultimate lateral stress of the soil (N/m2)", min_value=0, value=100000, step=1000)



# ----------------------------------------------------------------
# 1차 계산
st.header("Models for Clay")

## Matlock (1970)
st.subheader("Matlock(1970)")

st.write("$P_u = c_u D (3 + \gamma' / c_u *X + J* X / D)$")

Matlock_1970_static_y_over_y50 = np.arange(0,15,0.1)
Matlock_1970_static_p_over_pu = 0.5*Matlock_1970_static_y_over_y50**(1/3)

if st.button('Matlock Soft Clay(1970)'):
    plt.plot(Matlock_1970_static_y_over_y50, Matlock_1970_static_p_over_pu)
    plt.xlabel('y/y50')
    plt.ylabel('p/pc')
    plt.title('p-y curve')
    plt.grid(True)
    st.pyplot(plt)

## API 2002
st.subheader("API(2002)")

if st.button('API RP 2GEO(2002)'):
    plt.plot(API_2014_static_y_over_yc, API_2014_static_p_over_pu)
    plt.xlabel('y/yc')
    plt.ylabel('p/pc')
    plt.title('p-y curve')
    plt.grid(True)
    st.pyplot(plt)
    
## API 2014
st.subheader("API(2014)")

API_2014_static_p_over_pu = [0,0.23,0.33,0.5,0.72,1,1]
API_2014_static_y_over_yc = [0,0.1 ,0.3 ,1.0,3.0 ,8,15]


if st.button('API RP 2GEO(2014)'):
    plt.plot(API_2014_static_y_over_yc, API_2014_static_p_over_pu)
    plt.xlabel('y/yc')
    plt.ylabel('p/pc')
    plt.title('p-y curve')
    plt.grid(True)
    st.pyplot(plt)

# ----------------------------------------------------------------
# 2차 계산

st.header("Models for Sand")

st.write("$P_{us} = (C_1 X + C_2 D) \gamma' X$")



def api_py_curve(depth, diameter, soil_stiffness, ultimate_stress):
    y = np.linspace(0, 0.1, 100)
    p = soil_stiffness * (depth ** 0.5) * diameter * np.tanh(ultimate_stress * y / (soil_stiffness * (depth ** 0.5) * diameter))
    return y, p






