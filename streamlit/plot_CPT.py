import numpy as np
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

# 데이터 파일의 URL
url = 'https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_CPTs_Fugro_TNW/TNW_20200508_FNLM_AGS4.0_V02_F-SCPT.csv'

# 로버트슨 방법을 사용한 토양 분류 함수
def classify_soil(qc, fr):
    sigma_v0 = 100  # 가정된 수직 과부하 스트레스 (kPa)
    pa = 100  # 대기압 (kPa)
    Qtn = (qc / sigma_v0) * (pa / sigma_v0)**0.5
    Fr = (fr / qc) * 100  # 마찰비 (퍼센트)
    Ic = ((3.47 - np.log10(Qtn))**2 + (1.22 + np.log10(Fr))**2)**0.5
    if Ic < 2.6:
        return 'Sand'
    elif 2.6 <= Ic < 2.95:
        return 'Sandy Silt'
    elif 2.95 <= Ic < 3.6:
        return 'Clay'
    else:
        return 'Peat/Organic Soils'

def main():
    # 데이터 불러오기
    response = requests.get(url)
    csv_raw = StringIO(response.text)
    df_scpt = pd.read_csv(csv_raw, header=3)

    # qc 및 fr 값 추출
    qc = df_scpt.iloc[:, 4]  # Column E는 qc (콘 저항)
    fr = df_scpt.iloc[:, 5]  # Column F는 fr (측면 마찰)
    depth = df_scpt['0.05']  # Depth

    # 토양 분류
    soil_types = [classify_soil(q, f) for q, f in zip(qc, fr)]
    df_scpt['Soil Type'] = soil_types

    # 토양 유형별 깊이에 따른 분포 그래프
    plt.figure(figsize=(12, 6))
    for soil_type in set(soil_types):
        plt.plot(depth[df_scpt['Soil Type'] == soil_type], qc[df_scpt['Soil Type'] == soil_type], label=soil_type, linestyle='', marker='o')
    plt.gca().invert_yaxis()
    plt.xlabel('Depth (m)')
    plt.ylabel('qc (kPa)')
    plt.title('Soil Type Distribution with Depth')
    plt.legend()
    plt.grid(True)
    plt.show()

main()  # 메인 함수 실행
