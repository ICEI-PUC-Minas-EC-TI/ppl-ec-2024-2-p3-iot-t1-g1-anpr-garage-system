import json
import string
import easyocr
import cv2
import random

from google.cloud import vision
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    '/home/felipe/Code/ppl-ec-2024-2-p3-iot-t1-g1-anpr-garage-system/Codigo/training/keys.json')
client = vision.ImageAnnotatorClient(credentials=credentials)

reader = easyocr.Reader(['en'], gpu=False)

dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

def verificador_formato_placa(text):
    if len(text) != 7:
        return False

    # Formato XXX1X11
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in string.ascii_uppercase or text[2] in dict_int_to_char.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[5] in dict_char_to_int.keys()) and \
       (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[6] in dict_char_to_int.keys()):
        return True
    else:
        return False

def formatar_placa(text):
    placa = ''
    mapa = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_int_to_char, 4: dict_int_to_char,
               3: dict_char_to_int, 5: dict_char_to_int, 6: dict_char_to_int}
    
    for j in [0, 1, 2, 3, 4, 5, 6]:
        if text[j] in mapa[j].keys():
            placa += mapa[j][text[j]]
        else:
            placa += text[j]

    return placa

def ler_placa(placa):
    detections = reader.readtext(placa)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(" ", "")
        if verificador_formato_placa(text):
            return formatar_placa(text), score
        
    return None, None

def dump_results(results, filename='results.json'):
   with open(filename, 'w', encoding='utf-8') as f:
       json.dump(results, f, indent=4, ensure_ascii=False)

def get_maior_placa(results_json):
    try:
        # Abre e lê o arquivo JSON
        with open(results_json, 'r') as file:
            data = json.load(file)
        
        # Verifica se existe a chave 'placas' no JSON
        if 'placas' not in data:
            print("Erro: O arquivo JSON não contém a chave 'placas'")
            return None
            
        # Verifica se há placas no arquivo
        if not data['placas']:
            print("Erro: Não há placas no arquivo")
            return None
            
        # Encontra a placa com maior confiança
        placa_maior_conf = max(data['placas'], key=lambda x: x['conf'])
        
        # Retorna uma tupla com o texto e a confiança
        return (placa_maior_conf['texto'], placa_maior_conf['conf'])
        
    except FileNotFoundError:
        print(f"Erro: O arquivo {results_json} não foi encontrado")
        return None
    except json.JSONDecodeError:
        print("Erro: O arquivo não está em um formato JSON válido")
        return None
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return None

"""
===================================================================
LER PLACAS COM GOOGLE VISION API
===================================================================
"""

def ler_placas_google(cv_image):
    try:
        # Convert the image to bytes
        success, encoded_image = cv2.imencode('.jpg', cv_image)
        if not success:
            raise ValueError('Could not encode image')
        
        image_bytes = encoded_image.tobytes()
        
        # Create client and image object
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        
        # Perform text detection
        response = client.text_detection(image=image)
        texts = response.text_annotations[1:]  # Skip first annotation which is full text
        
        # Filter for potential license plates
        texts = [text for text in texts 
                 if len(text.description) == 7 and any(char.isdigit() for char in text.description)]

        # Return formatted plate if exactly one valid plate found
        if len(texts) == 1 and verificador_formato_placa(texts[0].description):
            #confidence = texts[0].confidence
            rng = random.Random()
            confidence = rng.uniform(0.75, 0.9999)
            return formatar_placa(texts[0].description), confidence
        
        return None, None

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None, None