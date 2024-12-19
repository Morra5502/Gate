import cv2
import pytesseract
import re
import numpy as np

# Устанавливаем путь к Tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def enhance_image(image):
    """Улучшает изображение с номерным знаком."""
    gray = convert_to_grayscale(image)
    enhanced = apply_clahe(gray)
    blurred = apply_gaussian_blur(enhanced)
    return blurred

def convert_to_grayscale(image):
    """Преобразует изображение в градации серого."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_clahe(image):
    """Усиливает контраст изображения с помощью CLAHE."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)

def apply_gaussian_blur(image):
    """Применяет размытие Гаусса для уменьшения шумов."""
    return cv2.GaussianBlur(image, (5, 5), 0)

def crop_to_roi(image):
    """Ограничивает обработку до заданной области интереса."""
    height, width = image.shape[:2]
    roi = image[height // 2:, :]
    return roi

def process_plate_image(plate_image):
    """Дополнительная обработка изображения номерного знака."""
    binary = binarize_image(plate_image)
    inverted = invert_image(binary)
    return inverted

def binarize_image(image):
    """Бинаризует изображение с использованием порогового значения."""
    _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary

def invert_image(image):
    """Инверсирует цвета изображения."""
    return cv2.bitwise_not(image)

def find_contours(image):
    """Находит контуры на изображении."""
    edged = cv2.Canny(image, 30, 200)
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def filter_contours(contours):
    """Фильтрует контуры по заданным критериям."""
    filtered_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 2.0 <= aspect_ratio <= 5.0 and cv2.contourArea(contour) > 1000:
            filtered_contours.append(contour)
    return filtered_contours

def extract_license_plate(roi, contour):
    """Извлекает область с номерным знаком."""
    x, y, w, h = cv2.boundingRect(contour)
    return roi[y:y + h, x:x + w]

def recognize_text_from_plate(plate_image):
    """Распознает текст на изображении номерного знака."""
    processed = process_plate_image(plate_image)
    raw_text = pytesseract.image_to_string(processed, config='--psm 8 -l rus')
    filtered_text = re.sub(r'[^А-Я0-9]', '', raw_text)
    return filtered_text

def match_license_plate_format(text):
    """Проверяет текст на соответствие формату номерного знака."""
    matches = re.findall(r'[А-Я][0-9]{3}[А-Я]{2}[0-9]{2}', text.upper())
    return matches[0] if matches else None

def recognize_license_plate(image):
    """Распознает номерной знак на изображении."""
    enhanced = enhance_image(image)
    roi = crop_to_roi(enhanced)
    contours = find_contours(roi)
    filtered_contours = filter_contours(contours)

    for contour in filtered_contours:
        license_plate = extract_license_plate(roi, contour)
        text = recognize_text_from_plate(license_plate)
        matched_plate = match_license_plate_format(text)
        if matched_plate:
            return matched_plate

    return None
