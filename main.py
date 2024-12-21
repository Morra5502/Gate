import asyncio
import cv2

from database import check_phone_number_in_database, check_license_plate_in_database
from esp import listen_for_phone_numbers
from logger import call_log, car_log
from recognition import recognize_license_plate  # Импорт функции из файла recognition


async def process_camera():
    """Асинхронная задача для обработки видеопотока с камеры."""
    cap = cv2.VideoCapture(0)  # Используем первую подключенную камеру
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Ошибка: Не удалось получить кадр с камеры")
                await asyncio.sleep(0.1)
                continue

            # Распознавание номерного знака
            license_plate = recognize_license_plate(frame)
            if license_plate:
                print(f"Распознан номер: {license_plate}")

            # Если существует
            if check_license_plate_in_database(license_plate):
                car_log(license_plate)

            # Показ обработанного кадра (опционально)
            cv2.imshow("Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Нажмите Q для выхода
                break

            await asyncio.sleep(0.1)  # Исключаем блокировку цикла
    finally:
        cap.release()
        cv2.destroyAllWindows()


async def listen_for_phone_number():
    """Асинхронная задача для ожидания номера телефона от ESP."""
    print("Ожидание данных от ESP...")
    while True:
        phone_number = listen_for_phone_numbers()
        print(f"Получен телефонный номер: {phone_number}")
        if check_phone_number_in_database(phone_number):
            call_log(phone_number)


async def main():
    """Основная асинхронная функция для запуска задач."""
    await asyncio.gather(
        process_camera(),
        #listen_for_phone_number()
    )


if __name__ == "__main__":
    asyncio.run(main())