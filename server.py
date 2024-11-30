import socket
import threading

# Initialize the server
HEADER = 64
SERVER_PORT = 5050
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_ADDRESS, SERVER_PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/leave"
CONNECT_MESSAGE = (f"/join {SERVER_ADDRESS} {SERVER_PORT}")
# print(server_address)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")


    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: 
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTED] {addr} has disconnected")

        print(f"[{addr}] {msg}")

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_ADDRESS}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args =(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



print("[STARTING SERVER] Wait for a moment while the server is starting...")
start()


