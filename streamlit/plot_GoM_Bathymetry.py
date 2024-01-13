import streamlit as st
import folium
from streamlit_folium import folium_static

# Function to create the Folium map with bathymetric data
def create_map():
    # Latitude and longitude coordinates for the center of the Gulf of Mexico
    gulf_of_mexico_coords = [25.8419, -90.4184]

    # Create a Folium map
    folium_map = folium.Map(location=gulf_of_mexico_coords, zoom_start=5)

    # Add ESRI Ocean Basemap for bathymetric data
    esri_ocean = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='ESRI Ocean Basemap',
        overlay=False,
        control=True
    )

    esri_ocean.add_to(folium_map)

    # Add other markers and features here

    return folium_map

# Streamlit app
def main():
    st.title("Map of the Gulf of Mexico with Bathymetry")

    # Create the map
    map_object = create_map()

    # Display the map in the Streamlit app
    folium_static(map_object)

# Entry point of the application
if __name__ == "__main__":
    main()
