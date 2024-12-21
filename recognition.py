import re

import pytesseract
import cv2

# Устанавливаем путь к Tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def open_img(image):
    carplate_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return carplate_img


def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5) #порвероять

    carplate_img = None

    for x, y, w, h in carplate_rects:
        carplate_img = image[y+15:y+h-10, x+15:x+w-20]

    return carplate_img


def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    return resized_image


def main_rec(img_path):
    carplate_img_rgb = img_path
    carplate_haar_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_russian_plate_number.xml')

    carplate_extract_img = carplate_extract(carplate_img_rgb, carplate_haar_cascade)
    if carplate_extract_img is None:
        return None
    cv2.imshow("extract", carplate_extract_img)

    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    cv2.imshow("enlarge", carplate_extract_img)

    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    cv2.imshow("gray", carplate_extract_img_gray)

    text = recognize_text_from_plate(carplate_extract_img_gray)

    return text

def recognize_text_from_plate(plate_image):
    """Распознает текст на изображении номерного знака."""
    raw_text = pytesseract.image_to_string(plate_image,
    config='--psm 8 -l rus tessedit_char_whitelist=АВЕКМНОРСТУХ1234567890')
    filtered_text = re.sub(r'[^А-Я0-9]', '', raw_text)
    return filtered_text

def match_license_plate_format(text):
    """Проверяет текст на соответствие формату номерного знака."""
    matches = re.findall(r'[А-Я][0-9]{3}[А-Я]{2}[0-9]{2}', text.upper())
    return matches[0] if matches else None

