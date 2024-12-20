import asyncio
import cv2
from camera import get_camera_frame, display_frame
from recognition import recognize_license_plate
from database import check_license_plate_in_database, check_phone_number_in_database
from esp import send_command_to_esp
from logger import log_event
from config import CAMERA_INDEX, RECOGNITION_DELAY

async def main():

    last_recognition_time = 0

    print("Система запущена. Нажмите 'q' для выхода.")

    cap = cv2.VideoCapture(CAMERA_INDEX)

    while True:
        try:
            frame = get_camera_frame(cap)
            license_plate = recognize_license_plate(frame)

            if license_plate and (asyncio.get_event_loop().time() - last_recognition_time > RECOGNITION_DELAY):
                log_event(f"Распознанный номер: {license_plate}")
                if check_license_plate_in_database(license_plate):
                    log_event(f"Номер {license_plate} найден в базе. Открываем шлагбаум.")
                    send_command_to_esp("OPEN_GATE")
                    last_recognition_time = asyncio.get_event_loop().time()
                else:
                    log_event(f"Номер {license_plate} не найден в базе.", level="warning")

            if not display_frame(frame):
                break

        except Exception as e:
            log_event(f"Ошибка: {e}", level="error")
    cap.release()

if __name__ == "__main__":
    asyncio.run(main())