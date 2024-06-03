import streamlit as st
def display_dff():
    # Table for exporting and reading data
    if 'dff' in st.session_state:
        #temp_df = st.session_state['dff']

        # Formatting columns so they're more pleasing to the eye
        #temp_df['% Aged 0 to 4'] = temp_df['% Aged 0 to 4'].map('{:.0%}'.format)
        #temp_df['% Aged 0 to 16'] = temp_df['% Aged 0 to 16'].map('{:.0%}'.format)

        st.dataframe(st.session_state['dff'], use_container_width=True)
    else:
        st.write("(╯°□°）╯︵ ┻━┻) this is a placeholder for a table!")

def display_cluster_aggs():
    if 'cluster_labels' in st.session_state:
        st.dataframe(st.session_state['cluster_aggs'].round(0))