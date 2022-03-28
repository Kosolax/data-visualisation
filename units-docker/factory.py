from unit import unit
from sys import argv
from time import sleep, time
import socket

# This file can get 4 arguments
# 1 - The unit number
# 2 - The folder where you want to generate the json
# 3 - The collector ip
# 4 - The collector port

unit = unit(int(argv[1]))

while(True):
    # generate json file
    nameFile = "paramunite" + str(unit.number) + "_" + str(time()) + ".json"
    nameFile = argv[2] + "/" + nameFile
    unit.generate_json_file(nameFile)

    # read the file
    file = open(nameFile, "r")
    data = file.read()

    # send the file to the collector
    clientMultiSocket = socket.socket()
    host = argv[3]
    port = int(argv[4])
    clientMultiSocket.connect((host, port))
    clientMultiSocket.send(data.encode("utf-8"))
    clientMultiSocket.close()
    sleep(60)