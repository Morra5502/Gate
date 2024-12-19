import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

def check_plate_in_database(license_plate):
    conn = None
    cursor = None
    #Проверяет наличие номерного знака в базе данных и логирует событие.
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Проверяем, есть ли номер в базе данных
        query = "SELECT full_name, apartment_number, phone_number, car_brand FROM residents WHERE car_number = %s"
        cursor.execute(query, (license_plate,))
        result = cursor.fetchone()

        if result: #по кайфу будет вынести в отдельную функцию а то сингл респонсабилити хуйня + работает пока только с номерами
            # Если номер найден, логируем событие в car_logs
            full_name, apartment_number, phone_number, car_brand = result
            log_query = "INSERT INTO car_logs (full_name, apartment_number, car_number, phone_number, car_brand) VALUES (%s, %s, %s, %s, %s) "
            cursor.execute(log_query, (full_name, apartment_number, license_plate, phone_number, car_brand))
            conn.commit()
            return True

        return False
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

