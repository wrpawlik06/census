import streamlit as st
from streamlit_folium import st_folium
import folium
import random
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from components.map import plot_points
from components.sliders import ranges_from_sliders
from components.text import title_header, criteria_matches, map_header
from utils.processing import load_data, create_query_strings_from, apply_filters
from utils.find_clusters import find_clusters, get_random_colour, assign_colours
# Set the page configuration
st.set_page_config(
    page_title="Find Your Market",  # Title that appears on the browser tab
    page_icon="🗺️",  # Icon that appears on the browser tab
    layout="centered",  # Other possible values: "wide"
    initial_sidebar_state="auto"  # Other possible values: "expanded", "collapsed"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df = None
    #st.session_state.gdf = None

# Displaying title
title_header()

# Initialize variables
#gdf = None
df = None

#to do - put caching in processing.py
# Load data once and cache it
def read_decision(data_loaded):
    """Deciding whether to read from the cache or the file"""
    if not data_loaded:
        with st.spinner('Loading awesome data & sliders ⏳...'):
            df = load_data()
            #geo_json = gdf.to_json()
            st.session_state.df = df
            #st.session_state.gdf = gdf
            #st.session_state.geo_json = geo_json
            data_loaded = True
            return data_loaded, df#, gdf, geo_json
    # If data is already cached, use it!
    else:
        df =  st.session_state.df
        #gdf = st.session_state.gdf
        #geo_json = st.session_state.geo_json
        return data_loaded, df#, gdf, geo_json

# Deciding to load data from file or from session state if it exists.
st.session_state.data_loaded, df = read_decision(st.session_state.data_loaded)

# Getting ranges from slicers
ranges = ranges_from_sliders()

# Create query string based on slider selections
# to do: Consider implementing list comprehension
query_strings = create_query_strings_from(ranges)

# Applying filters to get a dataframe and counts of matches
df_filtered, matches  = apply_filters(df,query_strings)

# Finding clusters for selected MSOAS
df_filtered['cluster'] = find_clusters(df_filtered)


# Displaying a text element
criteria_matches(df, df_filtered, matches)

# Displaying an interactive dataframe
st.dataframe(df_filtered)

# Displaying a map
map_header()
if len(df_filtered) > 0:
    # Colouring clusters
    cluster_colours = assign_colours(df_filtered)
    # Plotting points and colouring them
    m = plot_points(df_filtered,cluster_colours) 
    st_folium(m, width=700, height=500)
else:
    st.write("No data to map 😭!")

#filtered facts
# MSOAs
# total pop
# average(median pop value)
# pop distro
# Population pyramid for whole selection

# Create KDE plot for Population
#st.subheader("Population KDE Plot")
#fig, ax = plt.subplots()
#df_filtered['Population'].plot.kde(ax=ax)
#ax.set_title("KDE Plot of Population")
#st.pyplot(fig)


#aggregate facts

