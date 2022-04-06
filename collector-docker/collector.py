from sys import argv
import socket
from _thread import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# This file can get 4 arguments
# 1 - The server port
# 2 - The writer IP
# 3 - The writer port
# 4 - The size of packets accepted by the server

def multi_threaded_client(connection):
    while True:

        if not connection.recv(int(argv[4])):
            print("BREAK")
            break

        with open('/home/private.pem','r') as fk:
            priv = RSA.importKey(fk.read())
            print('clef privee')
            print(priv)

            cipher = PKCS1_OAEP.new(priv)
            data = cipher.decrypt(connection.recv(int(argv[4]))).decode("utf-8")
            fk.close()

        print("chifrement")
        print(connection.recv(int(argv[4])))
        print("KEYY")
        print(priv)
        print("DATAAAAAA")
        print(data)

        # open a connection for the writer
        writerSocket = socket.socket()
        host = argv[2]
        port = int(argv[3])
        writerSocket.connect((host, port))
        
        # send the data to the write
        writerSocket.send(data.encode("utf-8"))
        writerSocket.close()
        

            
    connection.close()

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