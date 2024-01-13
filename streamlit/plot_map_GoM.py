import streamlit as st
import folium
from streamlit_folium import folium_static

# Function to create the Folium map
def create_map():
    # Latitude and longitude coordinates for the center of the Gulf of Mexico
    gulf_of_mexico_coords = [25.8419, -90.4184]

    # Create a Folium map centered on the Gulf of Mexico
    folium_map = folium.Map(location=gulf_of_mexico_coords, zoom_start=6)

    # (Optional) Add any markers or other features here

    return folium_map

# Streamlit app
def main():
    st.title("Map of the Gulf of Mexico")

    # Create the map
    map_object = create_map()

    # Display the map in the Streamlit app
    folium_static(map_object)

if __name__ == "__main__":
    main()
