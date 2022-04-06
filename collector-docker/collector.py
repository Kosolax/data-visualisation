from sys import argv
import socket
from _thread import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from time import sleep, time

# This file can get 4 arguments
# 1 - The server port
# 2 - The writer IP
# 3 - The writer port
# 4 - The size of packets accepted by the server




def multi_threaded_client(connection):


    while True:

        if not connection.recv(int(argv[4])):
            print('NULL')
        else:
            print('NOT NULL')


        with open('/home/private.pem','r') as fk:
            priv = RSA.importKey(fk.read())
            fk.close()
        
        print(len(connection.recv(int(argv[4]))))

        cipher = PKCS1_OAEP.new(priv)
        #data = cipher.decrypt(connection.recv(int(argv[4])))


        print("datas")
        print(cipher)

            # open a connection for the writer
            #writerSocket = socket.socket()
            #host = argv[2]
            #port = int(argv[3])
            #writerSocket.connect((host, port))
        
            # send the data to the write
            #writerSocket.send(data)
            #writerSocket.close()

# init the server socket
serverSocket = socket.socket()
host = ''
port = int(argv[1])
serverSocket.bind((host, port))
serverSocket.listen(5)


while (True):
    client, address = serverSocket.accept()
    start_new_thread(multi_threaded_client, (client, ))

# stop the server, should never happen
serverSocket.close()