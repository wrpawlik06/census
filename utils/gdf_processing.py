import streamlit as st
import geopandas as gpd   

def clean_gdf_to_ss():
    st.session_state['gdff'] = st.session_state['gdff'].rename(columns={"msoa21cd": "MSOA code"}).to_crs(epsg=4326)
