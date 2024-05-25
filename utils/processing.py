import pandas as pd
import geopandas as gpd
import streamlit as st

# Function to load data with caching
@st.cache_data
def load_data():
    
    # Loading data from file.
    gdf = gpd.read_file("data.gpkg")
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.001)

    # Converting to a crs system compatible with folium.
    gdf = gdf.to_crs(epsg=4326)

    # Creating a lightweight companion dataframe for manipulation
    df = pd.DataFrame(gdf.drop(columns=['geometry', "LONG", "LAT", "GlobalID", "BNG_N", "BNG_E"]))

    df.rename(columns={"Year ending Mar 2023":"Median Value",
                       "Total":"Population",
                       "Population Density: Persons per square kilometre":"Pop Density (ppl/sq km)"}
                       ,inplace=True)
    # Specifing interesting columns
    print(df.columns)
    i_cols = ["MSOA code","MSOA21NM", "Median Value", "Population", "% Aged 0 to 4", "% Aged 0 to 16", "Pop Density (ppl/sq km)"]
    df = df[i_cols]
    print(df.columns)

    return gdf, df

#Filter dataframe based on slicers
def create_query_strings_from(ranges):
    pop_density_query = (f"`Pop Density (ppl/sq km)` >= {ranges["population_density_range"][0]} & "
                f"`Pop Density (ppl/sq km)` <= {ranges["population_density_range"][1]}")

    children_16_query = (f"`% Aged 0 to 16` >= {ranges["children_16_percentage_range"][0]} & "
                    f"`% Aged 0 to 16` <= {ranges["children_16_percentage_range"][1]}")
    
    children_4_query = (f"`% Aged 0 to 4` >= {ranges["children_4_percentage_range"][0]} & "
                f"`% Aged 0 to 16` <= {ranges["children_4_percentage_range"][1]}")
    
    property_query = (f"`Median Value` >= {ranges["median_price_range"][0]} & "
                    f"`Median Value` <= {ranges["median_price_range"][1]}")
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
