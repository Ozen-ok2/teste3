import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Home", page_icon="frontend/imagens/gen.ico")

# Dados
data = pd.read_csv('data.csv').rename({'Timestamp': 'timestamp', 'Distancia (cm)' : 'distancia', 'Duracao (ms)': 'duracao', 'Volume (ml)' : 'volume'})

st.subheader("Variação ao Longo do Tempo")
st.line_chart(data.set_index('duracao'))  # Linha para cada coluna, indexado pelo timestamp
