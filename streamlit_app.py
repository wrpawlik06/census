import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import subprocess
import zipfile
import os
import gdown
from tqdm import tqdm
from natsort import natsorted
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Constants
DEFAULT_MEDIAN_PRICE_THRESHOLD = 350000
DEFAULT_CHILDREN_PERCENTAGE_THRESHOLD = 0.22
DEFAULT_POPULATION_DENSITY_THRESHOLD = 2000
DEFAULT_TOP_AGE = 16

# Streamlit UI

median_price_threshold = st.slider("Median Price Threshold", 100000, 1000000, DEFAULT_MEDIAN_PRICE_THRESHOLD, 50000)
children_percentage_threshold = st.slider("Children Percentage Threshold", 0.0, 1.0, DEFAULT_CHILDREN_PERCENTAGE_THRESHOLD, 0.01)
population_density_threshold = st.slider("Population Density Threshold", 100, 10000, DEFAULT_POPULATION_DENSITY_THRESHOLD, 100)
#top_age = st.slider("Top Age for Child Percentage Calculation", 0, 20, DEFAULT_TOP_AGE, 1)

if st.button("Run Analysis"):
    progress_bar = st.empty()  # Define the progress bar placeholder here after the button
    progress_bar = progress_bar.progress(0)

    # Define your functions here
    def update_progress(progress, message):
        st.text(message)
        progress_bar.progress(progress)
    
    def build_ts_links() -> list:
        missing_files_indices = [14, 57, 43, 42, 69, 49]
        ts_count = 74
        ts_base_link = "https://www.nomisweb.co.uk/output/census/2021/census2021"
        links = []
        links.append("https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/housing/datasets/hpssadataset2medianhousepricebymsoaquarterlyrollingyear/current/hpssadataset2medianpricepaidbymsoa.zip")
        links.append('https://drive.google.com/uc?id=17bm9WWVn6R9gHxLvwirCafThKJAQ9v6x')
        for index in range(1, 75):
            if index not in missing_files_indices:
                if index < 10:
                    links.append(ts_base_link + f"-ts00{index}.zip")
                else:
                    links.append(ts_base_link + f"-ts0{index}.zip")
        return links

    def download_link(link):
        if "drive.google" in link:
            gdown.download(link, quiet=True)
        else:
            subprocess.run(["wget", link], stdout=subprocess.DEVNULL)

    def download_all_links():
        links = build_ts_links()
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(tqdm(executor.map(download_link, links), total=len(links), desc="Downloading files"))
        print("Downloads finished!")

    def extract_zip() -> list:
        for file in tqdm(os.listdir(), total=len(os.listdir()), desc="Unzipping files..."):
            if file.endswith(".zip"):
                file_path = os.path.join(os.getcwd(), file)
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(os.getcwd())
                except:
                    print(f"Failed to extract {file}!")
        print("Finished Unzipping!")

    def make_list_to_keep() -> list:
        files = ["streamlit_app.py", "requirements.txt"]
        for filename in os.listdir():
            if "msoa" in filename.lower() and "zip" not in filename.lower():
                files.append(filename)
                files.sort()
        return files

    def clean_directory(directory, files_to_keep):
        counter = 0
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path) and item not in files_to_keep:
                os.remove(item_path)
                counter += 1
        print(f"Deleted {counter} non-MSOA files.")

    def build_dataframes(tags_to_read) -> dict:
        all_files = os.listdir()
        dataframes = {}
        for filename in tqdm(all_files, desc="Building dataframes from files"):
            for file_tag in list(file_tags_to_descriptions.keys()):
                if file_tag in filename:
                    if ".csv" in filename:
                        dataframes[file_tag] = pd.read_csv(filename)
                    elif "HPSSA" in filename:
                        dataframes[file_tag] = pd.read_excel(filename, sheet_name="1a", skiprows=5, header=0)
                    else:
                        print(f"{filename} is of unknown data type, cannot be read.")
        return dataframes

    def join_dataframes(dataframes: dict) -> pd.DataFrame:
        df = pd.DataFrame()
        first_pass = True
        df_names = sorted(list(dataframes.keys()))
        for df_name in df_names:
            if first_pass:
                first_pass = False
                df = dataframes[df_name]
                print(f"Initializing main  dataframe with {df_name}.")
            else:
                print(f"Left joining {df_name} to main dataframe")
                right_cols = list(dataframes[df_name].columns.difference(['date', 'geography']))
                right_df = dataframes[df_name][right_cols]
                df = pd.merge(left=df, right=right_df, how="left", left_on="MSOA code", right_on="MSOA code")
        print(f"Success, MSOAs: {len(df)}, columns: {len(list(df.columns))}")
        return df

    def clean_population_density_ts006(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.replace("; measures: Value", "")
        df.rename(columns={"geography code": "MSOA code"}, inplace=True)
        return df

    def clean_HPSSA(df: pd.DataFrame, month_years: list) -> pd.DataFrame:
        cols_to_keep = ["MSOA code"]
        for col in dataframes['HPSSA'].columns:
            for year in month_years:
                if year in col:
                    cols_to_keep.append(col)
        return df[cols_to_keep]

    def dataframe_cleaner(dirty_dataframes: dict) -> dict:
        cleaned_dataframes = {}
        for key, df in tqdm(dirty_dataframes.items(), total=len(dirty_dataframes), desc="Cleaning Dataframes"):
            if key in cleaning_functions:
                cleaned_dataframes[key] = cleaning_functions[key](df)
            else:
                print(f"No specific cleaning function for {key}")
                cleaned_dataframes[key] = df
        print(f"Cleaned: {list(cleaned_dataframes.keys())}")
        return cleaned_dataframes

    def clean_age_ts007(df: pd.DataFrame, top_age: int, percentages: bool) -> pd.DataFrame:
        amount_meta_columns = 4
        max_col_index = amount_meta_columns + top_age + 1
        df.columns = df.columns.str.replace('Age: ', '').str.replace('; measures: Value', '')
        df.rename(columns={"Aged under 1 year": "Aged 0 years"}, inplace=True)
        df.rename(columns={"geography code": "MSOA code"}, inplace=True)
        df.drop(columns=df.columns[df.columns.str.contains("to")], inplace=True)
        df.drop(columns=df.columns[df.columns.str.contains("and")], inplace=True)
        output = df.iloc[:, :max_col_index]
        if percentages:
            for number_column in output.columns[4:]:
                percent_column = '%' + number_column
                output[percent_column] = output[number_column] / output['Total']
        return output

    # File descriptions
    file_tags_to_descriptions = {
        "ts006": "Population Density ts006",
        "ts007": "Age ts007",
        "HPSSA": "Median House Price HPSSA",
        "MSOA shapefiles": "MSOA Shapfiles 2021,"
    }

    # Run the pipeline
    update_progress(10, "Starting downloads...")
    download_all_links()
    update_progress(30, "Extracting files...")
    extract_zip()
    update_progress(50, "Cleaning directory...")
    clean_directory(directory=os.getcwd(), files_to_keep=make_list_to_keep())
    update_progress(60, "Building dataframes...")
    dataframes = build_dataframes(file_tags_to_descriptions.keys())
    
    cleaning_functions = {
        "ts007": lambda df: clean_age_ts007(df, top_age=top_age, percentages=True),
        "ts006": clean_population_density_ts006,
        "HPSSA": lambda df: clean_HPSSA(df, month_years=["Mar 2023"])
    }
    
    update_progress(70, "Cleaning dataframes...")
    clean_dataframes = dataframe_cleaner(dataframes)
    update_progress(80, "Joining dataframes...")
    df = join_dataframes(clean_dataframes)
    df = df[natsorted(df.columns)]
    df['% Aged 0 to 16'] = df[df.columns[0:16]].sum(axis=1)
    
    query_string = (
        f"`Population Density: Persons per square kilometre` >= {population_density_threshold} & "
        f"`Year ending Mar 2023` > {median_price_threshold} & "
        f"`% Aged 0 to 16` >= {children_percentage_threshold}"
    )
    
    df = df.query(query_string)
    print(f"Number of MSOAs after filtering: {len(df)}")

    update_progress(90, "Loading shapefiles and plotting map...")
    gpd_msoa = gpd.read_file("MSOA_2021_EW_BFC_V6.shp")
    gpd_msoa = gpd_msoa[gpd_msoa['MSOA21CD'].isin(df['MSOA code'])]
    gpd_msoa = gpd_msoa.to_crs(epsg=4326)
    
    map = folium.Map(location=[53.4084, -2.9916], tiles="OpenStreetMap", zoom_start=9)
    
    for _, r in tqdm(gpd_msoa.iterrows(), total=len(gpd_msoa), desc="Plotting Boundaries on a map..."):
        sim_geo = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
        folium.Popup(r["MSOA21CD"]).add_to(geo_j)
        geo_j.add_to(map)
    update_progress(100, "Rendering map...")

    folium_static(map)
