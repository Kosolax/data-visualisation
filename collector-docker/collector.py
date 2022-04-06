from sys import argv
import socket
from _thread import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from time import sleep, time
import json
from unit import unit

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

def multi_threaded_client(connection, address):
    try:
        if dictionaryIpCountError[address] >= 5:
            break

        shouldReadKey = False
        shouldReadJson = False
        while True:
            incomingData = connection.recv(int(argv[7]))
            if not incomingData:
                break

            if (shouldReadJson):
                print("json")
                shouldReadJson = False
                if address in dictionaryIpSyncKey:
                    cipherAES = AES.new(dictionaryIpSyncKey[address])
                    myJson = cipherAES.decrypt(incomingData)
                    insert(myJson.decode("utf-8"))
                    

            if (shouldReadKey):
                print("key")
                shouldReadKey = False
                with open('/home/private.pem','r') as fk:
                    priv = RSA.importKey(fk.read())
                    fk.close()
                cipherRSA = PKCS1_OAEP.new(priv)
                myUnitKey = cipherRSA.decrypt(incomingData)
                dictionaryIpSyncKey[address] = myUnitKey

            if (int.from_bytes(incomingData, 'big') == 1):
                shouldReadKey = True

            if (int.from_bytes(incomingData, 'big') == 2):
                shouldReadJson = True
    except:
        if address in dictionaryIpCountError:
            dictionaryIpCountError[address] = dictionaryIpCountError[address] + 1
        else:
            dictionaryIpCountError[address] = 1


def load_unit(data):
    temp = json.loads(data)
    dictionaryUnit = json.loads(temp)
    return unit(dictionaryUnit["number"], dictionaryUnit["automatons"])

def insert(data):
    # get data inside an object
    unit = load_unit(data)

    connection = db_connection()

    if not connection:
        return

    cursor = connection.cursor()

    # if unit don't exist we insert it in db
    if not do_unit_exist(unit, cursor):
        insert_unit(unit, cursor, connection)

    for i in range(len(unit.automatons)):
        # if automaton don't exist we insert it in db
        if not do_automaton_exist(unit, i, cursor):
            insert_automaton(unit, i, cursor, connection)
            
        # insert production data
        insert_production(unit, i, cursor, connection)
    connection.close()

def get_last_milk_weight(unit, i, cursor, id_automaton):
    sql_select_Query = "select milkWeight from productions where id_automaton = %s and id_unit = %s order by generatedTime desc;"
    record = (id_automaton, unit.number,)
    cursor.execute(sql_select_Query, record)
    records = cursor.fetchall()
    if cursor.rowcount == 0:
        return 0
    
    return records[0][0]

def load_unit(data):
    temp = json.loads(data)
    dictionaryUnit = json.loads(temp)
    return unit(dictionaryUnit["number"], dictionaryUnit["automatons"])

def insert_production(unit, i, cursor, connection):
    id_automaton = get_automaton_id(unit, i, cursor)
    # get the db last row
    lastMilkWeight = get_last_milk_weight(unit, i, cursor, id_automaton)
    mySql_insert_query = """INSERT INTO productions (id_automaton, id_unit, tankTemperature, outsideTemperature, milkWeight, finalizedProductWeight, ph, k, naci, salmonel, ecoli, listeria, generatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
    finalizedProductWeight = unit.automatons[i].milkWeight - lastMilkWeight
    if lastMilkWeight == 0:
        finalizedProductWeight = 0

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

def insert_unit(unit, cursor, connection):
    mySql_insert_query = """INSERT INTO units VALUES (%s); """
    record = (unit.number,)
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