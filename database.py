import psycopg2
from psycopg2 import sql

from config import DB_CONFIG
from logger import log_to_database

def check_in_database(identifier, value, log_table, search_column, log_data_columns):
    """
    Проверяет наличие записи в базе данных и логирует событие, если найдено.
    """
    conn = None
    cursor = None
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Проверяем, есть ли значение в базе данных
        query = sql.SQL("SELECT * FROM residents WHERE {column} = %s").format(
            column=sql.Identifier(search_column)
        )
        cursor.execute(query, (value,))
        result = cursor.fetchone()

        if result:
            # Создаем словарь данных для логирования
            log_data = {col: result[idx] for idx, col in enumerate(log_data_columns)}
            log_data['timestamp'] = 'now()'  # Добавляем текущую метку времени

            # Логируем событие
            log_to_database(log_table, log_data)
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def check_license_plate_in_database(license_plate):
    """
    Проверяет наличие номерного знака в базе данных.
    """
    return check_in_database(
        identifier="car_number",
        value=license_plate,
        log_table="car_logs",
        search_column="car_number",
        log_data_columns=["full_name", "apartment_number", "phone_number", "car_brand", "car_number"]
    )

def check_phone_number_in_database(phone_number):
    """
    Проверяет наличие номера телефона в базе данных.
    """
    return check_in_database(
        identifier="phone_number",
        value=phone_number,
        log_table="call_logs",
        search_column="phone_number",
        log_data_columns=["full_name", "apartment_number", "phone_number"]
    )


"""
def check_plate_in_database(license_plate): #ебануть под номер тоже и синг респонс хуйня
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
"""
