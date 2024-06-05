import streamlit as st
from display.text import sidebar_header
from display.sliders import sliders_to_ss, sliders_submitted_proc
from display.metrics import display_metrics
from utils.df_processing import df_to_ss, mm_to_ss
from display.map import display_map


# Initialize - loading dataframe to session state
#make session vars
if 'df' not in st.session_state:
    df_to_ss()
    mm_to_ss()

# Sidebar for a neat filter pane
with st.sidebar:
    sidebar_header()
    sliders_to_ss()
    sliders_submitted_proc()


# Container for map and metrics
st.title(body="🗺Find Your Market!")
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        display_map()
    with col2:
        # Now that we've used filters, display metrics
        display_metrics()