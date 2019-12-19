import socket
import time
import pickle
import threading

#||||||||||||||||||||||||||||||SERVER||||||||||||||||||||||||||

#TODO
#   1.  All the output from the clients, sort it out in a dict for later writing to a DB


HVA = '145.109.173.68'
l = 'localhost'
s = socket.socket()
serverAddress = l, 1111
s.bind(serverAddress)
s.listen(1)

socketDict = {} # who : conn
commandList = ['uptime', 'uname', 'pwd']
global resultDict
resultDict = {} #Holds who : [results] 


#   --> Receives a socket, Accepts connections and appends them to the socketDict
#       x is a dummy value because "Threading"
def connHandler(socket, x):
    while True:
        try:
            conn, addr = socket.accept()
            socketDict.update({pickle.loads(conn.recv(2048)) : conn})
        except Exception as e:
            print(e)

#   --> Sends commands to every socket in the socketDict
def sendCommands():
    for key in socketDict.keys():
        for command in commandList:
            try:
                socketDict[key].send(pickle.dumps(str(command)))
                receive()
            except Exception as e:
                print(e)
    print(resultDict)
 
 #  --> Should this start a thread for every socket in socketDict?
 #      what happens when more than one socket sends to this server?
def receive():
    for key in socketDict.keys():
        resultDict.update({key : []})
        try:
            x = pickle.loads(socketDict[key].recv(2048))
            resultDict[key].append(x)
        except Exception as e:
            print(e)
            time.sleep(1)


def main():
    threadedHandler = threading.Thread(target=connHandler, args=(s, 1)) 
    threadedHandler.start()


    startingTime = time.time()
    while True:
        timeDiff = time.time() - startingTime
        print(socketDict.keys())
        if timeDiff > 5: #Send command every 5 seconds
            sendCommands()
            startingTime = time.time()
        time.sleep(1)

main()
