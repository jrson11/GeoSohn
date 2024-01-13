import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import pandas as pd
import requests
from io import StringIO

# GitHub에서 데이터 불러오기
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/jrson11/GeoSohn/main/streamlit/input_CPTs_Fugro_TNW/TNW_20200508_FNLM_AGS4.0_V02_F-LOCA.csv'
    download = requests.get(url).text
    csv_raw = StringIO(download)
    df = pd.read_csv(csv_raw, header=3)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.iloc[:, 4], df.iloc[:, 5]))
    return gdf

gdf = load_data()

# Streamlit 애플리케이션 시작
st.title('CPT Data Points on Map')

# 지도 생성
m = folium.Map(location=[52.3676, 4.9041], zoom_start=7)  # 네덜란드의 암스테르담 근처를 중심으로 설정

# 마커 클러스터 추가
marker_cluster = MarkerCluster().add_to(m)
for idx, row in gdf.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=str(row['geometry'])).add_to(marker_cluster)

# Streamlit에 지도 표시
folium_static(m)
