import paho.mqtt.client as mqtt
import requests
import mysql.connector
import sys

#Conexão
con = mysql.connector.connect(
    host='localhost',
    database='Sistema_ANPR',
    user='root',
    password='cronoeston2',
    sql_mode=''
)

# verifique se a conexão ao BD foi realizada com sucesso
if con.is_connected():
    db_info = con.get_server_info()
    print("Conectado com sucesso ao Servidor ", db_info)

    # a partir de agora pode-se executar comandos SQL: para tanto é necessário criar um objeto tipo cursor
    # o cursor permite acesso aos elementos do BD
    cursor = con.cursor()
    cursor.execute("select database();")
    # crio uma variável qualquer para receber o retorno do comando de execução
    linha = cursor.fetchone()
    print(f"Conectado ao DB {linha}")

    # Creat BD
    createTable = """
                -- -----------------------------------------------------
-- Table Sistema_ANPR.Mensalista
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Mensalista (
    
    id_mensalista INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    CPF CHAR(11) NOT NULL,  
    RG VARCHAR(20) NOT NULL,
    status INT NOT NULL,
    CHECK (status IN (0,1)) 
);

-- -----------------------------------------------------
-- Table Sistema_ANPR.Garagem
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Garagem (

    id_garagem INT PRIMARY KEY AUTO_INCREMENT,
    capacidade INT NOT NULL,
    hora_abertura TIME NOT NULL,  
    hora_fechamento TIME NOT NULL,  
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    CEP CHAR(8) NOT NULL,  
    numero INT NOT NULL,
    rua VARCHAR(150) NOT NULL
);

-- -----------------------------------------------------
-- Table Sistema_ANPR.Carro
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Carro (
    id_carro INT PRIMARY KEY AUTO_INCREMENT,
    id_garagem INT NOT NULL,
    id_mensalista INT DEFAULT NULL,
    marca VARCHAR(150) NOT NULL,
    cor VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    placa CHAR(7) NOT NULL,
    ano INT NOT NULL, 
    FOREIGN KEY (id_mensalista) REFERENCES Mensalista(id_mensalista),
    FOREIGN KEY (id_garagem) REFERENCES Garagem(id_garagem)
);

-- -----------------------------------------------------
-- Table Sistema_ANPR.Fluxo
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Fluxo (

    id_fluxo INT NOT NULL AUTO_INCREMENT,
    id_garagem INT NOT NULL,
    id_carro INT NOT NULL,
    entrada DATETIME NOT NULL,
    saida DATETIME NOT NULL,
    PRIMARY KEY (id_fluxo),
    FOREIGN KEY (id_garagem) REFERENCES Garagem(id_garagem),
    FOREIGN KEY (id_carro) REFERENCES Carro(id_carro),
    CHECK (saida > entrada)
);

            """

    # este par try/except verifica se a tabeja  já está criada. Se a tabela não existe, cai no try e é criada
    # se existe, cai no except e só mostra a mensagem que  a tabela existe
    try:
        cursor.execute(createTable)
    except:
        print("Tabela já existe.")
        pass

# esta função é a função callback informando que o cliente se conectou ao servidor
def on_connect(client, userdata, flags, rc):
    print("Connectado com codigo "+str(rc))

    # assim que conecta, assina um tópico. Se a conexão for perdida, assim que
    # que reconectar, as assinaturas serão renovadas
    client.subscribe("topico-carro-detectado")

# esta função é a função callback que é chamada quando uma publicação é recebida do servidor
def on_message(client, userdata, msg):
      # Comando para finalizar conexão, caso a mensagem seja "termina"
    if str(msg.payload.decode().strip()) == "termina":
        print("Recebeu comando termina.")
        if con.is_connected():
            print("Fim da conexão com o Banco")
            client.loop_stop()  # Para o loop do MQTT
            con.close()  # Fechar o cursor
            sys.exit(0)  # Encerra o programa
            
    
    print("Mensagem recebida no tópico: " + msg.topic)
    print("Placa "+ str(msg.payload.decode()) + " detectada")

    flag = 1
    # Inicializando variáveis com valores padrão
    placa = msg.payload.decode().strip()
    marca = "Não encontrado"
    cor = "Não encontrado"
    modelo = "Não encontrado"
    ano = None  # Inicializando como None

    #Conectando com a API de placas para pegar as informações, tais como modelo, ano e etc
    placa = msg.payload.decode().strip()
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
        """
            # Exibe as informações
            print(f"Marca: {marca}")
            print(f"Cor: {cor}")
            print(f"Modelo: {modelo}")
            print(f"Ano: {ano}")
        """
    except requests.exceptions.RequestException as e:
        #print(f"Erro na requisição: {e}")
        print("Placa inválida ou não disponível no sistema, tente novamente.")
        flag = 0
    except ValueError:
        print("Erro ao processar a resposta JSON.")
        flag = 0
    if flag == 1:
        #Inserção no BD
        cursor = con.cursor()
        insert_query = """
        INSERT INTO Carro (id_garagem, id_mensalista, marca, cor, modelo, placa, ano) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    # Se ano for não encontrado atribuir None
        if ano == "Não encontrado" or ano is None:
            ano = None

        # Certificando a conexão
        if not con.is_connected():
            con.reconnect()

        print((1, None, marca, cor, modelo, placa, ano))

        try:
            # Executa o comando de inserção
            cursor.execute(insert_query, (1, None, marca, cor, modelo, placa, int(ano)))
            #print(cursor.mogrify(insert_query, dados))
            con.commit()
            print("Registro inserido com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir dados: {err}")

        # Certificando de que a conexão está ativa
        if not con.is_connected():
            con.reconnect()

        # Consultando a tabela Carro para verificar os registros
        cursor.execute("SELECT * FROM Carro")
        myresult = cursor.fetchall()
        print(myresult)

        # Comando para apagar registros, caso a mensagem seja "delete"
        if str(msg.payload.decode().strip()) == "delete":
            cursor.execute("TRUNCATE TABLE Carro")
            print("Tabela Carro foi truncada.")

        # Certificando de que a conexão está ativa
        if not con.is_connected():
            con.reconnect()


if __name__ == '__main__':
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)
    #client.connect("broker.hivemq.com", 1883, 60) # broker alternativo

    # a função abaixo manipula trafego de rede, trata callbacks e manipula reconexões.
    client.loop_forever()