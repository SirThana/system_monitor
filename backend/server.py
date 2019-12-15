import socket
import time
import pickle
import threading
import pdb

#||||||||||||||||||||||||||||||SERVER||||||||||||||||||||||||||


s = socket.socket()
serverAddress = ('localhost', 1111)
s.bind(serverAddress)
s.listen(1)

socketDict = {} # HOSTNAME : conn


#   --> Receives a socket, Accepts connections and appends them to the socketDict
def connHandler(socket, x):
    while True:
        try:
            conn, addr = socket.accept()
            socketDict.update({pickle.loads(conn.recv(2048)) : conn})
        except Exception as e:
            print(e)

def sendCommands():
    for key in socketDict.keys():
        try:
            x = "test message to : " , key
            socketDict[key].send(pickle.dumps(str(x)))
        except:
            pass
    


def main():
    threadedHandler = threading.Thread(target=connHandler, args=(s, 1)) 
    threadedHandler.start()
    #pdb.set_trace()
    while True:
        print(socketDict.keys())
        sendCommands()
        time.sleep(1)

main()
