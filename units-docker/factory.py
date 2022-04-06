from unit import unit
from sys import argv
from time import sleep, time
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import os

# This file can get 4 arguments
# 1 - The unit number
# 2 - The folder where you want to generate the json
# 3 - The collector ip
# 4 - The collector port

unit = unit(int(argv[1]))

dateLastKeyGeneration = ''
keySync = ''

def update_key():
    AES_key_length = 16
    secret_key = os.urandom(AES_key_length)
    keySync= secret_key
    return keySync

def do_i_need_new_key():
    if(dateLastKeyGeneration == '' or dateLastKeyGeneration < (datetime.now() - timedelta(minutes=1)) ):
        return True
    return False

while(True):
    clientMultiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = argv[3]
    port = int(argv[4])
    clientMultiSocket.connect((host, port))

    # generate json file
    nameFile = "paramunite" + str(unit.number) + "_" + str(time()) + ".json"
    nameFile = argv[2] + "/" + nameFile
    unit.generate_json_file(nameFile)

    # read the file
    file = open(nameFile, "r")
    data = file.read()
    
    if do_i_need_new_key():
        dateLastKeyGeneration = datetime.now()
        keySync = update_key()
        cipherAES = AES.new(keySync)
        # send the file to the collector
        with open('/home/public.pem','r') as fp:
            pub = RSA.importKey(fp.read())
            fp.close()
        cipherRSA = PKCS1_OAEP.new(pub)
        encryptedKey = cipherRSA.encrypt(keySync)
        integer_val = 1
        bytes_val = integer_val.to_bytes(2, 'big')
        clientMultiSocket.send(bytes_val)
        sleep(1)
        clientMultiSocket.send(encryptedKey)
        sleep(1)

    while len(data) % 16 !=0:
        data = data + " "
        
    integer_val = 2
    bytes_val = integer_val.to_bytes(2, 'big')
    encryptedJson = cipherAES.encrypt(data)
    clientMultiSocket.send(bytes_val)
    sleep(1)
    clientMultiSocket.send(encryptedJson)
    
    clientMultiSocket.close()
    sleep(10)