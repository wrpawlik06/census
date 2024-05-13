import streamlit as st
import plotter
import builder

# Example usage within a Streamlit app
if st.button("Download Files"):
    builder.download_all_links()
    
plotter.plot_map()