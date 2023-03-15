import streamlit as st

st.set_page_config(
    page_title='Home',
    page_icon='🏠'
)

st.title('Welcome to My Transaction Data Analysis Portfolio!')

st.sidebar.success('Select a page above.')

st.markdown(
    """
        Here is my project about **Analyzing Transaction Data**. The dataset for this project is **synthetically generated** using SDV library
        from a transaction data sample that I have.

        **👈 Select a page from the sidebar** to see the available pages

        **Visit my personal website to view my other projects**
        [here](https://www.michaelliem.com)
    """
)