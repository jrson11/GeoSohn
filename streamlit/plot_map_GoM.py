import streamlit as st
import folium
from streamlit_folium import folium_static

st.title("Map of the Gulf of Mexico")

# Latitude and longitude coordinates for the center of the Gulf of Mexico
gulf_of_mexico_coords = [25.8419, -90.4184]

# Create a Folium map centered on the Gulf of Mexico
folium_map = folium.Map(location=gulf_of_mexico_coords, zoom_start=6)

# Projects in GoM
keathley_coords = [26.935, -91.401]        # Coordinates for Keathley Canyon Block 293
mississippi_canyon_coords = [28.0, -89.0]  # Coordinates for Mississippi Canyon MC 520
green_canyon_coords = [27.5, -90.5]        # Coordinates for Green Canyon Block 825

# Add a marker on the GoM map
folium.Marker(keathley_coords, popup='Keathley Canyon Block 293').add_to(folium_map)
folium.Marker(mississippi_canyon_coords, popup='Mississippi Canyon MC 520').add_to(folium_map)
folium.Marker(green_canyon_coords, popup='Green Canyon Block 825').add_to(folium_map)

# Display the map in the Streamlit app
folium_static(folium_map)


# Button to show the Wikipedia link
st.markdown('<a href="https://en.wikipedia.org/wiki/Kaskida_Oil_Field" target="_blank">Wiki: Kaskida Oil Field</a>', unsafe_allow_html=True)
st.markdown('<a href="https://en.wikipedia.org/wiki/Mississippi_Canyon" target="_blank">Wiki: Mississippi Canyon</a>', unsafe_allow_html=True)
st.markdown('<a href="https://en.wikipedia.org/wiki/Mad_Dog_oil_field" target="_blank">Wiki: Mad Dog oil field</a>', unsafe_allow_html=True)

