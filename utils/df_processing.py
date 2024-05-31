import pandas as pd
import streamlit as st

# Function to load data with caching
def df_to_ss():
    """
    Load data from a CSV file, clean it, and store it in the session state.

    This function reads a CSV file named "data.csv", performs data cleaning and 
    rounding operations on specific columns, and stores the resulting DataFrame 
    in the Streamlit session state under the key 'df'.
    """
    df = pd.read_csv("data.csv")
    df["% Aged 0 to 16"] = df["% Aged 0 to 16"].round(2)
    df["% Aged 0 to 4"] = df["% Aged 0 to 4"].round(2)
    df["Pop Density (ppl/sq km)"] = df['Pop Density (ppl/sq km)'].round(0)
    df.drop(columns='Unnamed: 0', inplace=True)
    st.session_state['df'] = df

def mm_to_ss():
    """
    Calculate and store the minimum and maximum values for specified columns in the session state.

    This function calculates the minimum and maximum values for the columns 
    'Median Value', 'Population', '% Aged 0 to 4', '% Aged 0 to 16', and 
    'Pop Density (ppl/sq km)' in the DataFrame stored in the session state 
    under the key 'df'. It then stores these values in the session state with 
    appropriate keys.
    """
    cols = ['Median Value', 'Population', '% Aged 0 to 4', '% Aged 0 to 16', 'Pop Density (ppl/sq km)']
    for c in cols:
        min_var_name = f"{c}_min"
        max_var_name = f"{c}_max"

        st.session_state[min_var_name] = st.session_state['df'][c].min()
        st.session_state[max_var_name] = st.session_state['df'][c].max()
    st.session_state['mins_maxs_calculated'] = True

#Filter dataframe based on slicers
def filters_to_ss():
    """
    Create filter query strings based on session state slider values and store them in the session state.

    This function generates filter query strings for various columns based on the slider values stored
    in the session state. The generated queries are then stored in the session state.
    """
    pop_density_query = (f"`Pop Density (ppl/sq km)` >= {st.session_state['population_density_range'][0]} & "
                         f"`Pop Density (ppl/sq km)` <= {st.session_state['population_density_range'][1]}")

    children_16_query = (f"`% Aged 0 to 16` >= {st.session_state['children_16_percentage_range'][0]} & "
                         f"`% Aged 0 to 16` <= {st.session_state['children_16_percentage_range'][1]}")
    
    children_4_query = (f"`% Aged 0 to 4` >= {st.session_state['children_4_percentage_range'][0]} & "
                        f"`% Aged 0 to 4` <= {st.session_state['children_4_percentage_range'][1]}")
    
    property_query = (f"`Median Value` >= {st.session_state['median_price_range'][0]} & "
                      f"`Median Value` <= {st.session_state['median_price_range'][1]}")

    combined_query = " & ".join([pop_density_query, children_16_query, children_4_query, property_query])

    # Store the queries in the session state
    st.session_state['queries'] = {
        "combined_query": combined_query,
        "property_query": property_query,
        "children_16_query": children_16_query,
        "children_4_query": children_4_query,
        "pop_density_query": pop_density_query
    }


def dff_to_ss():
    """
    Filter the DataFrame based on the slider values and update the session state with the filtered DataFrame and match counts.

    This function filters the DataFrame stored in the session state using the combined query string 
    and updates the session state with the filtered DataFrame and the number of matches for each individual query.
    """
    df = st.session_state['df']
    queries = st.session_state['queries']

    # Filter data based on the combined query
    df_filtered = df.query(queries["combined_query"])
    
    # Dropping cols we don't need
    # SPOILER ALERT: We will use filtered geodataframe (gdff) for plotting centroids
    df_filtered.drop(columns =['LAT','LONG'],inplace=True)
    st.session_state['dff'] = df_filtered

def matches_to_ss():
    """
    Calculate the number of matches for each filter criterion and update the session state.

    This function calculates the number of rows in the DataFrame stored in the session state
    that match each of the individual query criteria stored in the session state. It then updates
    the session state with these match counts, which can be used to populate visual components,
    such as cards in the sidebar, to display the number of matches for each criterion.
    """

    df = st.session_state['df']
    queries = st.session_state['queries']

    # Calculate the number of matches for each individual query
    pop_den_matches = len(df.query(queries["pop_density_query"]))
    children_16_prct_matches = len(df.query(queries["children_16_query"]))
    children_4_prct_matches = len(df.query(queries["children_4_query"]))
    house_price_matches = len(df.query(queries["property_query"]))

    # Update session state with the filtered DataFrame and match counts
    st.session_state['matches'] = {
        "house_price_matches": house_price_matches,
        "children_16_prct_matches": children_16_prct_matches,
        "children_4_prct_matches": children_4_prct_matches,
        "pop_den_matches": pop_den_matches
    }

def aggs_to_ss():
    dff = st.session_state['dff']

    total_pop = dff['Population'].sum()
    total_pop_under_4 = (dff['Population']*dff['% Aged 0 to 4']).sum()
    total_pop_under_16 = (dff['Population']*dff['% Aged 0 to 16']).sum()
    av_value = dff['Median Value'].mean()
    av_pop_den = dff['Pop Density (ppl/sq km)'].mean()

    st.session_state['aggs'] = {
        'total_pop':total_pop,
        'total_pop_under_4':total_pop_under_4,
        'total_pop_under_16':total_pop_under_16,
        'av_value':av_value,
        'av_pop_den':av_pop_den

    }