
import hdbscan
import numpy as np
import streamlit as st
import random

def get_random_colour():
    colours = [
        'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 
        'beige', 'darkblue', 'darkgreen', 'cadetblue', 'pink', 'lightblue', 
        'lightgreen', 'gray', 'black'
    ]
    return random.choice(colours)

@st.cache_data
def find_clusters(df):
    # Convert your data to a NumPy array
    coordinates = df[['LAT', 'LONG']].to_numpy()

    # Initialize HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2, min_samples=1)

    # Fit the model
    cluster_labels = clusterer.fit_predict(coordinates)

    return cluster_labels

@st.cache_data
def assign_colours(df):
    unique_clusters = df['cluster'].unique()
    return {cluster: get_random_colour() for cluster in unique_clusters}