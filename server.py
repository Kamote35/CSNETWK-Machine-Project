import socket
import threading
import os
from datetime import datetime

# Initialize the server
HEADER = 64
SERVER_PORT = 5050
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_ADDRESS, SERVER_PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/leave"
DIRECTORY = "/dir"
CONNECT_MESSAGE = (f"/join {SERVER_ADDRESS} {SERVER_PORT}") 

#print(server_address)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#dictionary to store client username
client_alias = {}

#Getting the timestamp
currenttime = datetime.now()
format_time = currenttime.strftime("%Y-%m-%d %I:%M:%S")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    name = False
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: 
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTED] {addr} has disconnected")
            elif msg.startswith("/register"): #user inputs /register
                alias = msg.split(" ")[1]
                if alias in client_alias.values():
                    error_msg = f"Error: The name '{alias}' already exists. Please choose a different name."
                    send_length = str(len(error_msg)).encode(FORMAT)
                    send_length += b' ' * (HEADER - len(send_length))
                    conn.send(send_length)
                    conn.send(error_msg.encode(FORMAT))
                else:
                    name = True
                    client_alias[addr] = alias
                    print(f"[REGISTERED] {addr} registered as {alias}. Welcome, {alias}!")
                    confirmation_message = f"Successfully registered as {alias}."
                    send_length = str(len(confirmation_message)).encode(FORMAT)
                    send_length += b' ' * (HEADER - len(send_length))
                    conn.send(send_length)
                    conn.send(confirmation_message.encode(FORMAT))
            elif msg.startswith("/store"):
                filename = msg.split(" ")[1]
                f = open(filename, "r")
                print(f"[{addr}] {format_time}: Uploaded a file \"{filename}\"")
                print(f"File Content: {f.read()}")
            elif msg.startswith("/get"):
                filename = msg.split(" ")[1]
                if os.path.exists(filename):
                    with open(filename, 'r') as file:
                        file_content = file.read()
                        send_length = str(len(file_content)).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(file_content.encode(FORMAT))
                        print(f"[FILE SENT] {filename} to {addr}")
                else:
                    print(f"File '{filename}' does not exist.")
            elif msg == DIRECTORY:
                files = os.listdir('.')
                files_list = "\n".join(files)
                send_length = str(len(files_list)).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                conn.send(send_length)
                conn.send(files_list.encode(FORMAT))
                print(f"[DIRECTORY LIST] to {addr}")
            else:
                if name:
                    print(f"[{alias}] {msg}")
                else:
                    alias = client_alias.get(addr, "Unknown")
                    print(f"[{addr}] {msg}")

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_ADDRESS}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args =(conn, addr))
        thread.start()
        print(f"[CLIENT APP OPENED] {threading.active_count() - 1}")



print("[STARTING SERVER] Wait for a moment while the server is starting...")
start()


