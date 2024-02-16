from st_pages import Page, Section, show_pages
import streamlit as st

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("home.py", "Home", "🏫"),
        Page("teste_pag.py", "teste", "🏫"),
        Page("medicao_volume.py", "volume_teste", "💀"),
        Page("estado_da_arte.py", "Estado da Arte", "🏫"),
        Page("apresentacao_codigoesp32.py", "Algoritmo do ESP32", "💀"),
        Page("apresentacao_codigomqtt.py", "Algoritmo do MQTT", "💀"),
        Page("apresentacao_volume.py", "Algoritmo de medição do volume", "💀"),
        Page("apresentacao_incertezas.py", "Algoritmo da medição de incertezas", "💀")
        
    ]
)

st.switch_page("home.py")
