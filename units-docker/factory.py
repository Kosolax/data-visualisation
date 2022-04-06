from unit import unit
from sys import argv
from time import sleep, time
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from datetime import datetime, timedelta
import os
import base64

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
    encoded_secret_key = base64.b64encode(secret_key)
    keySync= encoded_secret_key
    return keySync

def do_i_need_new_key():
    if(dateLastKeyGeneration == '' or dateLastKeyGeneration < (datetime.now() - timedelta(hours=1)) ):
        return True
    return False

def send_symetric_key():
    dateLastKeyGeneration = datetime.now()
    keySync = update_key()

    with open('/home/public.pem','r') as fp:
        pub = RSA.importKey(fp.read())
    cipher = PKCS1_OAEP.new(pub)
    clientMultiSocket.connect((host, port))
    encryptedKey = cipher.encrypt(keySync)
    clientMultiSocket.send(encryptedKey)

# Todo
# chiffrer avec la clé symétrique les données
# découper le json en plein de petit bout
# vérifier tpc vs udp
while(True):
    clientMultiSocket = socket.socket()
    if(do_i_need_new_key()):
        send_symetric_key()

    host = argv[3]
    port = int(argv[4])
    
    # generate json file
    #nameFile = "paramunite" + str(unit.number) + "_" + str(time()) + ".json"
    #nameFile = argv[2] + "/" + nameFile
    #unit.generate_json_file(nameFile)

    # read the file
    #file = open(nameFile, "r")
    #data = file.read()

    # send the file to the collector

    #clientMultiSocket.send(data.encode("utf-8"))
    clientMultiSocket.close()
    fp.close()
    sleep(20)