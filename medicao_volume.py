import streamlit as st

col1, col2, col3 = st.columns(3)
col1.metric("Hora", "70 °F", "1.2 °F")
col2.metric("Distância", "9 mph", "-8%")
col3.metric("Volume", "86%", "4%")