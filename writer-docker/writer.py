import mysql.connector as mysql
from sys import argv
import socket
from _thread import *
from unit import unit
import json

from types import SimpleNamespace

# This file can get 5 arguments
# 1 - The server port
# 2 - The database IP
# 3 - The database port
# 4 - The database name
# 5 - The database user
# 6 - The database password
# 7 - The size of packets accepted by the server

def multi_threaded_client(connection):
    while True:
        # get the client data
        data = connection.recv(int(argv[7])).decode("utf-8")
        
        # insert data into the db
        # insert(data)
        
        if not data:
            break
            
    connection.close()

def insert(data):
    # get data inside an object
    myunit = json.loads(data)
    myunit2 = json.loads(myunit)
    # myunit3 = unit(myunit2)
    print(myunit2["number"])
    
def do_unit_exit():
    connection = db_connection()
    cursor = connection.cursor()

def db_connection():
    return mysql.connect(user=argv[5], password=argv[6], host=argv[2], port=argv[3], database=argv[4])

# init the server socket
serverSocket = socket.socket()
host = ''
port = int(argv[1])
serverSocket.bind((host, port))
serverSocket.listen(5)

while True:
    # accept the client connection
	client, address = serverSocket.accept()

    # start a new thread to treat all the data without blocking new client connection
	start_new_thread(multi_threaded_client, (client, ))

# stop the server, should never happen
serverSocket.close()