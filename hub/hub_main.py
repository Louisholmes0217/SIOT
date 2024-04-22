import socket
import threading
import csv

# Grabbing config from settings file.
with open("/opt/SIOT/hub/hub_settings.csv", "r") as f:
    reader = csv.DictReader(f)
    for line in reader:
        PORT = int(line["port"])
        IP = line["ip"]
        HEADER = 64
        FORMAT = "utf-8"
        DISCONNECT_MSG = "!DISCONNECT"

# Creating server socket object.
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((IP, PORT))

# Handles client requests.
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == ("!DISCONNECT"):
                connected = False
            print(f"{addr}, {msg}")
    conn.close()

# Starts server.
def start():
    SERVER.listen()
    print(f"Listening on port {IP}:{PORT}")
    while True:
        conn, addr = SERVER.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS: {threading.active_count() - 1}")

print("Starting server...")
start()