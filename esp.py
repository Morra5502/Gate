import requests

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

"""
# Конфигурация ESP
# ESP8266_IP = "192.168.0.18"  # Укажите IP ESP8266
#ESP8266_PORT = 8080  # Укажите порт ESP8266


def send_command_to_esp(command):
    #Отправка команды на ESP через сокет.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as esp_socket:
            esp_socket.connect((ESP8266_IP, ESP8266_PORT))
            esp_socket.sendall(f"{command}\n".encode())
            print(f"Команда отправлена на ESP: {command}")
    except Exception as e:
        print(f"Ошибка при отправке команды на ESP: {e}")

async def listen_for_phone_numbers():
    #Асинхронно прослушиваем UDP для получения номеров телефонов от ESP.
    global AUTHORIZED_PHONE_NUMBERS
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("0.0.0.0", ESP8266_PORT))
        print("Ожидание номеров телефонов от ESP...")

        while True:
            data, addr = udp_socket.recvfrom(1024)
            phone_number = data.decode().strip()
            if phone_number:
                if phone_number not in AUTHORIZED_PHONE_NUMBERS:
                    AUTHORIZED_PHONE_NUMBERS.append(phone_number)
                    print(f"Новый номер телефона добавлен: {phone_number}")
                    # Если номер телефона разрешен, отправляем команду на ESP
                    send_command_to_esp("BLINK_LED")
"""