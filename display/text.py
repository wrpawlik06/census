import streamlit as st

def title_header():
    st.header('🗺 Find Your Market', divider='rainbow')
    st.subheader("Use the sliders below to find your market :sunglasses:")

def map_header():
    st.header('📍See zones mapped as points.', divider='rainbow')
    st.subheader("☝This is the data from the table above.")

def criteria_matches(df, df_filtered, matches):
    st.write(f"Your 🏡Median Value criteria match {matches['house_price_matches']} ({int(matches['house_price_matches']/len(df)*100)}%) of zones.")
    st.write(f"Your children under 16 years old % criteria match {matches['children_16_prct_matches']} ({int(matches['children_16_prct_matches']/len(df)*100)}%) of zones.")
    st.write(f"Your children under 4 years old % criteria match {matches['children_4_prct_matches']} ({int(matches['children_4_prct_matches']/len(df)*100)}%) of zones.")
    st.write(f"Your population density criteria match {matches['pop_den_matches']} ({int(matches['pop_den_matches']/len(df)*100)}%) of zones.")
    st.write(f"Your combined criteria match {len(df_filtered)} ({int(len(df_filtered)/len(df)*100)}%) of zones.")

def sidebar_header():
    st.sidebar.image('display/wojtek mini.png', width=100, caption='PLACEHOLDER')
    st.header("Apply your filters here... ",divider='rainbow')

def display_total():

    # Work out the % of the total
    my_value = len(st.session_state['dff'] )/ len(st.session_state['df'])
    my_value_percentage = "{:.1%}".format(my_value)

    st.header(divider='rainbow',body=f"{len(st.session_state['dff'])} ({my_value_percentage}) of data zones match ALL of search criteria")

def warning_too_much_data():
    st.warning("Your selection is too large! Max 3000 Data Zones.")
