import socket
import pickle
import subprocess
import time

#||||||||||||||||||||||||||||||CLIENT||||||||||||||||||||||||||


socket = socket.socket()
serverAddress = 'localhost', 1111


def popenExecution(data):
    command = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return str(command.stdout.read() + command.stderr.read(), "utf-8")

def recv(socket):
    try:
        message = pickle.loads(socket.recv(2048))
        print(message)
    except Exception as e:
        print(e)

def main():
    
    socket.connect(serverAddress)
    #Standard command to identify who this machine is
    socket.send(pickle.dumps(popenExecution("who").split()[0]))
    while True:
        recv(socket)
        time.sleep(1)


main()
