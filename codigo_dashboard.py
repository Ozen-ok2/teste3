import paho.mqtt.client as mqtt
from datetime import datetime
import pandas as pd

# Variáveis globais para armazenar temporariamente os valores recebidos
current_time = None
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

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado com sucesso")
    else:
        print("Conectado com número de erro: " + str(rc))
    client.subscribe("sensor_HC-SR04/distancia")
    client.subscribe("sensor_HC-SR04/duracao")
    client.subscribe("sensor_HC-SR04/volume_ml")

def on_message(client, userdata, msg):
    global current_time, distancia, duracao, volume
    
    # Verificar o tópico da mensagem e processar de acordo
    if msg.topic == "sensor_HC-SR04/distancia":
        distancia = float(msg.payload.decode())
    elif msg.topic == "sensor_HC-SR04/duracao":
        duracao = float(msg.payload.decode())
    elif msg.topic == "sensor_HC-SR04/volume_ml":
        volume = float(msg.payload.decode())
    
    # Se todos os valores foram recebidos, adicionar à linha do CSV
    if all(val is not None for val in [distancia, duracao, volume]):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Abrir o arquivo CSV em modo de escrita e adicionar uma linha
        with open(csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([current_time, distancia, duracao, volume])
        # Resetar as variáveis
        current_time = distancia = duracao = volume = None

def iniciar_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("mqtt.eclipseprojects.io", 1883, 120)
    except Exception as e:
        print(f"Could not connect to MQTT server: {e}")

    # Configurar o loop MQTT em uma thread separada
    client.loop_forever()

iniciar_mqtt()
