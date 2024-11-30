import socket

HEADER = 64
SERVER_PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/leave"
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_ADDRESS, SERVER_PORT)
CONNECT_MESSAGE = (f"/join {SERVER_ADDRESS} {SERVER_PORT}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# send(input("Please input a messag/command: "))

print("To connect to server type: /join <server_address> <server_port>")
print("")
client_message = input("Please input a message/command: ")

if client_message == CONNECT_MESSAGE:
    send(client_message)
    print(f"Connected to succesfully to the File Exchange Server {SERVER_ADDRESS}!")

    while client_message != DISCONNECT_MESSAGE:
        client_message = input("Please input a message/command: ")
        send(client_message)

if client_message == DISCONNECT_MESSAGE:
    send(client_message)
    print(f"Disconnected successfully from File Exchange Server: {SERVER_ADDRESS}!")