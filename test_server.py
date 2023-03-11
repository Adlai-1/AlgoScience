"""
This module contains all the tests written to ensure that the program
codes in server.py work correctly without breaking.
"""
# imports
import socket
import configparser
import pytest

# create a configparser object.
config = configparser.ConfigParser()
config.read('config.ini')  # opens and reads content in the config file.

# defining variables
HOST = 'localhost'
PORT = 5000


@pytest.fixture(scope='module')
def tcp_server():
    """
    This function contains codes responsible for setting up
    and running our TCP Server during testing.
    """
    # Set up the TCP server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    yield server_socket

    server_socket.close()


def search_in_large_file(file_name, search_value):
    """
    This function groups the contents of a file into chunks
    and searches through their values to find a string value.
    When the value is found, it returns True;
    otherwise, it returns False.
    """

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            while True:
                chunk = file.read(1024)  # Read 1024 bytes at a time
                if not chunk:
                    break
                if search_value in chunk:
                    for data in chunk.split(';'):
                        if data == search_value:
                            return True

        file.close()
        return False
    except FileNotFoundError:
        return "[Error Message]: Unable to find file."


def test_tcp_server(tcp_server):
    """
    Test function for starting and running our TCP Server.
    """
    # Set up the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Send a message from the client to the server
    message = b'[Server Status]...Server is running!'
    client_socket.sendall(message)

    # Receive the message from the server
    conn, addr = tcp_server.accept()
    received_message = conn.recv(1024)

    # Assert that the message was received correctly
    assert received_message == message

    # Close the connections
    client_socket.close()
    conn.close()


def test_search_in_large_file():
    """
    Test function for executing a search query.
    The file 200k.txt is used as the file with all accepted
    string values.
    """
    error_message = "[Error Message]: Unable to find file."
    assert search_in_large_file('200k.txt', 'a') is False
    assert search_in_large_file('200k.txt', '1') is True
    assert search_in_large_file('200k.txt', 'v') is False
    assert search_in_large_file('200.txt', '4') == error_message
    assert search_in_large_file('400.html', '2') == error_message
