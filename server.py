import socket
import time
import pickle
import threading

#||||||||||||||||||||||||||||||SERVER||||||||||||||||||||||||||


s = socket.socket()
serverAddress = ('127.0.0.1', 1111)
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
    


def main():
    threadedHandler = threading.Thread(target=connHandler, args=(s, 1)) 
    threadedHandler.start()
    while True:
        if len(list(socketDict.keys())) > 0:
            print(list(socketDict.keys())[-1])
        time.sleep(1)

main()
