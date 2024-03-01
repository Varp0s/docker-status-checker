import socket
import json

def receive_container_status(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = s.recv(1024)
            if not data:
                break
            container_statuses = json.loads(data.decode())
            print("The Status of the Received Container:")
            print(container_statuses)

if __name__ == "__main__":
    SERVER_HOST = "127.0.0.1"   # change the host address
    SERVER_PORT = 12345  # change the port number
    receive_container_status(SERVER_HOST, SERVER_PORT)
