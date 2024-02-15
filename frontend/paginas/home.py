import streamlit as st, time
import pandas as pd
import numpy as np
from backend.codigo_dashboard import iniciar_mqtt, data

# Iniciar MQTT em uma thread separada
iniciar_mqtt()

# Configuração da página do Streamlit
st.set_page_config(page_title="Home", page_icon="frontend/imagens/gen.ico")
st.title("Trabalho de instrumentação eletrônica - Equipe 3")

# Função para receber dados apenas quando o botão é pressionado
#@st.cache_data
if st.button("Atualizar valores"):
    st.rerun()
# Função para atualizar automaticamente após um intervalo de tempo
def atualizar_pagina():
    st.rerun()


# Mostrar os dados - 15 linhas
st.table(data.tail(15))

# Função para atualizar a página após um intervalo de tempo
def atualizar_pagina():
    time.sleep(1)  # Espera 1 segundo
    st.rerun()  # Atualiza a página

# Atualizar automaticamente a página
#while True:
    #st.table(data)
    #atualizar_pagina()

df_tempo = data["Duração (ms)"]
df_distancia = data["Distância (cm)"]
df_volume = data["Volume (ml)"]

chart_data = pd.DataFrame ({
    "Distância" : df_distancia,
    "Volume" : df_volume    
})

st.line_chart(chart_data, x="col1", y="col2", color="col3")
