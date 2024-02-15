import paho.mqtt.client as mqtt
import time
from datetime import datetime
import pandas as pd
import numpy as np

# DataFrame para armazenar os dados
data = pd.DataFrame(columns=['Timestamp', 'Distância (cm)', 'Duração (ms)', 'Volume (ml)'])

# Variável global para controlar o status da conexão
is_connected = False

def on_connect(client, userdata, flags, rc):
    global is_connected
    if rc == 0:
        #print("Conectado com sucesso")
        is_connected = True
    else:
        #print("Conectado com número de erro: " + str(rc))
        is_connected = False
    client.subscribe("sensor_HC-SR04/distancia")
    client.subscribe("sensor_HC-SR04/duracao")
    client.subscribe("sensor_HC-SR04/volume_ml")

def on_message(client, userdata, msg):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Verificar o tópico da mensagem e processar de acordo
    if msg.topic == "sensor_HC-SR04/distancia":
        # Adicionar uma nova linha ao DataFrame apenas se o timestamp atual for diferente do último
        if len(data) == 0 or data.iloc[-1]['Timestamp'] != current_time:
            data.loc[len(data)] = [current_time, float(msg.payload.decode()), np.nan, np.nan]
    else:
        # Verificar se existe uma linha para o timestamp atual e atualizar os valores correspondentes
        if len(data) > 0 and data.iloc[-1]['Timestamp'] == current_time:
            if msg.topic == "sensor_HC-SR04/duracao":
                data.loc[len(data)-1, 'Duração (ms)'] = float(msg.payload.decode())
            elif msg.topic == "sensor_HC-SR04/volume_ml":
                data.loc[len(data)-1, 'Volume (ml)'] = float(msg.payload.decode())

def iniciar_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect("mqtt.eclipseprojects.io", 1883, 120)
    except Exception as e:
        print(f"Could not connect to MQTT server: {e}")

    # Configurar o loop MQTT em uma thread separada
    client.loop_start()
