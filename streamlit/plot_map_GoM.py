import streamlit as st
import folium
from streamlit_folium import folium_static

# Function to create the Folium map
def create_map():
    # Latitude and longitude coordinates for the center of the Gulf of Mexico
    gulf_of_mexico_coords = [25.8419, -90.4184]


    # Coordinates for Keathley Canyon Block 293 (example coordinates, replace with actual ones)
    keathley_coords = [26.935, -91.401]  # Replace with actual coordinates

    # Create a Folium map centered on the Gulf of Mexico
    folium_map = folium.Map(location=gulf_of_mexico_coords, zoom_start=6)


    # Add a marker for Keathley Canyon Block 293
    folium.Marker(keathley_coords, popup='Keathley Canyon Block 293').add_to(folium_map)
    

    return folium_map

# Streamlit app
def main():
    st.title("Map of the Gulf of Mexico")

    # Create the map
    map_object = create_map()

    # Display the map in the Streamlit app
    folium_static(map_object)


    # Button to show the Wikipedia link
    if st.button('Keathley Canyon'):
        st.markdown('<a href="https://en.wikipedia.org/wiki/Kaskida_Oil_Field" target="_blank">Learn more about Keathley Canyon</a>', unsafe_allow_html=True)

    if st.button('Mississippi Canyon'):
        st.markdown('<a href="https://en.wikipedia.org/wiki/Mississippi_Canyon" target="_blank">Learn more about Mississippi Canyon</a>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
