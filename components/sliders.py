import streamlit as st

def ranges_from_sliders():
    median_price_range = st.slider("Median Price Range", 25000, 1600000, (100000,300000), 50000)
    children_16_percentage_range = st.slider("Children under 16yrs Percentage Range", 0.0,0.4, (0.15, 0.20), 0.01)
    children_4_percentage_range = st.slider("Children under 4yrs Percentage Range", 0.0,0.4, (0.0, 0.20), 0.01)
    population_density_range = st.slider("Population Density Range", 100, 10000, (5000,21589), 100)
    
    return {'median_price_range': median_price_range,
            "children_16_percentage_range": children_16_percentage_range,
            "children_4_percentage_range": children_4_percentage_range,
            "population_density_range": population_density_range}
