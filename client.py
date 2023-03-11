"""
This module contains the necessary codes for our TCP client.
"""
# imports
import socket

# Define the TCP server host and port
HOST = 'localhost'
PORT = 5050

# Open a client socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# The loop keeps the connection between the client
# and the server alive.
try:
    while True:

        info = input("")
        client_socket.sendall(info.encode())

        # Receive the response from the server
        response = client_socket.recv(1024).decode()

        # Print the response
        print(response+"\n")

except KeyboardInterrupt:
    print("[Server Message]: Connection closed.")
except ConnectionRefusedError:
    print("[Server Message]: Unable to connect to Server.")
