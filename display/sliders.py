import streamlit as st
def sliders_to_ss():
    """
    Create sliders using the min and max values stored in the session state.
    
    This function creates sliders for various columns using the min and max 
    values previously calculated and stored in the session state.
    """
    st.session_state['median_price_range'] = st.slider(
        "Median Property Price", 
        min_value=int(st.session_state['Median Value_min']), 
        max_value=int(st.session_state['Median Value_max']), 
        value=(int(st.session_state['Median Value_min']), int(st.session_state['Median Value_max'])), 
        step=50000
    )
    
    st.session_state['children_16_percentage_range'] = st.slider(
        "Children under 16yrs Percentage", 
        min_value=float(st.session_state['% Aged 0 to 16_min']), 
        max_value=float(st.session_state['% Aged 0 to 16_max']), 
        value=(float(st.session_state['% Aged 0 to 16_min']), float(st.session_state['% Aged 0 to 16_max'])), 
        step=1.0
    )
    
    st.session_state['children_4_percentage_range'] = st.slider(
        "Children under 4yrs Percentage", 
        min_value=float(st.session_state['% Aged 0 to 4_min']), 
        max_value=float(st.session_state['% Aged 0 to 4_max']), 
        value=(float(st.session_state['% Aged 0 to 4_min']), float(st.session_state['% Aged 0 to 4_max'])), 
        step=1.0
    )
    
    st.session_state['population_density_range'] = st.slider(
        "Population Density", 
        min_value=int(st.session_state['Pop Density (ppl/sq km)_min']), 
        max_value=int(st.session_state['Pop Density (ppl/sq km)_max']), 
        value=(int(st.session_state['Pop Density (ppl/sq km)_min']), int(st.session_state['Pop Density (ppl/sq km)_max'])), 
        step=100
    )
