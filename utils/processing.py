import pandas as pd
import streamlit as st

# Function to load data with caching
@st.cache_data
def load_data():
    # Reading a lightweight  dataframe for manipulation
    df = pd.read_csv("data.csv")
    df["% Aged 0 to 16"] = df["% Aged 0 to 16"].round(2)
    df["% Aged 0 to 4"] = df["% Aged 0 to 4"].round(2)
    df["Pop Density (ppl/sq km)"]= df['Pop Density (ppl/sq km)'].round(0)
    df.drop(columns='Unnamed: 0',inplace=True)
    return df

#Filter dataframe based on slicers
def create_query_strings_from(ranges):
    pop_density_query = (f"`Pop Density (ppl/sq km)` >= {ranges['population_density_range'][0]} & "
                f"`Pop Density (ppl/sq km)` <= {ranges['population_density_range'][1]}")

    children_16_query = (f"`% Aged 0 to 16` >= {ranges['children_16_percentage_range'][0]} & "
                    f"`% Aged 0 to 16` <= {ranges['children_16_percentage_range'][1]}")
    
    children_4_query = (f"`% Aged 0 to 4` >= {ranges['children_4_percentage_range'][0]} & "
                f"`% Aged 0 to 16` <= {ranges['children_4_percentage_range'][1]}")
    
    property_query = (f"`Median Value` >= {ranges['median_price_range'][0]} & "
                    f"`Median Value` <= {ranges['median_price_range'][1]}")
    add = " & "
    combined_query = (pop_density_query + 
                      add + children_16_query +
                      add + children_4_query +
                      add + property_query
                    )
    return {"combined_query" : combined_query,
            "property_query" : property_query,
            "children_16_query" : children_16_query,
            "children_4_query" : children_4_query,
            "pop_density_query": pop_density_query
            }   

def apply_filters(df, strings):

# Filter data based on sliders
    df_filtered = df.query(strings["combined_query"])
    pop_den_matches = len(df.query(strings["pop_density_query"]))
    children_16_prct_matches = len(df.query(strings["children_16_query"]))
    children_4_prct_matches = len(df.query(strings["children_4_query"]))
    house_price_matches = len(df.query(strings["property_query"]))
    return df_filtered,{"house_price_matches" : house_price_matches,
                         "children_16_prct_matches" : children_16_prct_matches,
                         "children_4_prct_matches": children_4_prct_matches, 
                         "pop_den_matches" : pop_den_matches}  
