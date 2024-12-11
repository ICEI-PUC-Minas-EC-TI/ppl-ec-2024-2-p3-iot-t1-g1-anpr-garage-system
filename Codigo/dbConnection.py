import paho.mqtt.client as mqtt
import requests

# importe o conector do Python com o MySQL: instalar novamente neste env (environment)
import mysql.connector

def on_connect(client, userdata, flags, rc):
    print("Connectado com codigo "+str(rc))

    # assim que conecta, assina um tópico. Se a conexão for perdida, assim que
    # que reconectar, as assinaturas serão renovadas
    """
    ====================================================================
    alterar tópico
    ====================================================================
    """
    client.subscribe("topico_sensor_temperatura")
    # esta função é a função callback que é chamada quando uma publicação é recebida do servidor
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico: " + msg.topic)
    print("Mensagem: "+ str(msg.payload.decode()) + "º")

    #ao receber um dado, insere como um registro da tabela dadosIoT
    """
    ====================================================================
    conectar com a api:
    placa vai ser recebida como msg(caracteres identificadores da placa)
    mandar placa formatada para a api
    retornar os dados do carro
    ====================================================================
    """
   
    # Decodificar a mensagem recebida
    placa = msg.payload.decode().strip()
    print(f"Placa recebida: {placa}")

    url = f"https://wdapi2.com.br/consulta/{placa}/c4709b65a108c070d36bae5b56bb1336"
    try:
        # Faz a requisição na API
        response = requests.get(url)
        response.raise_for_status()  

        data = response.json()

        # Extração das informações
        marca = data.get("MARCA", "Não encontrado")
        cor = data.get ("cor", "Não encontrado")
        modelo = data.get("MODELO", "Não encontrado")
        ano = data.get("ano", "Não encontrado")
        
        # Exibe as informações
        print(f"Marca: {marca}")
        print(f"Cor: {cor}")
        print(f"Modelo: {modelo}")
        print(f"Ano: {ano}")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError:
        print("Erro ao processar a resposta JSON.")

    """
    ====================================================================
    mandar os dados recebidos pela api para o banco de dados
    ====================================================================
    """
    
    if str(msg.payload.decode().strip()) == "termina":
        print("Recebeu comando termina.")
        


if __name__ == '__main__':
    # print_hi('Olá Turma.')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)
    #client.connect("broker.hivemq.com", 1883, 60) # broker alternativo

    # a função abaixo manipula trafego de rede, trata callbacks e manipula reconexões.
    client.loop_forever()