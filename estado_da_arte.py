import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Estado da Arte", page_icon="frontend/imagens/gen.ico")

st.title("Estado da Arte")
st.header("Tanques de armazenamento de água em residências")

st.markdown("Nos tanques de armazenamento de água em residências, os sensores ultrassônicos, como o HC-SR04, desempenham um papel crucial na medição e no monitoramento dos níveis de água. Esses sensores oferecem uma solução eficiente e confiável para garantir que os tanques estejam sempre abastecidos adequadamente, permitindo que os moradores utilizem a água de forma consciente e evite interrupções no fornecimento.")
st.image('mini-cisterna-captaco-de-agua-da-chuva-detalhes.jpg')

st.markdown("Os sensores ultrassônicos podem ser instalados nos tanques de armazenamento de água em residências para medir o nível de água disponível. Esses sensores utilizam ondas ultrassônicas para determinar a distância entre o sensor e a superfície da água, fornecendo dados precisos sobre o volume de água no tanque. Isso permite que os moradores monitorem facilmente o nível de água e saibam quando é necessário reabastecer o tanque.")
st.image('hc-sr04.jpeg')