import streamlit as st

def cards_placeholder():
    st.write("This is a placeholder for your briliant results (◠‿・)—☆")

    
def display_metrics():
    # Creating a list containing 4 empty columns
    cols = st.columns(len(st.session_state['matches']))

    # Initializing a counter
    index = 0

    # For metric, we assign it to a column
    for key in st.session_state['matches']:
        #TO DO: Better labels!
        my_label = f"Zones Matching {key}"

        # Work out the % of the total
        my_value = st.session_state['matches'][key] / len(st.session_state['df'])
        my_value_percentage = "{:.1%}".format(my_value)

        # Assign a metric to a column
        cols[index].metric(label=my_label, value=my_value_percentage)

        # Increment counter
        index += 1

        # Move onto next metric & column!

def display_aggs():
    # Creating a list containing 4 empty columns
    cols = st.columns(len(st.session_state['aggs']))

    # Initializing a counter
    index = 0

    # For metric, we assign it to a column
    for key in st.session_state['aggs']:
        #TO DO: Better labels!
        my_label = f"{key}"

        # Work out the % of the total
        my_value = (st.session_state['aggs'][key])
        my_value_formatted = "{:.0f}k".format(my_value / 1000)


        # Assign a metric to a column
        cols[index].metric(label=my_label, value=my_value_formatted)

        # Increment counter
        index += 1
