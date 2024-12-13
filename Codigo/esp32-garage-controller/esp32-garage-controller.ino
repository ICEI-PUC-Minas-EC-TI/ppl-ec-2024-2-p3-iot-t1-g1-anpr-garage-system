#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// Definições de estados e constantes
enum EstadoVaga {
  LIVRE,
  OCUPADA,
  RESERVADA
};

// Constantes para o servo
const int SERVO_ABERTO = 90;
const int SERVO_FECHADO = 0;
const int SERVO_PIN = 35;  

// Constantes de tempo
const unsigned long PUBLISH_INTERVAL = 2000;
const unsigned long DEBOUNCE_DELAY = 50;
const unsigned long WIFI_TIMEOUT = 10000;
const unsigned long CATRACA_TIMEOUT = 5000;
const unsigned long MQTT_RETRY_INTERVAL = 5000;
const unsigned long WIFI_CHECK_INTERVAL = 100;

// Definições MQTT
#define TOPICO_VAGAS "topico-painel-de-controle-vagas"
#define TOPICO_CATRACA "topico-painel-de-controle-catraca"
#define TOPICO_DETECTA "topico-carro-detectado"
#define TOPICO_VAGAS_OCUPADAS "topico-total-vagas-ocupadas"
#define ID_MQTT "IoT_Paulo_PUC_SG_mqtt"

// Configurações de rede 
const char* SSID = "Galaxy J6+2944";
const char* PASSWORD = "paulokjh17";
const char* BROKER_MQTT = "test.mosquitto.org";
const int BROKER_PORT = 1883;

// Estrutura para gerenciar uma vaga
struct Vaga {
  bool ocupada;
  bool reservada;
  int pinoSensor;
  int ledPins[3];  // R, G, B
  int ultimoEstadoSensor;
  unsigned long ultimoDebounceTime;
};

// Configuração do sistema
const int numVagas = 3;
Vaga vagas[numVagas] = {
  {false, false, 34, {26, 25, 33}, LOW, 0},  // Vaga 1
  {false, false, 14, {18, 19, 21}, LOW, 0},  // Vaga 2
  {false, false, 13, {15, 2, 4}, LOW, 0}     // Vaga 3
};

// Variáveis globais
WiFiClient espClient;
PubSubClient MQTT(espClient);
Servo catraca;
unsigned long ultimaPublicacao = 0;
unsigned long tempoCatracaAberta = 0;
unsigned long ultimaTentativaMQTT = 0;
unsigned long ultimaVerificacaoWiFi = 0;
bool catracaAtiva = false;

// Protótipos de funções
void initWiFi();
void initMQTT();
void verificaConexaoMQTT();
void verificaConexaoWiFi();
bool publicaMQTT(const char* topico, const char* mensagem);
void controlaCatraca(bool abrir);
void atualizaLED(int vagaIndex);
void processaSensor(int vagaIndex);
void publicaStatusVagas();

// Função de callback MQTT
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  
  Serial.printf("Mensagem recebida [%s]: %s\n", topic, msg.c_str());
  
  if (String(topic) == TOPICO_VAGAS) {
    if (msg.length() >= 2) {
      int vaga = msg[0] - '0' - 1; // Converte char para int e ajusta índice
      char comando = msg[1];
      
      if (vaga >= 0 && vaga < numVagas) {
        if (comando == 'r') {
          vagas[vaga].reservada = true;
          atualizaLED(vaga);
        }
      }
    }
  } else if (String(topic) == TOPICO_CATRACA) {
    if (msg == "abrir") {
      controlaCatraca(true);
    } else if (msg == "fechar") {
      controlaCatraca(false);
    }
  } else if (String(topic) == TOPICO_DETECTA && msg.length() > 0) {
    controlaCatraca(true);
    tempoCatracaAberta = millis();
    catracaAtiva = true;
  }
}

void verificaConexaoMQTT() {
  if (!MQTT.connected()) {
    unsigned long agora = millis();
    if (agora - ultimaTentativaMQTT >= MQTT_RETRY_INTERVAL) {
      Serial.print("Conectando ao broker MQTT...");
      if (MQTT.connect(ID_MQTT)) {
        Serial.println("Conectado!");
        MQTT.subscribe(TOPICO_VAGAS);
        MQTT.subscribe(TOPICO_CATRACA);
        MQTT.subscribe(TOPICO_DETECTA);
      } else {
        Serial.print("Falha, rc=");
        Serial.print(MQTT.state());
        Serial.println(" Tentando novamente mais tarde...");
      }
      ultimaTentativaMQTT = agora;
    }
  }
}

void verificaConexaoWiFi() {
  if (WiFi.status() != WL_CONNECTED) {
    unsigned long agora = millis();
    if (agora - ultimaVerificacaoWiFi >= WIFI_CHECK_INTERVAL) {
      Serial.print(".");
      ultimaVerificacaoWiFi = agora;
    }
    
    if (agora - ultimaVerificacaoWiFi >= WIFI_TIMEOUT) {
      Serial.println("\nFalha ao reconectar ao WiFi");
      WiFi.begin(SSID, PASSWORD);
      ultimaVerificacaoWiFi = agora;
    }
  }
}

