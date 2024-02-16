import streamlit as st
import pandas as pd
import time

# Função para ler os dados do CSV e retornar apenas a última linha
def load_latest_csv_row():
    df = pd.read_csv("data.csv").tail(1)
    return df

# Configuração inicial do Streamlit
st.title("Medição de Volume")
col1, col2, col3 = st.columns(3)

# Inicialização dos placeholders com valores iniciais
placeholder_hora = col1.metric("Hora", "...")
placeholder_volume_percent = col2.metric("Volume (%)", "...")
placeholder_volume_ml = col3.metric("Volume (ml)", "...")

# Loop principal para atualizar os dados em tempo real
# Carregar a última linha do CSV
latest_row = load_latest_csv_row()

for index, row in latest_row.iterrows():
    # Extrair a parte da hora do timestamp
    hora = pd.to_datetime(row['Timestamp']).strftime('%H:%M:%S')

    # Calcular o volume em porcentagem em relação ao máximo de litros
    volume_ml = row['Volume (ml)']
    volume_percent = (volume_ml / 2000) * 100  # 1924.42184986 ml ou 2000 ml

    # Atualizar os valores na mesma linha
    placeholder_hora.metric("Hora", hora)
    placeholder_volume_percent.metric("Volume (%)", f"{volume_percent:.1f}%")
    placeholder_volume_ml.metric("Volume (ml)", volume_ml)

    # Aguardar 1 segundo antes de atualizar novamente
    st.rerun()
    time.sleep(1)