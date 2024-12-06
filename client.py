import socket
import os

HEADER = 64
SERVER_PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/leave"
REQUEST_COMMAND = "/?"
DIRECTORY = "/dir"
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_ADDRESS, SERVER_PORT)
CONNECT_MESSAGE = (f"/join {SERVER_ADDRESS} {SERVER_PORT}")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def inputsyntax():
    print("\nHere are the following input commands:")
    print("(1) Connect to server type: /join <server_address> <server_port>")
    print("(2) Leave server: /leave")
    print("(3) Register Username/Handle: /register <name>")
    print("(4) Send file to server: /store <filename>")
    print("(5) Request directory file list: /dir")
    print("(6) Fetch a file from a server: /get <filename>")
    print("(7) Request command help: /?")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def send_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            file_content = file.read()
            send(f"/store {filename}")
            send(file_content)
            print(f"File '{filename}' sent to the server.")
    else:
        print(f"File '{filename}' does not exist.")

def fetch_file(filename):
    send(f"/get {filename}")
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    file_content = client.recv(msg_length).decode(FORMAT)
    with open(filename, 'w') as file:
        file.write(file_content)
    print(f"File '{filename}' fetched from the server.")

def directory_list():
    send("/dir")
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    files_list = client.recv(msg_length).decode(FORMAT)
    print("Directory Listing:")
    print(files_list)

# send(input("Please input a message/command: "))

def main():
    print("Welcome to the client section! To start, join the server first by inputting the following command: ")
    print("(1) Connect to server type: /join <server_address> <server_port>")

    connect = False

    while not connect:
        client_message = input("Please input a message/command: ")

        if client_message == CONNECT_MESSAGE:
            try:
                client.connect(ADDR)
                send(client_message)
                print(f"Connected to succesfully to the File Exchange Server {SERVER_ADDRESS}!")
                connect = True
            except Exception as e:
                print(f"Error connecting to the IP: {e}")
        elif client_message == DISCONNECT_MESSAGE:
            print("You are not connected. Please connect to the server first.")
        else:
            print(f"Error: Connection to the Server has failed! Please check IP Address and Port Number.")
                
        
    while True:
        client_message = input("Please input a message/command: ")
        if client_message == REQUEST_COMMAND:
            inputsyntax()
        elif client_message.startswith("/store"):
            filename = client_message.split(" ")[1]
            send_file(filename)
        elif client_message.startswith("/get"):
            filename = client_message.split(" ")[1]
            fetch_file(filename)
        elif client_message == DIRECTORY: # /dir
            directory_list()
        elif client_message.startswith("/register"):
            send(client_message)
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                response = client.recv(msg_length).decode(FORMAT)
                print(response)
                continue
        elif client_message == DISCONNECT_MESSAGE:
            send(client_message)
            print(f"Disconnected successfully from File Exchange Server: {SERVER_ADDRESS}!")
        else:
            send(client_message)

    

main()
