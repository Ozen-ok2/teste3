import streamlit as st

st.header("Código do ESP32 EM C")
st.subheader("Declarando #include utilizados")

code1 = ''' #include <WiFi.h>
#include <PubSubClient.h>
#include <time.h> '''

st.code(code1, language='c++')

st.write("No caso foram usadas algumas bibliotecas principais como `WiFi.h`, `PubSubClient.h` e `time.h`.")

code2 = \
'''
#define TRIGGER_PIN  26
#define ECHO_PIN     14

// Dimensões do recipiente (cilindro)
float raioCilindro = 8.25; // em centímetros
float alturaMaximaAgua = 9.0; // em centímetros
float alturaSensor = 13.0; // em centímetros
float m = 33.4;  // Coeficiente angular obtido pela calibração
float b = 0.11;  // Termo independente obtido pela calibração

const char* ssid = "***"; 
const char* password = "***";  
'''

st.code(code2, language='c++')

st.write("Aqui são definidas as variáveis e constantes utilizadas no código do ESP32 em C. Isso inclui os pinos do sensor de distância, as dimensões do recipiente (cilindro) para cálculo do volume, as credenciais de WiFi e outras variáveis necessárias para a conexão e operação do dispositivo.")


code3 = \
'''
const char* mqtt_server = "mqtt.eclipseprojects.io"; 

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;   
const int   daylightOffset_sec = 3600; 

WiFiClient espClient;
PubSubClient client(espClient);
'''

st.code(code3, language='c++')

st.write("Aqui são definidos os servidores MQTT e NTP, bem como as configurações relacionadas ao fuso horário. Também são inicializados os objetos para conexão WiFi e MQTT.")

code4 = \
'''
void printLocalTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Falha ao obter a hora");
    return;
  }
  Serial.printf("%02d:%02d:%02d ", timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);
}

float calcularVolume(float distancia, float raio) {
  
  float alturaAgua = alturaMaximaAgua - (distancia - (alturaSensor - alturaMaximaAgua));

  // Calculando o volume do cilindro usando a área da base e a altura da água
  float volume = PI * raio * raio * alturaAgua;
  // Limitando o volume mínimo a 0, para não haver volumes negativos
  volume = (volume < 0) ? 0 : volume;

  return volume;
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado");
  Serial.println("Endereço IP: " + WiFi.localIP().toString());

  // Inicializa a configuração NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  client.setServer(mqtt_server, 1883);

  while (!client.connected()) {
    Serial.println("Conectando ao MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado");
    } else {
      Serial.print("Falha na conexão, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("ESP32Client")) {
        Serial.println("Reconectado");
      } else {
        delay(5000);
      }
    }
  }
  client.loop();

  float duracao, distancia;
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  duracao = pulseIn(ECHO_PIN, HIGH);
  distancia = m * (duracao/1000.0) + b;
  //distancia = (((duracao) / 2.0) * 0.0343);
    
  // Cálculo do volume usando as dimensões do recipiente
  float volumeLitros = calcularVolume(distancia, raioCilindro);

  int volumeMililitros = volumeLitros; // Convertendo para mililitros

  // Publicar no tópicos correspondentes
  client.publish("sensor_HC-SR04/distancia", String(distancia).c_str());
  client.publish("sensor_HC-SR04/duracao", String(duracao/1000).c_str());
  client.publish("sensor_HC-SR04/volume_ml", String(volumeMililitros).c_str());

  // Imprimir no Serial Monitor a temperatura que foi publicada com o horário
  printLocalTime();
  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.print("cm | Duração: ");
  Serial.print(duracao/1000);
  Serial.print(" ms | Volume: ");
  Serial.print(volumeMililitros);
  Serial.println(" ml");

  delay(1000);
}
'''
st.code(code4, language='c++')

st.write("Aqui são definidas algumas funções auxiliares, como printLocalTime() para obter e imprimir a hora local, e calcularVolume() para calcular o volume do cilindro com base na distância medida pelo sensor. Também são definidos os métodos setup() e loop(), que são parte do padrão do Arduino e são usados para inicializar e executar o código principal, respectivamente.")

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

# Título da apresentação
st.header("Medição do volume no streamlit")

# Declaração das bibliotecas utilizadas
st.subheader("Declaração das bibliotecas utilizadas")

code1 = '''import streamlit as st
import pandas as pd
import time'''
st.code(code1, language='python')

st.write("Neste trecho, importamos as bibliotecas necessárias para o funcionamento do código. `streamlit` é utilizado para a criação da interface web, `pandas` para manipulação de dados e `time` para controlar o tempo de atualização dos dados.")

# Função para carregar os dados do CSV
st.subheader("Função para Carregar os Dados do CSV")

code2 = \
'''
def load_csv_data():
    # Ler o arquivo CSV e selecionar apenas a última linha
    df = pd.read_csv("data.csv").tail(1)
    return df
'''
st.code(code2, language='python')

st.write("A função `load_csv_data()` é responsável por carregar os dados do arquivo CSV. Neste caso, estamos lendo o arquivo e selecionando apenas a última linha, que contém os dados mais recentes.")

# Configuração inicial do Streamlit
st.subheader("Configuração Inicial do Streamlit")

code3 = \
'''
# Configurar o Streamlit
st.title("Medição de Volume")
col1, col2, col3 = st.columns(3)

# Inicializar placeholders com valores iniciais
placeholder_hora = col1.metric("Hora", "...")
placeholder_volume_percent = col2.metric("Volume (%)", "...")
placeholder_volume_ml = col3.metric("Volume (ml)", "...")
'''
st.code(code3, language='python')

st.write("Neste trecho, configuramos a interface do Streamlit. Criamos três colunas para exibir os dados de hora, volume em percentagem e volume em mililitros. Os valores iniciais dos placeholders são definidos como '...'.")

# Loop principal para atualizar os dados
st.subheader("Loop Principal para Atualizar os Dados")

code4 = \
'''
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
'''
st.code(code4, language='python')

st.write("Neste trecho, implementamos o loop principal responsável por atualizar os dados em tempo real. Primeiro, carregamos os dados do arquivo CSV utilizando a função `load_csv_data()`. Em seguida, iteramos sobre o DataFrame para extrair os valores de hora e volume. Finalmente, atualizamos os valores nos placeholders e aguardamos 1 segundo antes da próxima atualização.")

