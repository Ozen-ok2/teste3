import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página do Streamlit
st.set_page_config(page_title="Home", page_icon="frontend/imagens/gen.ico")
st.title("Trabalho de instrumentação eletrônica - Equipe 3")

# Carregar os dados do arquivo CSV inicialmente
data = pd.read_csv('data.csv')

#st.table(data)

if not data.empty:
    # Gráfico de Linha para visualizar a variação ao longo do tempo
    st.subheader("Variação ao Longo do Tempo")
    st.line_chart(data.set_index('Timestamp'))  # Linha para cada coluna, indexado pelo timestamp
    
    # Histograma para visualizar a distribuição de distâncias
    st.subheader("Distribuição de Distâncias")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['Distancia (cm)'], bins=25, kde=True, ax=ax)
    st.pyplot(fig)  # Exibir o histograma
    
    # Kdeplot
    st.subheader("Volume x Distância")
    diamonds = sns.load_dataset('diamonds')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data=diamonds, x=data['Volume (ml)'])
    st.pyplot(fig)

    # Gráfico de dispersão para comparar distância e duração
    st.subheader("Dispersão: Distância vs. Duração")
    st.scatter_chart(data[['Distancia (cm)', 'Duracao (ms)']])  # Gráfico de dispersão
    
    # Gráfico de barras para visualizar o volume médio
    st.subheader("Volume Médio por Minuto")
    data['Minute'] = pd.to_datetime(data['Timestamp']).dt.second
    volume_avg = data.groupby('Minute')['Volume (ml)'].mean()
    st.bar_chart(volume_avg)  # Gráfico de barras
        
else:
    st.write("Nenhum dado disponível no momento.")

#time.sleep(1)
#st.rerun()

