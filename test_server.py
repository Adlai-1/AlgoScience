import socket
import pytest
import configparser

# Define the TCP server host and port
HOST = 'localhost'
PORT = 5050

# create a configparser object.
# open and read the config file.
config = configparser.ConfigParser()
config.read('config.ini')

# Define a test function to test the TCP server
def query_server(info):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect((HOST, PORT))
    
    client_socket.sendall(info.encode())

    # Receive the response from the server
    response = client_socket.recv(1024).decode()
    
    # Print the response
    return response

# Testing smaller components (functions) of our program.

# test function for persisting file path.
def persist_file_path(file_path,file_name):
    """
    This function persists (stores) the file path in
    PersistedFilePath.txt file.
    """
    try:
        with open(file_name,'w',encoding='utf-8') as file:
            file.write(file_path)
            file.close()
            return 'Done'
    except FileNotFoundError:
        return "[Error Message]: Unable to find file. Terminating Server."
    except TypeError:
        return "[Error Message]: Wrong input type. Terminating Server."

# test function for determining if a file path has been changed or not.
def file_path_changed (file_name) -> bool:
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
        return "[Error Message]: Unable to find file. Terminating Server."

# test function for finidng a string value.
def search_in_large_file(file_name, search_value):
    """
    This function searches for the client's value by
    putting the contents of a file in chunks and searches
    through each chunk for the value. It returns true when
    a value is found and False if otherwise.
    """
    try:
        with open(file_name, 'r',encoding='utf-8') as file:
            while True:
                chunk = file.read(1024)  # Read 1024 bytes at a time
                if not chunk:
                    break
                if search_value in chunk:
                    return True
        file.close()
        return False
    except FileNotFoundError:
        return"[Error Message]: Unable to find file. Terminating Server."
    
def test_query():
    """
    Test function for executing searh query.
    """
    assert query_server('1') == 'STRING EXISTS\n'
    assert query_server('a') == 'STRING NOT FOUND\n'
    assert query_server('8') == 'STRING EXISTS\n'
    assert query_server('B') == 'STRING NOT FOUND\n'
    assert query_server('c') == 'STRING NOT FOUND\n'

def test_persist_file_path():
    """
    Test function for executing searh query.
    """
    assert persist_file_path(' ','testFile2.txt') == 'Done'
    assert persist_file_path('./400.txt','testFile2.txt') == 'Done'
    assert persist_file_path(4,'testFile2.txt') == '[Error Message]: Wrong input type. Terminating Server.'

def test_search_in_large_file():
    """
    Test function for executing searh query.
    the file 200k.txt is used as the file with all accepted
    string values.
    """
    assert search_in_large_file('200k.txt','a') == False
    assert search_in_large_file('200k.txt','1') == True
    assert search_in_large_file('200k.txt','v') == False
    assert search_in_large_file('200.txt','4') == "[Error Message]: Unable to find file. Terminating Server."
    assert search_in_large_file('400.html','2') == "[Error Message]: Unable to find file. Terminating Server."

def test_file_path_changed():
    """
    Test function for determining if the file path has been changed.
    the file testFile1.txt is used for this test.
    """
    assert file_path_changed('testFile1.txt') == False
    assert file_path_changed('PersistedFilePath.txt') == True
    assert file_path_changed('test.txt') == "[Error Message]: Unable to find file. Terminating Server."
