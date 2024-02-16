import streamlit as st
import pandas as pd
import time

# Função para ler os dados do CSV
def load_csv_data():
    # Ler o arquivo CSV
    df = pd.read_csv("data.csv")
    return df

# Configurar o Streamlit
st.title("Medição de Volume")
col1, col2, col3 = st.columns(3)

# Inicializar placeholders com valores iniciais
placeholder_hora = col1.metric("Hora", "...")
placeholder_volume_percent = col2.metric("Volume (%)", "...")
placeholder_volume_ml = col3.metric("Volume (ml)", "...")

# Loop principal para atualizar os dados
while True:
    # Carregar os dados do CSV
    df = load_csv_data()
    
    for index, row in df.iterrows():
        # Extrair apenas a parte da hora do timestamp
        hora = pd.to_datetime(row['Timestamp']).strftime('%H:%M:%S')  # Formato de hora: HH:MM:SS

        # Calcular o volume em porcentagem em relação aos 2 litros
        volume_ml = row['Volume (ml)']
        volume_percent = (volume_ml / 2000) * 100  # 2 litros = 2000 ml

        # Atualizar os valores na mesma linha
        placeholder_hora.metric("Hora", hora)
        placeholder_volume_percent.metric("Volume (%)", f"{volume_percent:.1f}%")
        placeholder_volume_ml.metric("Volume (ml)", volume_ml)

        # Aguardar 1 segundo antes de atualizar novamente
        time.sleep(1)
