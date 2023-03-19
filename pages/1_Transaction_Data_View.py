import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import xlsxwriter
from io import BytesIO

st.set_page_config('Transaction Data Overview', layout='wide', initial_sidebar_state='auto', menu_items=None)
st.title('Transaction Data Overview')

# Load Excel file
df = pd.read_excel('transaction_data.xlsx').sort_values(by='reg_date')

# Sidebar filter for value selection
## HEADER
st.sidebar.header('Choose Filter Here:')

with st.sidebar.form(key ='Filter'):
    # ## CLIENT ID
    # all_client= st.checkbox("Select All Client IDs")
    # if all_client:
    #     client_filter = st.multiselect(
    #         "Select one or more Client IDs:",
    #         options=df['client_id'].unique(), 
    #         default=df['client_id'].unique()
    #     )
    # else:
    #     client_filter = st.multiselect(
    #         "Select one or more Client IDs:",
    #         options=df['client_id'].unique(),
    #         default=df['client_id'].iloc[0]
    #     )

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

    ## Product
    all_product = st.checkbox("Select All Products")
    if all_product:
        product_filter = st.multiselect(
            "Select one or more Products:",
            options=df['product'].unique(),
            default=df['product'].unique()
        )
    else:
        product_filter = st.multiselect(
            "Select one or more Products:",
            options=df['product'].unique(),
            default=df['product'].iloc[0]
        )

    ## Payment Method
    all_method = st.checkbox("Select All Payment Methods:")
    if all_method:
        method_filter = st.multiselect(
            "Select one or more Payment Methods:",
            options=df['payment_method_category'].unique(),
            default=df['payment_method_category'].unique()
        )
    else:
        method_filter = st.multiselect(
            "Select one or more Payment Methods:",
            options=df['payment_method_category'].unique(),
            default=df['payment_method_category'].iloc[0]
        )

    ## Transaction Date
    t_start_date_filter = st.date_input("Select Transaction START Date", value=df['transaction_date'].dt.date.min(), min_value=df['transaction_date'].dt.date.min(), max_value=df['transaction_date'].dt.date.max())
    t_end_date_filter = st.date_input("Select Transaction END Date (Included):", value=df['transaction_date'].dt.date.max(), min_value=t_start_date_filter, max_value=df['transaction_date'].dt.date.max())

    ## Status
    all_status = st.checkbox("Select All Statuses")
    if all_status:
        status_filter = st.multiselect(
            "Select one or more Statuses:",
            options=df['transaction_status'].unique(),
            default=df['transaction_status'].unique()
        )
    else:
        status_filter = st.multiselect(
            "Select one or more Statuses:",
            options=df['transaction_status'].unique(),
            default=df['transaction_status'].iloc[0]
        )

    ## Submit Button
    submitted = st.form_submit_button(label='Submit Filter')

# Filter the DataFrame based on selected column and value
filtered_df = df[
    # (df['client_id'].isin(client_filter)) &
    (df['lob'].isin(lob_filter)) &
    (df['reg_date'].dt.year.isin(year_filter)) &
    (df['product'].isin(product_filter)) &
    (df['payment_method_category'].isin(method_filter)) &
    (df['transaction_date'].dt.date >= t_start_date_filter) &
    (df['transaction_date'].dt.date < t_end_date_filter + timedelta(days=1)) &
    (df['transaction_status'].isin(status_filter))
].reset_index(drop=True)

# Print out dataframe
# dfSelection = df.query(
#     '''
#         lob in @lob_filter and reg_date in @year_filter
#     '''
# )

# if len(dfSelection):
#     st.dataframe(dfSelection)
# else:
#     st.dataframe(df)

st.dataframe(filtered_df)

# Download excel file
## Filtered Data
filtered_output = BytesIO()
filtered_writer = pd.ExcelWriter(filtered_output, engine='xlsxwriter')

filtered_df.to_excel(filtered_writer, index=False)
filtered_writer.close()

## All Data
all_output = BytesIO()
all_writer = pd.ExcelWriter(all_output, engine='xlsxwriter')
df.to_excel(all_writer, index=False)
all_writer.close()

## Download Button
dl_1, dl_2, _, _, _ = st.columns([1, 1, 1, 1, 1])
with dl_1:
    st.download_button("Download Filtered Data in Excel", data=filtered_output.getvalue(), file_name='transaction_filtered.xlsx', mime="application/vnd.ms-excel")
with dl_2: 
    st.download_button("Download All Data in Excel", data=all_output.getvalue(), file_name='transaction_all.xlsx', mime="application/vnd.ms-excel")