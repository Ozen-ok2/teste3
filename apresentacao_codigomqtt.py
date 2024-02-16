import streamlit as st
# Título da apresentação
st.title("Código para Medição de Volume em Tempo Real")

# Declaração das bibliotecas utilizadas
st.subheader("Declaração das bibliotecas utilizadas")

code1 = '''import paho.mqtt.client as mqtt
from datetime import datetime
import pandas as pd'''
st.code(code1, language='python')

st.write("Neste trecho, importamos as bibliotecas necessárias para o funcionamento do código. O `paho.mqtt.client` é utilizado para a comunicação MQTT, enquanto `datetime` e `pandas` são usados para lidar com datas e manipulação de dados, respectivamente.")

# Variáveis globais e inicialização do arquivo CSV
st.subheader("Variáveis Globais e Inicialização do Arquivo CSV")

code2 = \
'''
# Variáveis globais para armazenar temporariamente os valores recebidos
hora_atual = None
distancia = None
duracao = None
volume = None

import csv
import os

# Nome do arquivo CSV
csv_filename = 'data.csv'

# Verificar se o arquivo CSV existe, se não existir, criar
if not os.path.exists(csv_filename):
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Distancia (cm)', 'Duracao (ms)', 'Volume (ml)'])
'''
st.code(code2, language='python')

st.write("Neste trecho, definimos as variáveis globais para armazenar os valores recebidos via MQTT, bem como inicializamos o arquivo CSV onde esses valores serão armazenados. Se o arquivo CSV não existir, ele será criado com os cabeçalhos necessários.")

# Funções de callback do MQTT e conexão
st.subheader("Funções de Callback do MQTT e Conexão")

code3 = \
'''
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado com sucesso")
    else:
        print("Conectado com número de erro: " + str(rc))
    client.subscribe("sensor_HC-SR04/distancia")
    client.subscribe("sensor_HC-SR04/duracao")
    client.subscribe("sensor_HC-SR04/volume_ml")

def on_message(client, userdata, msg):
    global hora_atual, distancia, duracao, volume
    
    # Verificar o tópico da mensagem e processar de acordo
    if msg.topic == "sensor_HC-SR04/distancia":
        distancia = float(msg.payload.decode())
    elif msg.topic == "sensor_HC-SR04/duracao":
        duracao = float(msg.payload.decode())
    elif msg.topic == "sensor_HC-SR04/volume_ml":
        volume = float(msg.payload.decode())
    
    # Se todos os valores foram recebidos, adicionar à linha do CSV
    if all(val is not None for val in [distancia, duracao, volume]):
        hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Abrir o arquivo CSV em modo de escrita e adicionar uma linha
        with open(csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([hora_atual, distancia, duracao, volume])
        # Resetar as variáveis
        hora_atual = distancia = duracao = volume = None

def iniciar_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("mqtt.eclipseprojects.io", 1883, 120)
    except Exception as e:
        print(f"Não foi possível se conectar ao servidor MQTT: {e}")

    # Configurar o loop MQTT em uma thread separada
    client.loop_forever()
'''
st.code(code3, language='python')

st.write("Aqui definimos as funções de callback para quando nos conectamos ao servidor MQTT e para quando uma mensagem é recebida. A função `on_connect` subscreve aos tópicos relevantes e a função `on_message` processa as mensagens recebidas, armazenando os valores no arquivo CSV.")

# Execução do MQTT
st.subheader("Execução do MQTT")

code4 = \
'''
iniciar_mqtt()
'''
st.code(code4, language='python')

st.write("Finalmente, chamamos a função `iniciar_mqtt()` para iniciar a comunicação MQTT e começar a receber os dados do sensor. Esta função configura o cliente MQTT, conecta-se ao servidor e inicia o loop MQTT para receber e processar as mensagens.")
