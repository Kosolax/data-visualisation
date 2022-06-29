from sys import argv
import socket
from _thread import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from time import sleep, time
import json
from unit import unit
import mysql.connector as mysql
import struct
from operator import xor
from bitstring import BitArray
import time

# This file can get 4 arguments
# 1 - The server port
# 2 - The database IP
# 3 - The database port
# 4 - The database name
# 5 - The database user
# 6 - The database password
# 7 - The size of packets accepted by the server

dictionaryIpSyncKey = {}
dictionaryIpCountError = {}
dictionaryIpNameFile = {}
dictionaryIpMask = {}

def write_log(text_to_append):
    print(text_to_append)
    with open("/home/log.txt","a+") as file:
        file.seek(0)
        data = file.read(100)
        if len(data) > 0:
            file.write("\n")
        file.write(str(time.time()) + ":" + text_to_append)

def multi_threaded_client(connection, address):
    # try:
    if address in dictionaryIpCountError and dictionaryIpCountError[address] >= 5:
        print("Banned")
        write_log("The user is trying to connect even if he's banned.")
        return

    shouldReadKey = False
    shouldReadJson = False
    shouldReadNameFile = False
    shouldReadMask = False
    while True:
        incomingData = connection.recv(int(argv[7]))
        if not incomingData:
            break

        if (shouldReadJson):
            shouldReadJson = False
            write_log("reading json file")
            if address in dictionaryIpSyncKey and address in dictionaryIpMask and address in dictionaryIpNameFile:
                cipherAES = AES.new(dictionaryIpSyncKey[address])
                myJson = cipherAES.decrypt(incomingData)
                unit = load_unit(myJson.decode("utf-8"))
                
                write_log("calculating proof of work")
                # Essaye de calculer la preuve de travail à partir du nom du json
                epoch = float(dictionaryIpNameFile[address].split("_")[1].split(".json")[0])
                bitsEpoch = BitArray(float=epoch, length=64)
                bitsMask = bytearray(dictionaryIpMask[address])
                results = []
                for i, bit in enumerate(bitsEpoch):
                    results.append(xor(bit,bitsMask[i]))
                
                write_log("comparing proof of work")
                # Comparaison entre les deux preuves de travails
                shouldWeAllowToInsert = True
                for i, byte in enumerate(unit.generatedTime):
                    if (byte != results[i]):
                        shouldWeAllowToInsert = False
                        write_log("the proof of work doesn't match")
                        if address in dictionaryIpCountError:
                            dictionaryIpCountError[address] = dictionaryIpCountError[address] + 1
                        else:
                            dictionaryIpCountError[address] = 1

                if shouldWeAllowToInsert:
                    write_log("the proof of work match")
                    insert(unit, epoch)
                    connection.close()
                    exit()

        if (shouldReadKey):
            shouldReadKey = False
            write_log("reading asynchrone key")
            with open('/home/private.pem','r') as fk:
                priv = RSA.importKey(fk.read())
                fk.close()
            cipherRSA = PKCS1_OAEP.new(priv)
            myUnitKey = cipherRSA.decrypt(incomingData)
            dictionaryIpSyncKey[address] = myUnitKey

        if (shouldReadNameFile):
            shouldReadNameFile = False
            write_log("reading name file")
            if address in dictionaryIpSyncKey:
                cipherAES = AES.new(dictionaryIpSyncKey[address])
                nameFile = cipherAES.decrypt(incomingData)
                dictionaryIpNameFile[address] = nameFile.decode("utf-8")

        if (shouldReadMask):
            shouldReadMask = False
            write_log("reading mask")
            with open('/home/private.pem','r') as fk:
                priv = RSA.importKey(fk.read())
                fk.close()
            cipherRSA = PKCS1_OAEP.new(priv)
            mask = cipherRSA.decrypt(incomingData)
            dictionaryIpMask[address] = mask

        if (int.from_bytes(incomingData, 'big') == 1):
            shouldReadKey = True

        if (int.from_bytes(incomingData, 'big') == 2):
            shouldReadJson = True

        if (int.from_bytes(incomingData, 'big') == 3):
            shouldReadNameFile = True

        if (int.from_bytes(incomingData, 'big') == 4):
            shouldReadMask = True
    # except:
    #     if address in dictionaryIpCountError:
    #         dictionaryIpCountError[address] = dictionaryIpCountError[address] + 1
    #     else:
    #         dictionaryIpCountError[address] = 1


def load_unit(data):
    temp = json.loads(data)
    dictionaryUnit = json.loads(temp)
    return unit(dictionaryUnit["number"], dictionaryUnit["generatedTime"], dictionaryUnit["automatons"])

def insert(unit, epoch):
    # get data inside an object

    connection = db_connection()

    if not connection:
        return

    cursor = connection.cursor()

    # if unit don't exist we insert it in db
    if not do_unit_exist(unit, cursor):
        write_log("insert a new unit")
        insert_unit(unit, cursor, connection, epoch)

    for i in range(len(unit.automatons)):
        # if automaton don't exist we insert it in db
        if not do_automaton_exist(unit, i, cursor):
            write_log("insert a new automaton")
            insert_automaton(unit, i, cursor, connection)
            
        if (not do_production_exist(unit, i, cursor)):
            write_log("We have a duplicate data, we don't insert it in db.")
            continue

        # insert production data
        write_log("insert a new entry of data")
        insert_production(unit, i, cursor, connection)
    connection.close()

