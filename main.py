import asyncio
import multiprocessing
import time

import cv2

from config import CAMERA_INDEX, RECOGNITION_DELAY
from database import check_phone_number_in_database, check_license_plate_in_database
from esp import listen_for_phone_numbers, send_command_to_esp
from logger import call_log, car_log
from recognition import recognize_license_plate  # Импорт функции из файла recognition


def process_camera():
    """Асинхронная задача для обработки видеопотока с камеры."""
    last_time = 0
    cap = cv2.VideoCapture(CAMERA_INDEX)  # Используем первую подключенную камеру
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Ошибка: Не удалось получить кадр с камеры")
                continue

            # Распознавание номерного знака
            license_plate = recognize_license_plate(frame)
            if license_plate:
                print(f"Распознан номер: {license_plate}")
                # Проверяем, был ли номер обработан недавно

                current_time = time.time()

                if check_license_plate_in_database(license_plate):
                    if current_time - last_time > RECOGNITION_DELAY:
                        last_time = current_time
                        car_log(license_plate)
                        send_command_to_esp("OPEN")
                    else:
                        print("Такой есть, но сейчас делей")

            # Показ обработанного кадра (опционально)
            cv2.imshow("Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Нажмите Q для выхода
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


def listen_for_phone_number():
    """Асинхронная задача для ожидания номера телефона от ESP."""
    print("Ожидание данных от ESP...")
    while True:
        phone_number = listen_for_phone_numbers() # Добавляем await
        if phone_number:  # Проверяем, есть ли данные
            print(f"Получен телефонный номер: {phone_number}")
            if check_phone_number_in_database(phone_number):
                call_log(phone_number)
                send_command_to_esp("OPEN")



def main():
    # Создаем два процесса
    camera_process = multiprocessing.Process(target=process_camera)
    phone_process = multiprocessing.Process(target=listen_for_phone_number)

    # Запускаем процессы
    camera_process.start()
    phone_process.start()

    # Ожидаем завершения процессов
    camera_process.join()
    phone_process.join()


if __name__ == "__main__":
    main()