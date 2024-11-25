import cv2
from ultralytics import YOLOv10 as YOLO

# carrega o modelo treinado
model = YOLO('./runs/detect/train1/weights/last.pt')

# inicializa a camera
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Could not open webcam")
    exit()

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Can't receive frame from webcam")
        break

    # roda o modelo em cima do frame atual da camera
    results = model(frame)[0]

    # desenha a caixa
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = result[:6]
        label = f'{model.names[cls]} {conf:.2f}'

        if conf > 0.5:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # mostra os frames
    cv2.imshow('YOLO Detection', frame)

    # 'q' pra breakar o codigo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()