
import hdbscan
import numpy as np
import streamlit as st
import random
import pandas as pd
# Function to find clusters and save cluster labels to the session state
def cluster_labels_to_ss():
    np.random.seed(42)

    gdff = st.session_state['gdff']
    dff = st.session_state['dff']
    # Convert your data to a NumPy array
    coordinates = gdff[['lat', 'long']].to_numpy()

    # Initialize HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2, min_samples=1)

    # Fit the model
    st.session_state['cluster_labels'] = clusterer.fit_predict(coordinates)

    # Add cluster labels to the dataframe
    gdff['cluster'] = st.session_state['cluster_labels']
    dff['cluster'] = st.session_state['cluster_labels']
    st.session_state['gdff'] = gdff
    st.session_state['dff'] = dff


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


def cluster_aggs_to_ss():
    dff = st.session_state['dff']
    
    # Custom aggregation function for total population under 4 years of age
    def total_pop_under_4_agg(group):
        return (group['Population'] * group['% Aged 0 to 4'] / 100).sum()
    
    # Custom aggregation function for total population under 16 years of age
    def total_pop_under_16_agg(group):
        return (group['Population'] * group['% Aged 0 to 16'] / 100).sum()

    # Perform the aggregation
    cluster_aggregations = dff.groupby('cluster').apply(
        lambda group: pd.Series({
            'total_pop': group['Population'].sum(),
            'total_pop_under_4': total_pop_under_4_agg(group),
            'total_pop_under_16': total_pop_under_16_agg(group),
            'av_property_value': group['Median Value'].mean(),
            'av_pop_den': group['Pop Density (ppl/sq km)'].mean()
        })
    ).reset_index()

    st.session_state['cluster_aggs'] = cluster_aggregations

