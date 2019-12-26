import socket
import time
import pickle
import threading
import random
import pdb
from Crypto.Cipher import AES
import mysql.connector as mysql
from flask import Flask, jsonify

#||||||||||||||||||||||||||||||SERVER||||||||||||||||||||||||||


#TODO
#   1.  Maybe do something with checksums
#https://stackoverflow.com/questions/26851034/opening-a-ssl-socket-connection-in-python


#Set variables
HVA = '145.109.151.121'
l = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = l, 1111
s.bind(serverAddress)
s.listen(1)
app = Flask(__name__)

socketDict = {} # who : [conn, [key1, key2]]
commandList = ['uname', 'uptime', 'df -h']
global resultDict
resultDict = {} #Holds who : [{COMMAND : RESULT}] 


def startFlask(p, q):
    app.run()


#   --> takes a GET request with a WHO, returns all existing records of that machine
@app.route('/<uname>', methods=['GET'])
def APIGET(uname):
#    while True:
#        for key in resultDict.keys():
#            if str(key) == str(uname):
#                return jsonify(resultDict)
#
#                for command in resultDict[key]:
#                    print(command)
#                    return str(command)
#    return str(resultDict.keys())
    return (jsonify(resultDict[uname]))
    

def encryptAES(message, key, key2):
    obj = AES.new(key, AES.MODE_CFB, key2)
    ciphertext = obj.encrypt(message)
    return ciphertext


def decryptAES(ciphertext, key, key2):
    obj2 = AES.new(key, AES.MODE_CFB, key2)
    message = obj2.decrypt(ciphertext)
    return message


#   --> Generates a list of 2 keys based on a given keySize (Default 16).
#       All ASCII printable symbols
def generateKeys(keySize):
    key = []
    for i in range(0, 2):
        x = ""
        for j in range(keySize):
            x += chr(int(random.randrange(33, 126))) #Character set, check ASCII if you're curious
        key.append(x)
    return key

#   --> Receives a socket, Accepts connections and appends them to the socketDict
#       x is a dummy value because "Threading"
def connHandler(socket, x):
    while True:
        try:
            conn, addr = socket.accept() #accept connection
            key = generateKeys(16) #Generate keypair
            who = pickle.loads(conn.recv(2048))
            socketDict.update({who : [conn, key]}) #store key
            conn.send(pickle.dumps(key)) #send key
            resultDict.update({who : []}) #For every new conn, initialize it with who : []
        except Exception as e:
            print(e)

#   --> Sends commands to every socket in the socketDict
def sendCommands():
    for key in socketDict.keys(): #For each key,
        for command in commandList: #Send a command, try and receive a response, for every command
            try:
                command = encryptAES(command, socketDict[key][1][0], socketDict[key][1][1]) #encrypt
                command = pickle.dumps(command) #Serialize
                socketDict[key][0].send(command) #Send that shit
                receive(key) #We're gonna expect a response, call for a receive with the WHO
            except Exception as e:
                print(e)


#   --> Receives something from a socket, key is the key in socketDict.
#       socketDict[key][0] is a socket, [1][0] and [1][1] are keys
#       x ought to be a dictionairy {COMMAND : RESULT}
def receive(key):

    try:
        x = socketDict[key][0].recv(2048)
        x = decryptAES(x, socketDict[key][1][0], socketDict[key][1][1]) #Decrypt
        x = pickle.loads(x) # {COMMAND : RESULT}
        x = { key.decode(): val.strip('\n') for key, val in x.items() } #Remove garbage b and \n

        #Update existing records with different values for same keys, append non existing record
        for idx, dict in enumerate(resultDict[key]):
            for dictKey in dict.keys():
                if dictKey == list(x.keys())[0]:
                    return(resultDict[key][idx].update(x))
        return(resultDict[key].append(x))

    #Catch network related errors
    except Exception as e:
        print(e)

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
        print(e)


def main():

    #Handle connections in a thread
    threadedHandler = threading.Thread(target=connHandler, args=(s, 1)) 
    threadedHandler.start()

    #Start restful API in a thread
    threadedHandler = threading.Thread(target=startFlask, args=(0, 1)) 
    threadedHandler.start()

    #Keep track of time, to send commands on a set interval
    startingTime = time.time()
    while True:
        timeDiff = time.time() - startingTime
        if timeDiff > 5: #Send command every 5 seconds
            sendCommands()
            startingTime = time.time()
        time.sleep(1)

main()
