"""
This module contains the necessary codes for our TCP server.
"""
# imports.
import socket
import threading
import datetime
import time
import configparser

# declare vaialbles for host address and port number.
PORT = 5050
HOST = 'localhost'

# create socket object.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding socket to a specific address and port.
server_socket.bind((HOST, PORT))

# create a configparser object.
# open and read the config file.
config = configparser.ConfigParser()
config.read('config.ini')

def search_in_large_file(file, search_value):
    """
    This function searches for the client's value by
    putting the contents of a file in chunks and searches
    through each chunk for the value. It returns True when
    the value is found and False if otherwise.
    """
    while True:
        chunk = file.read(1024)  # Read 1024 bytes at a time
        if not chunk:
            break
        if search_value in chunk:
            for data in chunk.split(';'):
                if data == search_value:
                    return True
        return False

def client_handler(client_socket, client_address,file_path):
    """
    This function handles requests from clients whenever a
    connection is established.
    """
    # The while loop makes it possible for the client to make multiple queries
    # with the same connection.
    try:
        search_file = open(file_path,"r",encoding="utf-8")
        while True:
            # get the start time for our search query.
            start_time = time.time()

            # recieve string value not more than 1024 bytes.
            data = client_socket.recv(1024)

            # decode byte data recieved into string.
            data = data.decode()

            # removing any x\00 characters from the end of the string.
            data = data.rstrip('\x00')

            new_file_path = config.get("path","linuxpath")

            # check to see if filepath in the config file has changed.
            if file_path == new_file_path:
                reread_on_query = False
            else:
                reread_on_query = True

            if reread_on_query:
                with open(new_file_path,"r",encoding="utf-8") as file:
                    if search_in_large_file(file,data):
                        client_socket.sendall(b"STRING EXISTS")
                    else:
                        client_socket.sendall(b"STRING NOT FOUND")
                    search_file = file # reassign search_file with the current filepath.
            else:
                if search_in_large_file(search_file,data):
                    client_socket.sendall(b"STRING EXISTS")
                else:
                    client_socket.sendall(b"STRING NOT FOUND")

            # get the finish time for our search query.
            finish_time = time.time()

            # get the time taken to execute the search query.
            execution_time = finish_time - start_time

            # rounding up our finishTime to 2 decimal place.
            execution_time = round(execution_time, 2)

            # get the timestamp after executing query.
            time_stamp = datetime.datetime.now()

            print(
                f"DEBUG:\n"
                f"[IP Address]: {client_address[0]},"
                f"[Search Query]: {data},\n"
                f"[Execution Time]: {execution_time}ms,"
                f"[Timestamp]: {time_stamp}\n"
                )

    except ConnectionAbortedError:
        print("[Server Message]: Connection terminated.")
    except ValueError:
        print("[Error Message]: Client entered the wrong value")
    except ConnectionError:
        print("[Error Message]: Connection terminated")

def run_server():
    """
    This function starts our TCP Server.
    """
    server_socket.listen()
    print("[Server Status]...Server is running!")

    file_path = config.get("path","linuxpath") # checks for the filepath in the config file

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=client_handler,args=(client_socket,client_address,
        file_path))
        client_thread.start()

        print(f"Connection established with {client_address[0]}")

run_server()
