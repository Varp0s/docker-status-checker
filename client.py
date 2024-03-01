import docker
import time
import socket
import json
from docker.errors import APIError

def get_container_status(container):
    return {
        'id': container.id,
        'name': container.name,
        'status': container.status
    }

def send_container_status(conn, containers):
    container_statuses = [get_container_status(container) for container in containers]
    data = json.dumps(container_statuses).encode()
    conn.sendall(data)

def listen_to_containers(host, port):
    try:
        client = docker.from_env()
    except APIError as e:
        print("Communication error with Docker daemon:", e)
        return
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("The server is resting...")
        conn, addr = s.accept()
        with conn:
            print("The connection is accepted:", addr)
            containers = client.containers.list(all=True)
            previous_statuses = [get_container_status(container) for container in containers]
            while True:
                time.sleep(10)
                containers = client.containers.list(all=True)
                current_statuses = [get_container_status(container) for container in containers]
                if current_statuses != previous_statuses:
                    send_container_status(conn, containers)
                    previous_statuses = current_statuses

if __name__ == "__main__":
    SERVER_HOST = "127.0.0.1"  # change the host address
    SERVER_PORT = 1453  # change the port number
    listen_to_containers(SERVER_HOST, SERVER_PORT)
