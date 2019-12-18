import socket
import time
import pickle
import threading

#||||||||||||||||||||||||||||||SERVER||||||||||||||||||||||||||

#TODO
#   1.  Have the server send a command at a fixed time interval and immediately expect the ouput


HVA = '145.109.173.68'
l = 'localhost'
s = socket.socket()
serverAddress = l, 1111
s.bind(serverAddress)
s.listen(1)

socketDict = {} # who : conn
commandList = ['uptime', 'uname']


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
        try:
            socketDict[key].send(pickle.dumps(str(commandList[0])))
            receive()
        except Exception as e:
            print(e)
 
 #  --> Should this start a thread for every socket in socketDict?
 #      what happens when more than one socket sends to this server?
def receive():
    for key in socketDict.keys():
        try:
            x = pickle.loads(socketDict[key].recv(2048))
            print(x)
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
