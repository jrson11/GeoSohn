import numpy as np
import pandas as pd
import requests
from io import StringIO

# 데이터 파일의 URL
url = 'https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_CPTs_Fugro_TNW/TNW_20200508_FNLM_AGS4.0_V02_F-SCPT.csv'

# GitHub에서 데이터 불러오기
response = requests.get(url)
csv_raw = StringIO(response.text)
df_scpt = pd.read_csv(csv_raw, header=3)

# qc 및 fr 값 추출
qc = df_scpt.iloc[:, 4]  # Column E는 qc (콘 저항)을 나타냅니다.
fr = df_scpt.iloc[:, 5]  # Column F는 fr (측면 마찰)을 나타냅니다.

# 로버트슨 방법을 사용한 토양 분류
def classify_soil(qc, fr):
    # 정규화된 콘 저항(Qtn) 및 마찰비(Fr) 계산
    sigma_v0 = 100  # 가정된 수직 과부하 스트레스 (kPa)
    pa = 100  # 대기압 (kPa)
    Qtn = (qc / sigma_v0) * (pa / sigma_v0)**0.5
    Fr = (fr / qc) * 100  # 마찰비 (퍼센트)

    # 토양 행동 유형 지수 (Ic)
    Ic = ((3.47 - np.log10(Qtn))**2 + (1.22 + np.log10(Fr))**2)**0.5

    # Ic를 기반으로 한 토양 분류
    if Ic < 2.6:
        return 'Sand'
    elif 2.6 <= Ic < 2.95:
        return 'Sandy Silt'
    elif 2.95 <= Ic < 3.6:
        return 'Clay'
    else:
        return 'Peat/Organic Soils'

# 각 데이터 포인트에 대한 분류 적용
soil_types = [classify_soil(q, f) for q, f in zip(qc, fr)]

# 데이터프레임에 토양 유형 추가
df_scpt['Soil Type'] = soil_types

# 결과 표시
print(df_scpt[['0.05', 'Soil Type']].head())  # 깊이와 토양 유형 열 표시

