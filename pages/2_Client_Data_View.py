import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config('Client Data Overview', layout='wide', initial_sidebar_state='auto', menu_items=None)
st.title('Client Data Overview')

# Load Excel file
df = pd.read_excel('transaction_data.xlsx')[['client_id', 'lob', 'reg_date']].drop_duplicates().sort_values(by='reg_date')

# Sidebar filter for value selection
## HEADER
st.sidebar.header('Choose Filter Here:')

with st.sidebar.form(key ='Filter'):
    ## LOB
    all_lob = st.checkbox("Select All LoBs")
    if all_lob:
        lob_filter = st.multiselect(
            "Select one or more LOBs:",
            options=df['lob'].unique(),
            default=df['lob'].unique(),
        )
    else:
        lob_filter = st.multiselect(
            "Select one or more LoBs:",
            options=df['lob'].unique(),
            default=df['lob'].iloc[0]
        )

    ## Reg Year
    all_year = st.checkbox("Select All Years")
    if all_year:
        year_filter = st.multiselect(
            "Select one or more Years:",
            options=df['reg_date'].dt.year.unique(), 
            default=df['reg_date'].dt.year.unique()
        )
    else:
        year_filter = st.multiselect(
            "Select one or more Years:",
            options=df['reg_date'].dt.year.unique(),
            default=df['reg_date'].dt.year.iloc[0]
        )

    ## Submit Button
    submitted = st.form_submit_button(label='Submit Filter')
    
# Filter the DataFrame based on selected column and value
filtered_df = df[
    # (df['client_id'].isin(client_filter)) &
    (df['lob'].isin(lob_filter)) &
    (df['reg_date'].dt.year.isin(year_filter))
].reset_index(drop=True)

# Print out dataframe
st.dataframe(filtered_df)