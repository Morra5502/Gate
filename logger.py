import logging
import psycopg2
from psycopg2 import sql

from config import DB_CONFIG


#логгер в консоль
def setup_logger(log_file="app.log"):
    """Настраивает логгер."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

logger = setup_logger()

def log_event(event_message, level="info"):
    """Логирует событие."""
    if level == "info":
        logger.info(event_message)
    elif level == "error":
        logger.error(event_message)
    elif level == "warning":
        logger.warning(event_message)

def log_to_database(table, data):
    """
    Универсальная функция для логирования данных в базу.
    """
    conn = None
    cursor = None
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Динамическое построение SQL-запроса для вставки данных
        columns = data.keys()
        values = tuple(data.values())
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
            table=sql.Identifier(table),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        cursor.execute(query, values)
        conn.commit()
        print(f"Данные успешно добавлены в таблицу {table}.")
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()