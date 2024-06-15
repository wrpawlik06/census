import streamlit as st
from utils.df_processing import filters_strings_to_ss,dff_to_ss,matches_to_ss
from utils.db import sql_to_ss

def sliders_to_ss():
    """
    Create sliders using the min and max values stored in the session state.
    
    This function creates sliders for various columns using the min and max 
    values previously calculated and stored in the session state.
    """
    # Keeping the sliders in a form to prevent constant state changes.
    with st.form(key='sliders'):
        submit_button = st.form_submit_button(label='Submit Filters')

    # Sending slicer selection to session state
    # Calculate step size as 5% of the maximum value for each slider
        price_step = 25000
        children_16_step = 1.0
        children_4_step = 1.0
        density_step = 50

        st.session_state['median_price_range'] = st.slider(
            "Median Property Price (£)", 
            min_value=0, 
#            min_value=int(st.session_state['Median Value_min']), 
            max_value=1000000, 
            value=(0,1000000), 
            #max_value=int(st.session_state['Median Value_max']), 
            #value=(int(st.session_state['Median Value_min']),1000000), 
            step=price_step
        )
        
        st.session_state['children_16_percentage_range'] = st.slider(
            "Percentage of Children under 16 years old in a Data Zone", 
            min_value=float(st.session_state['% Aged 0 to 16_min']), 
            max_value=float(st.session_state['% Aged 0 to 16_max']), 
            value=(float(st.session_state['% Aged 0 to 16_min']), float(st.session_state['% Aged 0 to 16_max'])), 
            step=children_16_step
        )
        
        st.session_state['children_4_percentage_range'] = st.slider(
            "Percentage of Children under 4 years old in a Data Zone", 
            min_value=float(st.session_state['% Aged 0 to 4_min']), 
            max_value=float(st.session_state['% Aged 0 to 4_max']), 
            value=(float(st.session_state['% Aged 0 to 4_min']), float(st.session_state['% Aged 0 to 4_max'])), 
            step=children_4_step
        )
        
        st.session_state['population_density_range'] = st.slider(
            "Population Density (people per square km)", 
            min_value=0, 
            max_value=int(st.session_state['Pop Density (ppl/sq km)_max']), 
            value=(0, int(st.session_state['Pop Density (ppl/sq km)_max'])), 
            step=density_step
        )

# A convienent procedure to keeping things neat
def sliders_submitted_proc():
    """
    Process the submitted slider values and create a filtered dataframe.

    This function performs the following steps:
    1. Checks if 'median_price_range' exists in the session state.
    2. Generates filter strings based on slider values.
    3. Creates a filtered dataframe (dff) from the main dataframe (df).
    4. Calculates the number of matching zones for each criterion.
    5. Constructs an SQL string based on the filters.
    6. Writes a confirmation message to the Streamlit app.
    """
    # Create a filtered dataframe (dff) based on slider values.
    if 'median_price_range' in st.session_state:
        # Make filter strings
        filters_strings_to_ss()

        # Make dff (not df!)
        dff_to_ss()

        # Calculate matches - how many zones match each criteria
        matches_to_ss()
        # make sql string
        sql_to_ss()
