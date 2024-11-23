import socket

def main():
    # Define the server address and port
    server_address = 'localhost'
    server_port = 12345

    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the socket to the server's address and port
        client_socket.connect((server_address, server_port))
        print(f"Connected to server at {server_address}:{server_port}")

        # Send data to the server
        message = "Hello, Server!"
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent: {message}")

        # Receive data from the server
        data = client_socket.recv(1024)
        print(f"Received: {data.decode('utf-8')}")

    finally:
        # Close the socket
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    main()