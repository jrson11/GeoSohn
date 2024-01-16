import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 서브 스크립트에서 사이드바 링크 추가
from sidebar_links import add_sidebar_links
add_sidebar_links()

# Streamlit app
st.title("p-y Curve")

'''
# 지반 및 파일 특성
c = 100  # 토양 응력
phi = 30  # 토양의 마찰각 (degrees)
R = 0.3  # 파일 반경 또는 등가 지름 (m)

# 파일 횡향 변형 범위 및 단계
y_range = np.linspace(0, 1.0, 100)  # 횡향 변형 범위 (0부터 1까지)
delta_y = y_range[1] - y_range[0]  # 단계 크기

# 초기 조건 설정
p_prev = 0  # 초기 횡향 하중
p_max = 0  # 최대 횡향 하중

# 결과 저장을 위한 리스트
p_values = []

# 반복적인 p-y 곡선 계산
for y in y_range:
    # p-y 곡선 모델 (Matlock's Equation 예제)
    k = c * (R / 9.0) + np.tan(np.radians(phi)) * (R / 9.0)
    p = k * y
    
    # p-y 곡선 계산 결과 저장
    p_values.append(p)
    
    # 최대 횡향 하중 갱신
    if p > p_max:
        p_max = p

    # 반복 해석
    if abs(p - p_prev) < 1e-6:  # 수렴 조건 (예: 오차가 충분히 작을 때)
        break
    
    p_prev = p

# Generate and plot P-Y curve
# 결과 그래프 그리기
if st.button('Generate p-y Curve'):
    plt.plot(y_range, p_values)
    plt.xlabel('횡향 변형 (y)')
    plt.ylabel('횡향 하중 (p)')
    plt.title('반복 해석이 포함된 p-y 곡선')
    plt.grid(True)
    st.pyplot(plt)


def api_py_curve(depth, diameter, soil_stiffness, ultimate_stress):
    y = np.linspace(0, 0.1, 100)
    p = soil_stiffness * (depth ** 0.5) * diameter * np.tanh(ultimate_stress * y / (soil_stiffness * (depth ** 0.5) * diameter))
    return y, p





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
'''

