import streamlit as st
import folium
from streamlit_folium import folium_static


## 스트림릿 타이틀
st.title("Map of the Gulf of Mexico")

## 기본이 되는 GoM
# Latitude and longitude coordinates for the center of the Gulf of Mexico
gulf_of_mexico_coords = [25.8419, -90.4184]

# Create a Folium map centered on the Gulf of Mexico
folium_map = folium.Map(location=gulf_of_mexico_coords, zoom_start=6)

# Projects in GoM
Kaskida_coords = [26.935, -91.401]
Mississippi_Canyon_coords = [28.0, -89.0]
Mad_Dog_coords = [27.5, -90.5]
Atlantis_coords = [29.0, -88.0] 
Whale_coords = [25,-92]

# Add markers on the GoM map
folium.Marker(Kaskida_coords, popup='Keathley Canyon Block 293').add_to(folium_map)
folium.Marker(Mississippi_Canyon_coords, popup='Mississippi Canyon Block 520').add_to(folium_map)
folium.Marker(Mad_Dog_coords, popup='Green Canyon Block 825').add_to(folium_map)
folium.Marker(Atlantis_coords, popup='Green Canyon Block 700').add_to(folium_map)
folium.Marker(Whale_coords, popup='Alaminos Canyon Block 772').add_to(folium_map)


## Placeholder coordinates for the corners of the rectangle

# 함수 정의
def add_rectangle_to_map(folium_map, northwest_corner, southeast_corner, color='#ff7800', fill_color='#ffff00', fill_opacity=0.2):
    folium.Rectangle(
        bounds=[northwest_corner, southeast_corner],
        color=color,
        fill=True,
        fill_color=fill_color,
        fill_opacity=fill_opacity
    ).add_to(folium_map)


# Replace these with the actual coordinates of Green Canyon Block 700
northwest_corner = [27.6, -90.6]
southeast_corner = [27.4, -90.4]

# Call the function to add a rectangle to the map
add_rectangle_to_map(folium_map, northwest_corner, southeast_corner)


## Display the map in the Streamlit app
folium_static(folium_map)

# Button to show the Wikipedia links
st.markdown('<a href="https://en.wikipedia.org/wiki/Kaskida_Oil_Field" target="_blank">Wiki: Kaskida Oil Field</a>', unsafe_allow_html=True)
st.markdown('<a href="https://en.wikipedia.org/wiki/Mississippi_Canyon" target="_blank">Wiki: Mississippi Canyon</a>', unsafe_allow_html=True)
st.markdown('<a href="https://en.wikipedia.org/wiki/Mad_Dog_oil_field" target="_blank">Wiki: Mad Dog oil field</a>', unsafe_allow_html=True)
st.markdown('<a href="https://www.offshore-technology.com/projects/atlantis-platform/"_blank">Offshore: Atlantis oil field</a>', unsafe_allow_html=True)
st.markdown('<a href="https://www.nsenergybusiness.com/projects/whale-field-development/" target="_blank">NS energy: Whale Field</a>', unsafe_allow_html=True)

