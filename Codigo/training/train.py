import os
from ultralytics import YOLOv10

config_path = './config.yaml'

model = YOLOv10.from_pretrained("jameslahm/yolov10n")

model.train(data=config_path, epochs=200, batch=32)