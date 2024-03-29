import paho.mqtt.client as mqtt
from datetime import datetime
import csv
import os

# Variáveis globais para armazenar temporariamente os valores recebidos
hora_atual = None
distancia = None
duracao = None
volume = None

# Nome do arquivo CSV
csv_filename = 'data.csv'

# Verificar se o arquivo CSV existe, se não existir, criar
if not os.path.exists(csv_filename):
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Escrever o cabeçalho do CSV
        writer.writerow(['Timestamp', 'Distancia (cm)', 'Duracao (ms)', 'Volume (ml)'])

# Callback de conexão ao MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado com sucesso")
    else:
        print("Conectado com número de erro: " + str(rc))
    # Subscrever aos tópicos relevantes
    client.subscribe("sensor_HC-SR04/distancia")
    client.subscribe("sensor_HC-SR04/duracao")
    client.subscribe("sensor_HC-SR04/volume_ml")

# Callback de recebimento de mensagem MQTT
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

# Função para iniciar o cliente MQTT
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

# Iniciar o cliente MQTT
iniciar_mqtt()
