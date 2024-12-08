#include <Arduino.h>//CODIGO CERTO
#include <WiFi.h>
#include <PubSubClient.h>

#define PIN_LED 2
#define PIN_LED2 22

/*
================================================
Funções do esp:
 - receber flag do espRaspberryConection.py
 - controlar o motor baseado nessa flag
 - publicar qual vaga está ou não ocupada
 - receber comandos para reservar uma vaga
================================================
*/

/* 
================================================
Definicoes para o MQTT 
================================================
*/
#define TOPICO_VAGAS "topico-painel-de-controle-vagas"
#define TOPICO_CATRACA "topico-painel-de-controle-catraca"
#define TOPICO_DETECTA "topico-carro-detectado"

#define ID_MQTT  "IoT_Paulo_PUC_SG_mqtt"

const char* BROKER_MQTT = "test.mosquitto.org";
int BROKER_PORT = 1883; // Porta do Broker MQTT

//celular
const char* SSID = "Galaxy J6+2944";
const char* PASSWORD = "paulokjh17";

//Variáveis e objetos globais
WiFiClient espClient; // Cria o objeto espClient
PubSubClient MQTT(espClient); // Instancia o Cliente MQTT passando o objeto espClient

long numAleatorio;


/* Prototypes */
void initWiFi(void);
void initMQTT(void);
void mqtt_callback(char* topic, byte* payload, unsigned int length);
void reconnectMQTT(void);
void reconnectWiFi(void);
void VerificaConexoesWiFIEMQTT(void);

/*
   Implementações
*/

/* Função: inicializa e conecta-se na rede WI-FI desejada
   Parâmetros: nenhum
   Retorno: nenhum
*/
void initWiFi(void)
{
  delay(10);
  Serial.println("------Conexao WI-FI------");
  Serial.print("Conectando-se na rede: ");
  Serial.println(SSID);
  Serial.println("Aguarde");

  reconnectWiFi();
}


/* Função: inicializa parâmetros de conexão MQTT(endereço do
           broker, porta e inicializa a função de callback)
   Parâmetros: nenhum
   Retorno: nenhum
*/
void initMQTT(void)
{
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);   //informa qual broker e porta deve ser conectado
  MQTT.setCallback(mqtt_callback);            //atribui função de callback (função chamada quando qualquer informação de um dos tópicos subescritos chega)
}

/* Função: função de callback
           esta função é chamada toda vez que uma informação de
           um dos tópicos subescritos chega)
   Parâmetros: nenhum
   Retorno: nenhum
*/
void mqtt_callback(char* topic, byte* payload, unsigned int length)
{
  String msg;

  /* obtem a string do payload recebido */
  for (int i = 0; i < length; i++)
  {
    char c = (char)payload[i];
    msg += c;
  }

  Serial.print("Chegou a seguinte string via MQTT: ");
  Serial.println(msg);
  /* toma ação dependendo da string recebida */

  /*
  ================================================
  Se topic == topico-painel-de-controle-vagas OU topico-painel-de-controle-catraca
    - se msg == valor numerico N(1-5), acende led[N-1] amarelo
    - se msg == "abrir", abre a catraca
    - se msg == "fechar", fecha a catraca

  Se topic == topico-carro-detectado
    - se msg == "detectado", abre a catraca por X segundos
  ================================================
  */
  
}
/* Função: reconecta-se ao broker MQTT (caso ainda não esteja conectado ou em caso de a conexão cair)
           em caso de sucesso na conexão ou reconexão, o subscribe dos tópicos é refeito.
   Parâmetros: nenhum
   Retorno: nenhum
*/
void reconnectMQTT(void)
{
  while (!MQTT.connected())
  {
    Serial.print("* Tentando se conectar ao Broker MQTT: ");
    Serial.println(BROKER_MQTT);
    if (MQTT.connect(ID_MQTT))
    {
      Serial.println("Conectado com sucesso ao broker MQTT!");
      MQTT.subscribe(TOPICO_SUBSCRIBE_LED);
    }
    else
    {
      Serial.println("Falha ao reconectar no broker.");
      Serial.println("Havera nova tentativa de conexao em 2s");
      delay(2000);
    }
  }  
}
/* Função: verifica o estado das conexões WiFI e ao broker MQTT.
           Em caso de desconexão (qualquer uma das duas), a conexão
           é refeita.
   Parâmetros: nenhum
   Retorno: nenhum
*/
void VerificaConexoesWiFIEMQTT(void)
{
  if (!MQTT.connected())
    reconnectMQTT(); //se não há conexão com o Broker, a conexão é refeita

  reconnectWiFi(); //se não há conexão com o WiFI, a conexão é refeita
}

/* Função: reconecta-se ao WiFi
   Parâmetros: nenhum
   Retorno: nenhum
*/
void reconnectWiFi(void)
{
  //se já está conectado à rede WI-FI, nada é feito.
  //Caso contrário, são efetuadas tentativas de conexão
  if (WiFi.status() == WL_CONNECTED)
    return;

  WiFi.begin(SSID, PASSWORD); // Conecta na rede WI-FI

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Conectado com sucesso na rede ");
  Serial.print(SSID);
  Serial.println("\nIP obtido: ");
  Serial.println(WiFi.localIP());
}


void setup() {
  Serial.begin(9600); //Enviar e receber dados em 9600 baud
  delay(1000);
  Serial.println("\nDisciplina IoT: acesso a nuvem via ESP32");
  delay(1000);
  // programa LED interno como saida

  /*
  ================================================
  alterar variaveis de sensores/atuadores
  ================================================
  */

  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_LED2, OUTPUT);
  
  digitalWrite(PIN_LED, HIGH);
  digitalWrite(PIN_LED2, HIGH);
  delay(1000);
  digitalWrite(PIN_LED, LOW);    // apaga o LED
  digitalWrite(PIN_LED2, LOW);

  /* Inicializa a conexao wi-fi */
  initWiFi();

  /* Inicializa a conexao ao broker MQTT */
  initMQTT();
}

// the loop function runs over and over again forever
void loop() {
/* garante funcionamento das conexões WiFi e ao broker MQTT */
  VerificaConexoesWiFIEMQTT();

  /*
  ================================================
  publicar info das vagas
  em um vetor de sensores, quais estão HIGH
  topico-painel-de-controle-vagas
  - enviar Nr ou Nl quando uma vaga ficar ocupada ou livre
  - enviar total de vagas ocupadas no vetor de sensores a cada X segundos
  ================================================
  */
  
  /* keep-alive da comunicação com broker MQTT */
  MQTT.loop();

  /*
  ================================================
    Refazer o ciclo após 2 segundos
  ================================================
  */
}
