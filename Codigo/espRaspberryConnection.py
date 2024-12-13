import paho.mqtt.client as mqtt

topicoFlag = "topico-carro-detectado"

# esta função é a função callback informando que o cliente se conectou ao servidor
def on_connect(client, userdata, flags, rc):
    print("Connectado com codigo "+str(rc))

    # assim que conecta, assina um tópico. Se a conexão for perdida, assim que
    # que reconectar, as assinaturas serão renovadas
    client.subscribe(topicoFlag)

#funcao que publica uma flag no topicoFlag "" caso um carro seja detectado
def car_detection(placa):

    """
    ====================================================================
    - mandar a flag para o esp
    (codigo no esp, ao receber a flag, abre a catraca por X segundos)
    - enviar a string da placa para dbConnection.py
    ====================================================================
    """
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("test.mosquitto.org", 1883, 60)

        result = client.publish(topicoFlag, placa)

        client.loop_start()
        client.loop_stop()
        
        client.disconnect()

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Mensagem publicada com sucesso: {placa}")
        else:
            print("Falha ao publicar mensagem")
    except Exception as exception:
        print(f"Erro: {exception}")