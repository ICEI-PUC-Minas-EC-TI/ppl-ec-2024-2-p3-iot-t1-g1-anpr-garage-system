import paho.mqtt.client as mqtt

# esta função é a função callback informando que o cliente se conectou ao servidor
def on_connect(client, userdata, flags, rc):
    print("Connectado com codigo "+str(rc))

    # assim que conecta, assina um tópico. Se a conexão for perdida, assim que
    # que reconectar, as assinaturas serão renovadas
    client.subscribe("topico_sensor_temperatura")

#funcao que publica uma flag no topicoFlag "" caso um carro seja detectado
def car_detection(placa):
    topicoFlag = ""

    """
    ====================================================================
    mandar a flag para o esp
    codigo no esp, ao receber a flag, abre a catraca por X segundos
    ====================================================================
    """

    """
    ====================================================================
    enviar a string da placa para dbConnection.py
    ====================================================================
    """