def do_production_exist(unit, i, cursor):
    id_automaton = get_automaton_id(unit, i, cursor)
    sql_select_Query = "select * from productions where id_automaton = %s and id_unit = %s and generatedTime = %s;"
    record = (id_automaton, unit.number, unit.automatons[i].generatedTime)
    cursor.execute(sql_select_Query, record)
    records = cursor.fetchall()
    if cursor.rowcount == 0:
        return True
    
    return False

def get_last_milk_weight(unit, i, cursor, id_automaton):
    sql_select_Query = "select milkWeight from productions where id_automaton = %s and id_unit = %s order by generatedTime desc;"
    record = (id_automaton, unit.number,)
    cursor.execute(sql_select_Query, record)
    records = cursor.fetchall()
    if cursor.rowcount == 0:
        return 0
    
    return records[0][0]

def insert_production(unit, i, cursor, connection):
    id_automaton = get_automaton_id(unit, i, cursor)
    # get the db last row
    lastMilkWeight = get_last_milk_weight(unit, i, cursor, id_automaton)
    mySql_insert_query = """INSERT INTO productions (id_automaton, id_unit, tankTemperature, outsideTemperature, milkWeight, finalizedProductWeight, ph, k, naci, salmonel, ecoli, listeria, generatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
    finalizedProductWeight = unit.automatons[i].milkWeight - lastMilkWeight
    if lastMilkWeight == 0:
        finalizedProductWeight = 0

    if (not (unit.automatons[i].tankTemperature >= 2.5 and unit.automatons[i].tankTemperature <= 4)):
        write_log("The tank temperature should be between 2.5 and 4. That's why we reject the JSON")
        return

    if (not (unit.automatons[i].outsideTemperature >= 8 and unit.automatons[i].outsideTemperature <= 14)):
        write_log("The outside temperature should be between 8 and 14. That's why we reject the JSON")
        return

    if (not (unit.automatons[i].milkWeight >= 3512 and unit.automatons[i].milkWeight <= 4607)):
        write_log("The weight of the milk should be between 3512 and 4607. That's why we reject the JSON")
        return

    if (not(unit.automatons[i].ph >= 6.8 and unit.automatons[i].ph <= 7.2)):
        write_log("The ph should be between 6.8 and 7.2. That's why we reject the JSON")
        return

    if (not(unit.automatons[i].k >= 35 and unit.automatons[i].k <= 47)):
        write_log("The k should be between 35 and 47. That's why we reject the JSON")
        return

    if (not(unit.automatons[i].naci >= 1 and unit.automatons[i].naci <= 1.7)):
        write_log("The naci should be between 1 and 1.7. That's why we reject the JSON")
        return

    if (not(unit.automatons[i].salmonel >= 17 and unit.automatons[i].salmonel <= 37)):
        write_log("The salmonel should be between 17 and 37. That's why we reject the JSON")
        return

    if (not(unit.automatons[i].ecoli >= 35 and unit.automatons[i].ecoli <= 49)):
        write_log("The ecoli should be between 35 and 49. That's why we reject the JSON")
        return

    if (not(unit.automatons[i].listeria >= 28 and unit.automatons[i].listeria <= 54)):
        write_log("The listeria should be between 28 and 54. That's why we reject the JSON")
        return

    record = (id_automaton, unit.number, unit.automatons[i].tankTemperature, unit.automatons[i].outsideTemperature, unit.automatons[i].milkWeight, finalizedProductWeight, unit.automatons[i].ph, unit.automatons[i].k, unit.automatons[i].naci, unit.automatons[i].salmonel, unit.automatons[i].ecoli, unit.automatons[i].listeria, unit.automatons[i].generatedTime,)
    cursor.execute(mySql_insert_query, record)
    connection.commit()

def get_automaton_id(unit, i, cursor):
    sql_select_Query = "select id from automatons where number = %s and id_unit = %s;"
    record = (unit.automatons[i].number, unit.number,)
    cursor.execute(sql_select_Query, record)
    records = cursor.fetchall()
    if cursor.rowcount == 0:
        return 0
    
    return records[0][0]

def insert_automaton(unit, i, cursor, connection):
    mySql_insert_query = """INSERT INTO automatons (id_unit, number, type) VALUES (%s, %s, %s); """
    record = (unit.number, unit.automatons[i].number, unit.automatons[i].type,)
    cursor.execute(mySql_insert_query, record)
    connection.commit()

def do_automaton_exist(unit, i, cursor):
    sql_select_Query = "select * from automatons where number = %s and id_unit = %s;"
    record = (unit.automatons[i].number, unit.number,)
    cursor.execute(sql_select_Query, record)
    records = cursor.fetchall()
    if cursor.rowcount == 0:
        return False
    
    return True

def do_unit_exist(unit, cursor):
    sql_select_Query = "select * from units where number = %s;"
    record = (unit.number,)
    cursor.execute(sql_select_Query, record)
    records = cursor.fetchall()
    if cursor.rowcount == 0:
        return False
    
    return True

def insert_unit(unit, cursor, connection, epoch):
    mySql_insert_query = """INSERT INTO units VALUES (%s, %s); """
    record = (unit.number, epoch)
    cursor.execute(mySql_insert_query, record)
    connection.commit()

def db_connection():
    return mysql.connect(user=argv[5], password=argv[6], host=argv[2], port=argv[3], database=argv[4])

# init the server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = int(argv[1])
serverSocket.bind((host, port))
serverSocket.listen(5)
while (True):
    client, address = serverSocket.accept()
    start_new_thread(multi_threaded_client, (client, address[0]))

# stop the server, should never happen
serverSocket.close()