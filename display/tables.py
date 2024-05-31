import streamlit as st
def display_dff():
    # Table for exporting and reading data
    if 'dff' in st.session_state:
        dff = st.session_state['dff']
        # Formatting columns so they're more pleasing to the eye
        dff['% Aged 0 to 4'] = dff['% Aged 0 to 4'].map('{:.0%}'.format)
        dff['% Aged 0 to 16'] = dff['% Aged 0 to 16'].map('{:.0%}'.format)

        st.dataframe(dff, use_container_width=True)
    else:
        st.write("(╯°□°）╯︵ ┻━┻) this is a placeholder for a table!")