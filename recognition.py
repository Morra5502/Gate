import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def recognize_license_plate(image):
    """Распознает номерной знак с помощью Tesseract."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Преобразуем изображение в градации серого
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Убираем шум
    edged = cv2.Canny(blurred, 30, 60)  # Выделяем контуры

    # Находим контуры и фильтруем их по соотношению сторон и площади
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 2.0 <= aspect_ratio <= 9.0 and cv2.contourArea(contour) > 500:  # Соотношение сторон и минимальная площадь
            filtered_contours.append(contour) #test

    filtered_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)[:10]

    license_plate = None
    for contour in filtered_contours:
        # Ищем прямоугольник
        approx = cv2.approxPolyDP(contour, 0.018 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            license_plate = gray[y:y + h, x:x + w]
            break

    if license_plate is not None:
        # Дополнительная обработка контрастности для букв
        license_plate = cv2.resize(license_plate, (0, 0), fx=2, fy=2)  # Увеличиваем масштаб
        license_plate = cv2.equalizeHist(license_plate)  # Выравнивание гистограммы
        _, license_plate = cv2.threshold(license_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        cv2.imshow("Thresholded License Plate", license_plate)  # Показываем после пороговой обработки
        cv2.waitKey(1)

        # Добавлено: поддержка русского языка
        raw_text = pytesseract.image_to_string(license_plate, config='--psm 8 -l rus tessedit_char_whitelist=АВЕКМНОРСТУХ1234567890') #УМОМ

        filtered_text = re.sub(r'[^А-Я0-9]', '', raw_text.upper())  # Оставляем только буквы и цифры
        return filtered_text.strip()
    return None