void initWiFi() {
  Serial.println("Iniciando conexão WiFi");
  WiFi.begin(SSID, PASSWORD);
  unsigned long startTime = millis();
  
  while (WiFi.status() != WL_CONNECTED && millis() - startTime < WIFI_TIMEOUT) {
    unsigned long currentTime = millis();
    if (currentTime - ultimaVerificacaoWiFi >= WIFI_CHECK_INTERVAL) {
      Serial.print(".");
      ultimaVerificacaoWiFi = currentTime;
    }
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha na conexão WiFi");
  }
  
  WiFi.setSleep(false);
}

void initMQTT() {
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  MQTT.setCallback(mqtt_callback);
}

bool publicaMQTT(const char* topico, const char* mensagem) {
  if (!MQTT.connected()) return false;
  return MQTT.publish(topico, mensagem);
}

void controlaCatraca(bool abrir) {
  catraca.write(abrir ? SERVO_ABERTO : SERVO_FECHADO);
}

void atualizaLED(int vagaIndex) {
  if (vagaIndex < 0 || vagaIndex >= numVagas) return;
  
  Vaga& vaga = vagas[vagaIndex];
  
  // Desliga todos os LEDs primeiro
  for (int i = 0; i < 3; i++) {
    digitalWrite(vaga.ledPins[i], HIGH);
  }
  
  if (vaga.reservada) {
    // Amarelo (RED + GREEN)
    digitalWrite(vaga.ledPins[0], LOW);
    digitalWrite(vaga.ledPins[1], LOW);
  } else if (vaga.ocupada) {
    // Vermelho
    digitalWrite(vaga.ledPins[0], LOW);
  } else {
    // Verde
    digitalWrite(vaga.ledPins[1], LOW);
  }
}

void processaSensor(int vagaIndex) {
  if (vagaIndex < 0 || vagaIndex >= numVagas) return;
  
  Vaga& vaga = vagas[vagaIndex];
  int leitura = !digitalRead(vaga.pinoSensor);
  
  if (leitura != vaga.ultimoEstadoSensor) {
    vaga.ultimoDebounceTime = millis();
  }
  
  if ((millis() - vaga.ultimoDebounceTime) > DEBOUNCE_DELAY) {
    bool novoEstado = (leitura == HIGH);
    if (novoEstado != vaga.ocupada && !vaga.reservada) {
      vaga.ocupada = novoEstado;
      atualizaLED(vagaIndex);
      
      char mensagem[3];
      snprintf(mensagem, sizeof(mensagem), "%d%c", vagaIndex + 1, 
               vaga.ocupada ? 'o' : 'v');
      publicaMQTT(TOPICO_VAGAS, mensagem);
    }
  }
  
  vaga.ultimoEstadoSensor = leitura;
}

void publicaStatusVagas() {
  int vagasOcupadas = 0;
  for (int i = 0; i < numVagas; i++) {
    if (vagas[i].ocupada || vagas[i].reservada) vagasOcupadas++;
  }
  
  char mensagem[3];
  snprintf(mensagem, sizeof(mensagem), "%d", vagasOcupadas);
  publicaMQTT(TOPICO_VAGAS_OCUPADAS, mensagem);
}

void setup() {
  Serial.begin(115200);
  
  // Verifica memória disponível
  if (ESP.getFreeHeap() < 10000) {
    Serial.println("Aviso: Pouca memória disponível!");
  }
  
  // Configuração dos pinos
  for (int i = 0; i < numVagas; i++) {
    pinMode(vagas[i].pinoSensor, INPUT);
    for (int j = 0; j < 3; j++) {
      pinMode(vagas[i].ledPins[j], OUTPUT);
      digitalWrite(vagas[i].ledPins[j], HIGH);
    }
  }
  
  // Configuração do servo
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  catraca.setPeriodHertz(50);
  catraca.attach(SERVO_PIN, 500, 2400);
  controlaCatraca(false);
  
  // Inicialização das conexões
  btStop();  // Desliga Bluetooth
  initWiFi();
  initMQTT();
}

void loop() {
  unsigned long agora = millis();
  
  // Verifica conexões
  verificaConexaoMQTT();
  verificaConexaoWiFi();
  
  // Processa sensores
  for (int i = 0; i < numVagas; i++) {
    processaSensor(i);
    yield();
  }
  
  // Publica status periodicamente
  if (agora - ultimaPublicacao >= PUBLISH_INTERVAL) {
    publicaStatusVagas();
    ultimaPublicacao = agora;
  }
  
  // Controle automático da catraca
  if (catracaAtiva && (agora - tempoCatracaAberta >= CATRACA_TIMEOUT)) {
    controlaCatraca(false);
    catracaAtiva = false;
  }
  
  MQTT.loop();
}
