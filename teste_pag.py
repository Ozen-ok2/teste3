import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo CSV
data = pd.read_csv('data.csv')

# Configuração da página do Streamlit
st.set_page_config(page_title="Visualização de Dados", page_icon=":bar_chart:")

# Título do aplicativo
st.title("Visualização de Dados")

# Gráfico de Linha para visualizar a variação ao longo do tempo
st.subheader("Variação ao Longo do Tempo")
fig, ax = plt.subplots()
ax.plot(data['Timestamp'], data['Distancia (cm)'], label='Distância (cm)')
ax.plot(data['Timestamp'], data['Duracao (ms)'], label='Duração (ms)')
ax.plot(data['Timestamp'], data['Volume (ml)'], label='Volume (ml)')
ax.set_xlabel('Tempo')
ax.set_ylabel('Valor')
ax.set_title('Variação ao Longo do Tempo')
ax.legend()
st.pyplot(fig)

# Histograma para visualizar a distribuição dos valores
st.subheader("Distribuição dos Valores")
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
axs[0].hist(data['Distancia (cm)'], bins=20, color='skyblue', edgecolor='black')
axs[0].set_title('Distância (cm)')
axs[0].set_xlabel('Valor')
axs[0].set_ylabel('Frequência')
axs[1].hist(data['Duracao (ms)'], bins=20, color='salmon', edgecolor='black')
axs[1].set_title('Duração (ms)')
axs[1].set_xlabel('Valor')
axs[1].set_ylabel('Frequência')
axs[2].hist(data['Volume (ml)'], bins=20, color='lightgreen', edgecolor='black')
axs[2].set_title('Volume (ml)')
axs[2].set_xlabel('Valor')
axs[2].set_ylabel('Frequência')
st.pyplot(fig)

# Gráfico de Dispersão para explorar a relação entre as variáveis
st.subheader("Relação entre as Variáveis")
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].scatter(data['Distancia (cm)'], data['Duracao (ms)'], color='orange', alpha=0.5)
axs[0].set_title('Distância vs. Duração')
axs[0].set_xlabel('Distância (cm)')
axs[0].set_ylabel('Duração (ms)')
axs[1].scatter(data['Distancia (cm)'], data['Volume (ml)'], color='purple', alpha=0.5)
axs[1].set_title('Distância vs. Volume')
axs[1].set_xlabel('Distância (cm)')
axs[1].set_ylabel('Volume (ml)')
st.pyplot(fig)
