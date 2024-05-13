import folium
import streamlit.components.v1 as components

def plot_map():
    # Create a base map
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

    # Optionally, add some markers or layers
    folium.Marker([45.5236, -122.6750], popup='Hello from Portland!').add_to(m)


    # Render the map as HTML
    map_html = m._repr_html_()

    # Use components.html to display the map
    components.html(map_html, height=600)
