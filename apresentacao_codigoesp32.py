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
