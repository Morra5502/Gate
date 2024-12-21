import psycopg2
from psycopg2 import sql

from config import DB_CONFIG
from logger import car_log, call_log


def check_in_database(column, value):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Динамический запрос к базе данных
        query = sql.SQL("SELECT full_name, apartment_number, phone_number, car_brand FROM residents WHERE {column} = %s").format(
            column=sql.Identifier(column)
        )
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def check_license_plate_in_database(license_plate):
    result = check_in_database("car_number", license_plate)
    if result:
        return True
    return False

def check_phone_number_in_database(phone_number):
    result = check_in_database("phone_number", phone_number)
    if result:
        call_log(phone_number)
        return True
    return False