import socket
import threading
import json

def handleClient(connectionSocket, addr):
    print(str(addr) + " successful connection")
    request_data = connectionSocket.recv(1024).decode()

    try:
        request_json = json.loads(request_data)

        method = request_json.get("method")

        if method == "Random":
            min_val = request_json.get("Tal1")
            max_val = request_json.get("Tal2")
            import random
            random_num = random.randint(min_val, max_val)
            response = {"status": "success", "result": random_num}
        elif method == "Add":
            num1 = request_json.get("num1")
            num2 = request_json.get("num2")
            result = num1 + num2
            response = {"status": "success", "result": result}
        elif method == "Subtract":
            num1 = request_json.get("num1")
            num2 = request_json.get("num2")
            result = num1 - num2
            response = {"status": "success", "result": result}
        else:
            response = {"status": "error", "message": "Invalid method"}
    except (ValueError, KeyError):
        response = {"status": "error", "message": "Invalid request format"}

    response_data = json.dumps(response)
    connectionSocket.send(response_data.encode())
    connectionSocket.close()

# Opret en socket til serveren
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socketen til en specifik adresse og port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Lyt efter indkommende forbindelser
server_socket.listen(5)
print("Serveren lytter på {}:{}".format(*server_address))

while True:
    # Accepter en indkommende forbindelse
    client_socket, client_address = server_socket.accept()
    print("Forbindelse fra:", client_address)

    # Opret en tråd til at håndtere klienten
    handle_thread = threading.Thread(target=handleClient, args=(client_socket, client_address))
    handle_thread.start()
