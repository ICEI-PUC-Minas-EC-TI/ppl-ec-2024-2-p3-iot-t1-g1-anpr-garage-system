# Sistema de Gerenciamento de Garagem

## Estrutura do Projeto
```Codigio/```
- ```training/``` - Códigos relacionados ao treinamento do moedlo de detecção de objetos(YOLOv10)
- ```esp32-garage-controler/``` - Implementação do controle da maquete
- ```testing/``` - Scripts utilizados para testar diferentes partes do código ao longo do projeto

## Requisitos
- Python 3.8+
- OpenCV
- [YOLOv10](https://github.com/THU-MIG/yolov10)
- Bibliotecas SQL
- Bibliotecas MQTT
- Bibliotecas Raspberry Pi
- Chave das APIs utilizadas

## Configuração
1. Se o diretório Codigo/training/yolov10 não existir ou estiver vazio, clone o repositório lá.
2. Instale as dependências: ```pip install -r requirements.txt```
3. Configure as variáveis de ambiente no ```.env```
4. Execute ```python predict.py```

## Uso

### Pré-requisitos para a execução
- Raspberry Pi com câmera conectada na porta 0
- MySQL Workbench instalado e configurado
- Chave da API Cloud Vision Google
- Ambiente da API Cloud Vision configurado

### Execução
1. Execute o código principal:
```bash
python predict.py
```

O sistema irá:

- Capturar a imagem da placa
- Enviar sinais MQTT para controle da maquete
- Armazenar informações do veículo no banco de dados