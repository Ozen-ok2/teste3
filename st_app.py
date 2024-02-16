from st_pages import Page, Section, show_pages
import streamlit as st

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("home.py", "Home", "🏫"),
        Page("teste_pag.py", "teste", "🏫"),
        Page("medicao_volume.py", "volume_teste", "💀")
    ]
)

st.switch_page("home.py")
