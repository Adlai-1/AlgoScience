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

# variable to hold file path to the persisted file
# storing the file path to the file storing all
# accepted string values.
PersistedFile = config.get('path','persistedFilePath')

def persist_file_path(file_path,file_name):
    """
    This function persists (stores) the file path in
    PersistedFilePath.txt file.
    """
    try:
        with open(file_name,'w',encoding='utf-8') as file:
            file.write(file_path)
            file.close()
    except FileNotFoundError:
        print("[Error Message]: Unable to find file. Terminating Server.")
    except TypeError:
        print("[Error Message]: Wrong input type. Terminating Server.")

def file_path_changed (file_name):
    """
    This function checks to see if the file path in our config
    file has been changed and returns True as well as stores
    the new path in our PersistedFilePath.txt file.
    """
    try:
        with open(file_name,'r',encoding='utf-8') as persisted_file:
            persisted_file_path = persisted_file.readline()

            file_path = config.get('path','linuxpath')

            persisted_file.close()

            return file_path == persisted_file_path

    except FileNotFoundError:
        print("[Error Message]: Unable to find file. Terminating Server.")

def search_in_large_file(file_name, search_value):
    """
    This function searches for the client's value by
    putting the contents of a file in chunks and searches
    through each chunk for the value. It returns true when
    a value is found and False if otherwise.
    """
    try:
        with open(file_name, "r",encoding='utf-8') as file:
            while True:
                chunk = file.read(1024)  # Read 1024 bytes at a time
                if not chunk:
                    break
                if search_value in chunk:
                    return True
        file.close()
        return False
    except FileNotFoundError:
        print("[Error Message]: Unable to find file. Terminating Server.")

def client_handler(client_socket, client_address, file_name):
    """
    This function handles individual client requests.
    """
    # The while loop makes it possible for the client to make multiple queries
    # with the same connection.
    try:
        file = config.get('path','linuxpath')
        while True:
            # get the start time for our search query.
            start_time = time.time()

            # recieve string value not more than 1024 bytes.
            data = client_socket.recv(1024)

            # decode byte data recieved into string.
            data = data.decode()

            # removing any x\00 characters from the end of the string.
            data = data.rstrip('\x00')

            #intializing flag with value returned from filePathChanged function
            reread_on_query = file_path_changed(file_name)

            if reread_on_query:
                file_path = config.get('path','linuxpath') # get the new filepath.
                persist_file_path(file_path,file_name) # persist the new filepath.

            if search_in_large_file(file, data):
                client_socket.send(b"STRING EXISTS\n")
            else:
                client_socket.send(b"STRING NOT FOUND\n")

            # get the finish time for our search query.
            finish_time = time.time()

            # get the time taken to execute the search query.
            execution_time = finish_time - start_time

            # rounding up our finishTime to 2 decimal place.
            execution_time = round(execution_time, 2)

            # get the timestamp after executing query.
            time_stamp = datetime.datetime.now()

            print(f"DEBUG:\n [IP Address]: {client_address[0]} [Search Query]: {data}\n\
            [Execution Time]: {execution_time}ms, [Timestamp]: {time_stamp}")

    except ConnectionAbortedError:
        print("[Server Message]: Connection closed.")
    except ValueError:
        print("[Error Message]: Entered the wrong value")
    except ConnectionError:
        print("[Error Message]: Connection was terminated")

def run_server():
    """
    We call this function anytime we need to startup our server scripts.
    """
    server_socket.listen()
    print("[Server Status]...Server is running!")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=client_handler,args=(client_socket,client_address,
        PersistedFile))
        client_thread.start()

        print(f"Connection established with {client_address[0]}")

run_server()
