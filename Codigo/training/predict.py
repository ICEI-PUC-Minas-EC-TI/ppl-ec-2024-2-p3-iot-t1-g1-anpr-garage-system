import cv2
import time
import os
from picamera2 import Picamera2
from ultralytics import YOLOv10 as YOLO
from util import dump_results, get_maior_placa, ler_placas_google

import sys
sys.path.append('../')  # Only need to go up one level since you're in 'training'
from espRaspberryConnection import car_detection

os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Carrega o modelo treinado
model = YOLO('./runs/detect/train1/weights/last.pt')

results = {}

# Inicializa a camera
picam2 = Picamera2()
capture_config = picam2.create_still_configuration(main={"size": (1640, 1232)})
picam2.configure(capture_config)
picam2.start()

while True:
    frame = picam2.capture_array()

    # Roda o modelo em cima do frame atual da camera
    detections = model(frame)[0]

    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = detection[:6]
        label = f'{model.names[cls]} {conf:.2f}'

        # Corta a placa
        placa_cortada = frame[int(y1):int(y2), int(x1):int(x2), :]

        # Processamento da imagem da placa
        placa_cinza = cv2.cvtColor(placa_cortada, cv2.COLOR_BGR2GRAY)
        placa_cinza_hist = cv2.equalizeHist(placa_cinza)
        _, placa_thresh = cv2.threshold(placa_cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Mostrar as placas cortadas
        # cv2.imshow('original', placa_cortada)
        # cv2.imshow('cinza', placa_cinza)
        # cv2.imshow('hist', placa_cinza_hist)
        # cv2.imshow('thresh', placa_thresh)

        # Lê os caracteres da placa
        texto_placa, conf_texto_placa = ler_placas_google(placa_thresh)

        # Inicializa a lista de placas se ela nn existir
        """
        ===================================================
        Implementar estratégia para otimização de leitura de placas de diferentes carros
        ===================================================
        """
        if "placas" not in results:
            results["placas"] = []
            start_time = time.perf_counter()


        # Concatena as placas na lista
        if texto_placa is not None:
            
            results["placas"].append({
                "texto": texto_placa,
                "conf": conf_texto_placa
            })

        if time.perf_counter() - start_time > 5:
            dump_results(results)
            maior_conf = get_maior_placa('results.json')
            if maior_conf:
                texto, confianca = maior_conf
                print(f"Placa: {texto}, Confiança: {confianca}")
                car_detection(texto)


            picam2.stop()
            cv2.destroyAllWindows()
            exit()

        # Desenha a caixa
        if conf > 0.5:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # mostra os frames
    cv2.imshow('YOLO Detection', frame)

    # 'q' pra breakar o codigo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()