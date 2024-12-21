import socket

import requests
from config import ESP8266_IP, ESP8266_PORT

def send_command_to_esp(command, esp_url="http://192.168.1.100"):
    """Отправляет команду на ESP."""
    try:
        response = requests.post(f"{esp_url}/command", json={"command": command})
        if response.status_code == 200:
            print(f"Команда {command} успешно отправлена.")
        else:
            print(f"Ошибка при отправке команды {command}: {response.status_code}")
    except Exception as e:
        print(f"Ошибка связи с ESP: {e}")

async def listen_for_phone_numbers():
    """
    Асинхронно прослушивает UDP-порт для получения номеров телефонов от ESP.
    Проверяет, подключен ли ESP, и возвращает номер телефона при поступлении сигнала.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("0.0.0.0", ESP8266_PORT))
        print("Ожидание подключения ESP на порт", ESP8266_PORT)

        while True:
            try:
                udp_socket.settimeout(10)  # Устанавливаем таймаут ожидания 10 секунд
                data, addr = udp_socket.recvfrom(1024)
                if data:
                    phone_number = data.decode().strip()
                    print(f"Получен телефонный номер: {phone_number} от {addr}")
                    return phone_number
            except socket.timeout:
                print("ESP не подключен или не отправляет данные. Повтор ожидания...")