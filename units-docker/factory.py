from unit import unit
from sys import argv
from time import sleep
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import os
import time
import struct
from operator import xor
from bitstring import BitArray
from random import randint, uniform

# This file can get 4 arguments
# 1 - The unit number
# 2 - The folder where you want to generate the json
# 3 - The collector ip
# 4 - The collector port
# 5 - The mask

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

clientMultiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = argv[3]
port = int(argv[4])
clientMultiSocket.connect((host, port))
with open('/home/public.pem','r') as fp:
    pub = RSA.importKey(fp.read())
    fp.close()
cipherRSA = PKCS1_OAEP.new(pub)
bitsMask = BitArray(float=round(uniform(1, 999), 2), length=64)
encryptedMask = cipherRSA.encrypt(bytes(bitsMask))

integer_val = 4
bytes_val = integer_val.to_bytes(2, 'big')
clientMultiSocket.send(bytes_val)
sleep(1)
clientMultiSocket.send(encryptedMask)
clientMultiSocket.close()
sleep(1)

while(True):
    clientMultiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = argv[3]
    port = int(argv[4])
    clientMultiSocket.connect((host, port))

    generatedTime = float(time.time())
    
    # generate json file
    nameFile = "paramunite" + str(int(argv[1])) + "_" + str(generatedTime) + ".json"
    nameFile = argv[2] + "/" + nameFile

    epoch = float(nameFile.split("_")[1].split(".json")[0])
    bitsEpoch = BitArray(float=epoch, length=64)
    results = []
    for i, bit in enumerate(bitsEpoch):
        results.append(xor(bit,bitsMask[i]))
    myNewUnit = unit(int(argv[1]), results)
    myNewUnit.generate_json_file(nameFile)

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

    integer_val = 3
    bytes_val = integer_val.to_bytes(2, 'big')
    while len(nameFile) % 16 !=0:
        nameFile = nameFile + " "

    encryptedJson = cipherAES.encrypt(nameFile)
    clientMultiSocket.send(bytes_val)
    sleep(1)
    clientMultiSocket.send(encryptedJson)
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