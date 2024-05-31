import folium
from folium import GeoJson, Circle
from streamlit_folium import st_folium
import streamlit as st
from utils.db import gdff_to_ss
from utils.clustering import cluster_labels_to_ss
from utils.gdf_processing import clean_gdf_to_ss

def map_placeholder():
    st.write("🗺Your awesome map will go here!")


def map_to_ss():
    # Access DataFrame and GeoDataFrame from session state
    gdff = st.session_state['gdff']
    #dff = st.session_state['dff']

    # Initialize map centered on the first point
    m = folium.Map(location=[gdff["lat"].mean(), gdff["long"].mean()], zoom_start=6)

    # Add polygons and their centroids to the map
    for _, row in gdff.iterrows():
        # Add polygon
        # Add polygon with style
        GeoJson(
            row['geom'],
            style_function=lambda x, color=row['colour']: {'color': color, 'weight': 2, 'fillColor': color, 'fillOpacity': 0.5}
        ).add_to(m)       

        # Add centroid
        #Circle(
        #    location=[row['lat'], row['long']],
        #    radius=250,
        #    color=row['colour'],
        #    fill=True,
        #    fill_color=row['colour']
        #).add_to(m)
    # Save the map to session state
    st.session_state['map'] = m

def map_pipeline():
    with st.status("Downloading data...", expanded=True) as status:
        st.write("🐕‍🦺Fetching...")
        gdff_to_ss()
        st.write("🧼Cleaning...")
        clean_gdf_to_ss()
        if len(st.session_state['gdff']) > 1:
            st.write("📍Clustering...")
            cluster_labels_to_ss()
        else:
            st.write("❌📍 Skipping Clustering...")
        st.write("🗺Mapping data...")
        map_to_ss()
        status.update(label="Download complete!", state="complete", expanded=False)

    with st.spinner('Wait for it...'):
        st_folium(st.session_state['map'], width=700, height=500)




