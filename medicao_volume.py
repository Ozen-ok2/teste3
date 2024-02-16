import streamlit as st
import pandas as pd
import time

# Função para ler os dados em tempo real
def load_realtime_data():
    # Aqui você implementa a lógica para carregar os dados em tempo real
    # Por exemplo, pode ser a leitura de dados de um sensor, uma API, ou de outro lugar
    # Neste exemplo, vamos apenas retornar valores fictícios
    return [
        {"Timestamp": "2024-02-16 06:16:12", "Volume (ml)": 350.0},
        {"Timestamp": "2024-02-16 06:16:13", "Volume (ml)": 450.0},
        {"Timestamp": "2024-02-16 06:16:15", "Volume (ml)": 1050.0},
        {"Timestamp": "2024-02-16 06:16:15", "Volume (ml)": 350.0},
        {"Timestamp": "2024-02-16 06:16:16", "Volume (ml)": 0.0},  # Exemplo de leitura em 0
        {"Timestamp": "2024-02-16 06:16:17", "Volume (ml)": 0.0},  # Exemplo de leitura em 0
        {"Timestamp": "2024-02-16 06:16:18", "Volume (ml)": 0.0},  # Exemplo de leitura em 0
        {"Timestamp": "2024-02-16 06:16:19", "Volume (ml)": 0.0},  # Exemplo de leitura em 0
        {"Timestamp": "2024-02-16 06:16:20", "Volume (ml)": 0.0}   # Exemplo de leitura em 0
    ]

# Configurar o Streamlit
st.title("Medição de Volume")
col1, col2, col3 = st.columns(3)

# Inicializar placeholders com valores iniciais
placeholder_hora = col1.metric("Hora", "...")
placeholder_volume_percent = col2.metric("Volume (%)", "...")
placeholder_volume_ml = col3.metric("Volume (ml)", "...")

# Loop principal para atualizar os dados
while True:
    # Carregar os dados em tempo real
    data = load_realtime_data()
    
    for row in data:
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

