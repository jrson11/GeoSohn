import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 데이터 로딩 함수
@st.cache  # Streamlit의 캐시 기능을 사용하여 데이터 로딩 성능 개선
def load_data(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return None

## Define FWD
def FWD(zq,zi,x1,x2):
    zi1 = zi[0:-1]    # depth index of Top layer
    zi2 = zi[1:]      # depth index of Bottom layer    
    z1 = []
    z2 = []
    x_dummy = []
    z_dummy = []
    nk = len(x1)
    for i in range(nk): # To check each layer
        z1.append(round(zq[zi1[i]],3))
        z2.append(round(zq[zi2[i]],3))
        x_dummy.append(x1[i])
        x_dummy.append(x2[i])
        z_dummy.append(round(zq[zi1[i]],3))
        z_dummy.append(round(zq[zi2[i]-1],3))
    z_dummy[-1] = zq[-1]
    yq = np.interp(zq, z_dummy, x_dummy)
    return yq

# 초기 지층 모델 생성 함수
def create_initial_stratigraphy_model(df_Raw):
    cols = df_Raw.columns
    z_header = cols[0]
    x_header = cols[1]
    zmin = min(df_Raw[z_header])
    zmax = max(df_Raw[z_header])
    xavg = round(np.mean(df_Raw[x_header]))
    xmin = round(min(df_Raw[x_header])*0.9)
    xmax = round(max(df_Raw[x_header])*1.1)

    dz = 0.2  # depth interval
    zq = np.arange(dz, zmax, dz)
    xq = np.interp(zq, df_Raw[z_header], df_Raw[x_header])
    nq = len(zq)

    nk = 5  # number of layers
    x1_ini = np.ones(nk)*xavg*0.95
    x2_ini = np.ones(nk)*xavg*1.05
    zi_ini = list(np.linspace(0, nq-1, nk+1).astype(int))

    xq_ini = FWD(zq, zi_ini, x1_ini, x2_ini)

    # Create and return figure
    fig, ax = plt.subplots(1, 2, figsize=(9, 6), dpi=100)
    ax[0].plot(df_Raw[x_header], df_Raw[z_header], '.', label='Raw data', alpha=0.2)
    ax[0].plot(xq, zq, 'k--', label='Interpolated')
    ax[0].set_title('Observed vertical profile')

    ax[1].plot(xq, zq, 'k--', label='Interpolated')
    ax[1].plot(xq_ini, zq, 'r--', label='Initial guess')
    ax[1].set_title('Initial stratigraphic model')

    for i in range(2):
        ax[i].set_xlim([xmin, xmax])
        ax[i].set_ylim([zmax, 0])
        ax[i].set_xlabel('UW (kN/m2)')
        ax[i].set_ylabel('Depth (m)')
        ax[i].grid(linestyle='dotted')
        ax[i].legend(loc=3, fancybox=True, shadow=True, fontsize=10)

    for j in range(nk):
        width = xmax - xmin
        height = zq[zi_ini[j+1]] - zq[zi_ini[j]]
        ax[1].add_patch(patches.Rectangle((xmin, zq[zi_ini[j]]), width, height, color=f'C{j}', alpha=0.1))

    plt.tight_layout()
    return fig

# 메인 함수
def main():
    st.title("MCMC 앱")

    # 데이터 로딩
    df = load_data('https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_MCMC_soil_layers/UW_PCPT_Robertson2010.csv')
    if df is not None:
        st.dataframe(df.head())  # 데이터 프레임 표시

        # 초기 지층 모델 생성 및 표시
        fig = create_initial_stratigraphy_model(df)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
