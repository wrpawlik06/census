import streamlit as st
from config import set_up_config
from display.sliders import sliders_to_ss
from display.text import sidebar_header, display_total,warning_too_much_data
from display.metrics import cards_placeholder, display_metrics, display_aggs
from utils.df_processing import df_to_ss, mm_to_ss, filters_to_ss, dff_to_ss, matches_to_ss, aggs_to_ss
from utils.db import sql_to_ss
from display.map import map_pipeline
from display.tables import display_dff, display_cluster_aggs
# Page setup
set_up_config()

# Initialize
#make session vars
if 'df' not in st.session_state:
    df_to_ss()
    mm_to_ss()
# This runs every time there is a change

# Draw Page
# sidebar for neat filtering
with st.sidebar:
    sidebar_header()
    # Using the "with" syntax
    with st.form(key='sliders'):

            sliders_to_ss()
            submit_button = st.form_submit_button(label='Submit Filters')

    # Update session state with slider ranges

    # Create a filtered dataframe (dff) based on slider values.
    # Only works if filters have already been used
    if 'median_price_range' in st.session_state:
        # Make filter strings
        filters_to_ss()

        # Make dff (not df!)
        dff_to_ss()

        # Calculate matches - how many zones match each criteria
        matches_to_ss()
        # make sql string
        sql_to_ss()


    # Displaying matches as neat cards
    else:
        cards_placeholder()

# Centre Pane
# Container to fit a map
# Now that we've used filters, display metrics
display_total()
display_metrics()

# Process map generation


# Using the "with" syntax
with st.form(key='map_container'):
    if 'dff' in st.session_state and len(st.session_state['dff']) > 3000:
        warning_too_much_data()
        submit_button = st.form_submit_button(label='We need fewer Data Zones', disabled=True)
    else:
        map_pipeline()
        submit_button = st.form_submit_button(label='Map again')


with st.container():


    # Displaying the filtered dataframe
    display_dff()

    if 'gdff' in st.session_state:
        # Making aggregates and sending them to session state
        aggs_to_ss()

        # Displaying aggregates
        display_aggs()
        display_cluster_aggs()


#st.write(st.session_state)
    #Processing
        # change session state vars
            #change filter string
            # change sql string

            #remake dff

        # get geo data
            #remake gdff





