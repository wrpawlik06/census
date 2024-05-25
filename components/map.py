import folium

# Function to create Folium map
def plot_points(df, cluster_colours):
    # Create a folium map centered around the average location
    map_center = [df['LAT'].mean(), df['LONG'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    # Add markers with cluster-specific colors
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['LAT'], row['LONG']],
            popup=f"Cluster: {row['cluster']}",
            tooltip=f"Cluster: {row['cluster']}",
            icon=folium.Icon(color=cluster_colours[row['cluster']])
        ).add_to(m)
    return m