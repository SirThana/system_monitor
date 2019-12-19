import socket
import time
import pickle
import threading
import random
from Crypto.Cipher import AES
import mysql.connector as mysql

#||||||||||||||||||||||||||||||SERVER||||||||||||||||||||||||||

#TODO
#   1.  line 57 should right after accepting a connection, send the keyvalues to
#       the connected client. Client should catch this and use this keypair for futher
#       communication


HVA = '145.109.151.121'
l = 'localhost'
s = socket.socket()
serverAddress = HVA, 1111
s.bind(serverAddress)
s.listen(1)

socketDict = {} # who : conn
commandList = ['uptime', 'uname', 'pwd']
global resultDict
resultDict = {} #Holds who : [results] 
global key
key = []


def encryptAES(message, key):
    obj = AES.new(key[0], AES.MODE_CBC, key[1])
    ciphertext = obj.encrypt(message)
    return ciphertext


def decryptAES(ciphertext, key):
    obj2 = AES.new(key[0], AES.MODE_CBC, key[1])
    message = obj2.decrypt(ciphertext)
    return message


def generateKeys(keySize):
    key = []
    for i in range(0, 2):
        x = ""
        for j in range(keySize):
            x += str(int(random.random() * 10))
        key.append(x)
    return key

#   --> Receives a socket, Accepts connections and appends them to the socketDict
#       x is a dummy value because "Threading"
def connHandler(socket, x):
    while True:
        try:
            conn, addr = socket.accept()
            key = generateKeys(8)
            socketDict.update({pickle.loads(conn.recv(2048)) : [conn, key]})
        except Exception as e:
            print(e)

#   --> Sends commands to every socket in the socketDict
def sendCommands():
    for key in socketDict.keys():
        for command in commandList:
            try:
                socketDict[key][0].send(pickle.dumps(str(command)))
                receive(key)
            except Exception as e:
                print(e)
    print(resultDict)
 
#   --> Receives something from a socket, key is the key in socketDict.
#       socketDict[key][0] is a socket, 1 and 2 are keys
def receive(key):
    resultDict.update({key : []})
    try:
        x = pickle.loads(socketDict[key][0].recv(2048))
        resultDict[key].append(x)
    except Exception as e:
        print(e)
        time.sleep(1)

#   --> try to connect to the database
def connDatabase(resultDict):
    try:
        db = mysql.connect(host="145.109.143.23",
                                    user="tester",
                                    passwd="P@ssword",
                                    database = "TESTMAU"
        )

        if db.is_connected():
            db_version = db.get_server_info()
            print("MySQL Database Connected: " + db_version)
            cursor = db.cursor(buffered=True)
            cursor.execute("INSERT INTO Data (Time) VALUES ('{}')".format(resultDict)) 
            db.commit()

    except Exception as e:
        pass

def main():
    threadedHandler = threading.Thread(target=connHandler, args=(s, 1)) 
    threadedHandler.start()

    startingTime = time.time()
    while True:
        timeDiff = time.time() - startingTime
        #print(socketDict.keys())
        print(socketDict)
        if timeDiff > 5: #Send command every 5 seconds
            sendCommands()
            startingTime = time.time()
        time.sleep(1)

main()
