import socket
import threading
import json

# Opret en socket til klienten
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Forbinder til serveren
server_address = ('localhost', 12345)
client_socket.connect(server_address)

try:
    while True:
        # Læs kommando fra terminalen
        method = input("Indtast metode (Random, Add, Subtract): ")

        if method == "exit":
            break

        if method not in ["Random", "Add", "Subtract"]:
            print("Ukendt metode")
            continue

        try:
            # Læs tal1 og tal2 fra brugeren
            tal1 = int(input("Indtast tal1: "))
            tal2 = int(input("Indtast tal2: "))
        except ValueError:
            print("Ugyldigt input. Brug kun heltal.")
            continue

        # Opret JSON request
        request = {
            "method": method,
            "Tal1": tal1 if method == "Random" else None,
            "Tal2": tal2 if method == "Random" else None,
            "num1": tal1 if method in ["Add", "Subtract"] else None,
            "num2": tal2 if method in ["Add", "Subtract"] else None
        }

        # Send JSON request til serveren
        client_socket.send(json.dumps(request).encode())

        # Modtag og udskriv svaret fra serveren
        response_data = client_socket.recv(1024).decode()
        response = json.loads(response_data)

        if response["status"] == "success":
            print("Resultat:", response["result"])
        else:
            print("Fejl:", response["message"])

except KeyboardInterrupt:
    pass
finally:
    # Luk forbindelsen til serveren
    client_socket.close()
