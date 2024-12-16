
# Materiais

Os materiais utilizados no projeto foram:
- Raspberry Pi 5
- Modulo Camera Raspberry Pi 5 8MP
- Chapa de papel paraná
- Palito de picolé (cancela)
- Sensores Infravermelho
- Leds RGB
- Esp32
- Mini Motor DC 3-6V
- protoboard
- Resistores

# Desenvolvimento

O sistema de gerenciamento de garagens ANPR foi desenvolvido utilizando uma arquitetura modular e distribuída, permitindo a integração eficiente entre os componentes de hardware e software. A solução implementada combina tecnologias de visão computacional para reconhecimento de placas veiculares com um sistema de controle de acesso automatizado. O sistema foi desenvolvido em Python devido à sua extensa biblioteca de visão computacional (OpenCV), integração nativa com frameworks de aprendizado de máquina e amplo suporte para desenvolvimento IoT em dispositivos como Raspberry Pi

## Desenvolvimento do Aplicativo

### Interface

A dashborad foi deseenvolvido utilizando o aplicativo MQTT Panel.

## Desenvolvimento do Hardware

### Montagem

Construímos a maquete utilizando papel paraná, palito de picolé, cola quente e tinta amarela. Posicionamos os sensores infravermelhos em cada vaga para que fossem detectados os carros que estacionassem e os LEDs foram colocados em cima das vagas para identificar se aquela vaga estava disponível ou não. O micro servo foi fixado na entrada da garagem para simular uma catraca, abrindo e fechando conforme um carro fosse detectado.

### Desenvolvimento do Código
O dataset utilizado para treinar o modelo YOLOv10 foi construído a partir de aproximadamente 300 imagens coletadas de repositórios públicos como Roboflow e Open Images Dataset, focando especificamente em placas veiculares nos padrões brasileiro antigo e Mercosul. O processo de preparação do dataset incluiu a remoção de imagens duplicadas e renomeação sistemática dos arquivos. A anotação das imagens foi realizada na plataforma CVAT utilizando Bounding Boxes para delimitar as placas, com posterior exportação no formato YOLO compatível com a biblioteca Ultralytics, sendo o conjunto de dados dividido em 80\% para treinamento e 20\% para validação.

Para o reconhecimento óptico de caracteres (OCR) das placas veiculares, foi implementada a Google Cloud Vision API. Antes do processamento pela API, as imagens das placas detectadas passam por um pipeline de pré-processamento que inclui o recorte da região da placa, conversão para escala de cinza (greyscale), equalização de histograma para aumento de contraste e aplicação de threshold inverso, otimizando assim a precisão do reconhecimento de caracteres.

O microcontrolador ESP-32 foi implementado para controlar uma maquete que simula o ambiente real de um estacionamento. O dispositivo gerencia o sistema de catracas e monitora o status das vagas disponíveis, recebendo comandos via protocolo MQTT para controle remoto das funcionalidades e enviando mensagens para atualizar o Painel de Controle.

## Comunicação entre App e Hardware

O protocolo MQTT atua como backbone da comunicação entre os componentes do sistema, estabelecendo três principais fluxos de dados: a conexão entre Raspberry Pi e banco de dados para atualização de registros, a comunicação entre Raspberry Pi e ESP32 para controle automatizado da catraca, e a interface com o MQTT Panel para monitoramento remoto do sistema.