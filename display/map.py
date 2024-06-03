import folium
from folium import GeoJson, Circle
from streamlit_folium import st_folium
import streamlit as st
from utils.db import gdff_to_ss
from utils.clustering import cluster_labels_to_ss,cluster_aggs_to_ss
from utils.gdf_processing import clean_gdf_to_ss
from utils.df_processing import aggs_to_ss
import geopandas as gdf

def map_placeholder():
    st.write("🗺Your awesome map will go here!")


def map_to_ss():
    # Access DataFrame and GeoDataFrame from session state
    gdff = st.session_state['gdff']
    dff = st.session_state['dff']
    cluster_aggs = st.session_state['cluster_aggs'].round(0)


    # Merge the GeoDataFrame and DataFrame on MSOA_code
    gdff = gdff.merge(dff, on='MSOA code')
    gdff = gdff.rename(columns={'cluster_x':'cluster'})
    print(cluster_aggs.columns)
    print(gdff.columns)
    gdff = gdff.merge(cluster_aggs, on='cluster')


    # Initialize map centered on the first point
    m = folium.Map(location=[gdff["lat"].mean(), gdff["long"].mean()], zoom_start=8)

    # Add polygons and their centroids to the map
    for _, row in gdff.iterrows():
        tooltip_text = (
            f"MSOA Code: {row['MSOA code']}<br>"
            #f"MSOA Name: {row['MSOA2021NM']}<br>"

            #f"Population: {row['Population']}<br>"
            #f"Median Value: {row['Median Value']}<br>"
            #f"Population Density: {row['Pop Density (ppl/sq km)']}<br>"
            f"Cluster: {row['cluster']}<br>"
            f"Cluster Pop: {int(row['total_pop']/1000)}K<br>"
            f"Cluster Pop Under 16: {int(row['total_pop_under_16']/1000)}K<br>"
            f"Cluster Average Property Price: £{int(row['av_property_value']/1000)}K<br>"


        )
        # Add polygon
        # Add polygon with style
        GeoJson(
            row['geom'],
            style_function=lambda x, color=row['colour']: {'color': color, 'weight': 2, 'fillColor': color, 'fillOpacity': 0.5},
            highlight_function= lambda feat: {'fillColor': 'blue'},
            tooltip=folium.Tooltip(tooltip_text)

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
            aggs_to_ss()
            cluster_aggs_to_ss()
        else:
            st.write("❌📍 Skipping Clustering...")
        st.write("🗺Mapping data...")
        map_to_ss()
       


        status.update(label="Download complete!", state="complete", expanded=False)

    with st.spinner('Displaying...'):
        st.session_state['map'] = st_folium(st.session_state['map'], width=700, height=500)




