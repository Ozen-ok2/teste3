from st_pages import Page, Section, show_pages
import streamlit as st

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("frontend/paginas/home.py", "Home", "🏫")
    ]
)

st.switch_page("frontend/paginas/home.py")
