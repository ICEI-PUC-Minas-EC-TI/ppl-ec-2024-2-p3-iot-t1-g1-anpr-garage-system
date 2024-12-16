# Introdução

O reconhecimento automático de placas veiculares (ANPR - Automatic Number Plate Recognition) tem revolucionado o controle de acesso e segurança em ambientes urbanos. Com o avanço da visão computacional e Internet das Coisas (IoT), a automatização destes sistemas tornou-se mais acessível e eficiente. Neste contexto, este trabalho propõe um sistema integrado de gerenciamento de garagens que combina reconhecimento de placas veiculares com automação IoT. 

O sistema utiliza técnicas de reconhecimento de imagens para identificar as placas dos veículos e integra dispositivos de automação para gerenciar o controle de acesso e a ocupação das vagas. O projeto enfrenta desafios como a precisão de modelos de detecção "on edge" (processamento local no dispositivo, como o Raspberry Pi), e a comunicação entre dispositivos IoT com o protocolo MQTT.

![alt text](https://github.com/ICEI-PUC-Minas-EC-TI/ppl-ec-2024-2-p3-iot-t1-g1-anpr-garage-system/blob/main/Apresentacao/Fotos/fluxograma.png)
*Fluxograma representando o processo completo.*

## Problema

O projeto propõe a demonstrar a viabilidade de um sistema automatizado de gerenciamento de garagens, combinando ANPR e IoT. O objetivo é validar a possibilidade de integrar reconhecimento de placas em dispositivos de baixo custo como Raspberry Pi com sensores e atuadores IoT, servindo como base para futuras implementações em escala comercial.

## Objetivo Geral
Desenvolver um Sistema de Gerenciamento de Garagem automatizado, implemetando tecnologias de ANPR utilizando Raspberry Pi e modelos de computação visual para extrair os caracteres da placa. Integrando também dispositivos físicos (sensores e atuadores) em conjunto com softwares, para melhorar a eficiência e a segurança no controle de estacionamentos.

## Objetivos Específicos
### Implementar o reconhecimento de placas:
 * Aplicar modelos de detecção de objetos para identificar placas em imagens capturadas.
 * Integrar tecnologia de OCR (Reconhecimento Ótico de Caracteres) para a extração eficiente do texto das placas.

### Aplicar conceitos de IoT:
 * Utilizar sensores de proximidade (infravermelho) e LEDs para controlar a ocupação da garagem.
 * Receber as informações dos sensores através do protocolo MQTT.

### Utilizar uma API de placas de trânsito:
 * Enviar os dados das placas, capturados via MQTT, para uma API que retorne informações detalhadas do veículo, como cor, modelo, ano, etc.
 * Integrar as informações retornadas pela API ao banco de dados.

### Analisar a eficiência do ANPR no gerenciamento de estacionamentos:
 * Avaliar a relevância do reconhecimento automático de placas no controle de fluxo.
 * Identificar problemas ou melhorias necessárias em processos de automação de estacionamentos.