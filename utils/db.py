from dotenv import load_dotenv
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import os
import streamlit as st

def conn_str_to_ss() -> str:
    
    load_dotenv()

    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    ipaddress = os.getenv('DB_IPADDRESS')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_DATABASE')

    st.session_state['conn_str']= f"postgresql://{user}:{password}@{ipaddress}:{port}/{database}"

def sql_to_ss():
    # Convert the series to a list of unique values
    msoa_list = st.session_state['dff']['MSOA code'].unique().tolist()
    
    # Convert the list to a string format suitable for SQL IN clause
    msoa_str = ', '.join(f"'{msoa}'" for msoa in msoa_list)
    
    # Create the SQL query
    base_sql = "SELECT * FROM msoa_2021_v6"
    if msoa_str:  # Add WHERE clause only if there are MSOA codes
         st.session_state['sql'] = f"{base_sql} WHERE msoa21cd IN ({msoa_str})"
    else:
         st.session_state['sql'] = base_sql  # No MSOA codes, return the base query without WHERE clause



def gdff_to_ss():
    """Fetches a filtered geopandas dataframe and saves it to session state"""
    # Make a connection string using secrets in .env
    conn_str_to_ss()
    # Make a sql engine using sqlalchemy
    engine = create_engine(st.session_state['conn_str'])
    # Connect to postgis DB
    connection = engine.connect()

    st.session_state['gdff'] = gpd.read_postgis(st.session_state['sql'], engine, geom_col='geom')
    connection.close()
    # Phew, that took me 20 hours to work! No joke!
