import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Home", page_icon="frontend/imagens/gen.ico")

# Dados
data = pd.read_csv('data.csv')

st.subheader("Variação ao Longo do Tempo")
st.line_chart(data)  # Linha para cada coluna, indexado pelo timestamp
