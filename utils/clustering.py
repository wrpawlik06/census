
import hdbscan
import numpy as np
import streamlit as st
import random

# Function to find clusters and save cluster labels to the session state
def cluster_labels_to_ss():
    gdff = st.session_state['gdff']
    # Convert your data to a NumPy array
    coordinates = gdff[['lat', 'long']].to_numpy()

    # Initialize HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2, min_samples=1)

    # Fit the model
    st.session_state['cluster_labels'] = clusterer.fit_predict(coordinates)

    # Add cluster labels to the dataframe
    gdff['cluster'] = st.session_state['cluster_labels']
    st.session_state['gdff'] = gdff

    # Assign colors to clusters
    assign_colours()

# Function to generate a random color
def get_random_colour():
    r = lambda: random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r(), r(), r())

# Function to assign colors to clusters and save them to the session state
def assign_colours():
    gdff = st.session_state['gdff']
    unique_clusters = gdff['cluster'].unique()
    cluster_colours = {cluster: get_random_colour() for cluster in unique_clusters}
    gdff['colour'] = gdff['cluster'].map(cluster_colours)
    st.session_state['gdff'] = gdff


