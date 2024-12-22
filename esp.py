import socket

import requests
from config import ESP8266_IP, ESP8266_PORT

def send_command_to_esp(command):
    print("Типа отправил")

def listen_for_phone_numbers():
    """
    Асинхронно прослушивает UDP-порт для получения номеров телефонов от ESP.
    Возвращает номер телефона, если данные поступили. Если данных нет, возвращает None.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("0.0.0.0", ESP8266_PORT))
        print("Ожидание подключения ESP на порт", ESP8266_PORT)

        while True:
            try:
                data, addr = udp_socket.recvfrom(1024)
                if data:
                    phone_number = data.decode().strip()
                    print(f"Получен телефонный номер: {phone_number} от {addr}")
                    return phone_number
            except socket.timeout:
                print("ESP не подключен или не отправляет данные. Повтор ожидания...")
                return None
