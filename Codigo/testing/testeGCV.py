from google.cloud import vision
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    '/home/felipe/Code/ppl-ec-2024-2-p3-iot-t1-g1-anpr-garage-system/Codigo/training/keys.json')
client = vision.ImageAnnotatorClient(credentials=credentials)

def detect_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        print(f'{text.confidence}')
    texts = [text for text in texts if len(text.description) == 7 and any(char.isdigit() for char in text.description)]

    print("Texts:")
    for text in texts:
        print(f'"{text.description}" (confidence: {text.confidence:.2f})')

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

path = "./teste/image_20241119_223742.jpg"
detect_text(path)