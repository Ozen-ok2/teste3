#include <WiFi.h>
#include <PubSubClient.h>
#include <time.h>

#define TRIGGER_PIN  26
#define ECHO_PIN     14

// Dimensões do recipiente (cilindro)
float raioCilindro = 8.25; // em centímetros
float alturaMaximaAgua = 9.0; // em centímetros
float alturaSensor = 13.0; // em centímetros
float m = 33.4;  // Coeficiente angular obtido pela calibração
float b = 0.11;  // Termo independente obtido pela calibração

const char* ssid = "BLACK"; 
const char* password = "LORY2022";  

const char* mqtt_server = "mqtt.eclipseprojects.io"; 

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;   
const int   daylightOffset_sec = 3600; 

WiFiClient espClient;
PubSubClient client(espClient);

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
  // Limitando o volume minimo a 0, pra não haver volumes negativos
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
  //int volumeLitrosInt = volumeLitros/1000; // Convertendo para inteiros

  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.print("cm | Duração: ");
  Serial.print(duracao/1000);
  Serial.print(" ms | Volume: ");
  //Serial.print(volumeLitros);
  //Serial.print(" litros ");
  Serial.print(volumeMililitros);
  Serial.println(" ml");

  // Simular leitura de temperatura

  //int temperatura = random(20, 30);
  //char temperaturaString[8];
  //sprintf(temperaturaString, "%d°C", temperatura);

  // Publicar no tópico de temperatura
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
  //Serial.print(volumeLitros);
  //Serial.print(" litros ");
  Serial.print(volumeMililitros);
  Serial.println(" ml");

  delay(1000);
}