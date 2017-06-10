#!/usr/bin/env python3
from socket import *
import time
import sys
import os
import select
class cli:

    initPort = 5001
    mapPort1 = 5002
    mapPort2 = 5003
    reducerPort = 5004
    prmPort = 5005

    incomingTCP = dict()
    outgoingTCP = dict()

    def __init__(self):
       #needs to be able to determine how many sockets there will be
       #needs to keep track of prm sockets
       self.socket_to_map = None
       self.socket_to_reduce = None
       self.prmSock = None 
       self.mapSock = None
       self.reducerSock = None
       self.mapsockets = []
        #since we have multiple mappers, and i want it to be dynamic i'm trying this
       print("CLI init'd")



    def setup(self):

        #setting up connections
        server = socket(AF_INET)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", int (initPort)))
        server.listen(10)
        print("cli receiving connection from prm")
        connection = server.accept()
        #address = server.accept()
        incomingTCP["prm"] = connection
        print("cli received connection from prm")

        
  
    def prmConnect(self):
        self.ip = "127.0.0.1"
        prmSock = socket(AF_INET, SOCK_STREAM)
        addr = (self.ip, int(prmPort))
        time.sleep(5)
        print("cli connecting to prm")
        prmSock.connect(addr)
        outgoingTCP["prm"] = prmSock
        print("cli connected to prm")


    def getSize(self, file):
        #this helper gets you the file size
        size = os.stat(file)
        return size.st_size


    def mapFile(self, file):
        #I realized that the mapper function needed a helper to find offset, and params
        #UPDATE: I realized that its a better a helper for the whole cmd
        fileSize = self.getSize(file)
        #integer division 
        if(fileSize%2 == 0):
            offset = fileSize//2
        else:
            offset = fileSize - (offset = fileSize//2)
        file = open(file)
        while(True):
            c = file.read(1)
            if c == " ":
                break
            offset += 1
        msg1 = file + " " + "0" + " " + str(offset) + "*"
        msg2 = file + " " + str(offset) + " " + str(file_size//2) + "*"
        mapSock1.sendall(msg1.encode())
        mapSock2.sendall(msg2.encode())
        receive(incomingTCP)

    def fileTranslation(file):
        result = ""
        with open(file) as f:
            for line in f.readlines()
            current = line.split()
            result += current[0] + " " + current[1] + " "
        return result



    def mapperConnect(self, id, port):
        #connect to mapper
        (mapSock+id) = socket(AF_INET, SOCK_STREAM)
        addr = (self.ip, int(port))
        print("connecting to mapper " + id)
        (mapSock+id).connect(addr)
        outgoingTCP["mapper" + id] = mapSock

        #receive connection from mapper
        print("cli receiving connection from mapper1")
        connect = server.accept()
        #addr = server.accept()
        incomingTCP["mapper" + id] = connect
        print("cli has connect with mapper" + id )

    def reducerConnect(self, port):
        reducerSock = socket(AF_INET, SOCK_STREAM)
        addr = (self.ip, int(port))
        print("connecting to reducer")
        reducerSock.connect(addr)
        outgoingTCP["reducer"] = reducerSock
        print("cli connected to reducer")

        #receive connection from reducer
        print("cli receiving connection from reducer")
        connection = server.accept()
        addr = server.accept()
        incomingTCP["reducer"] = connection
        print("cli has received connection from reducer")

    def receive(self, channels):
        received = False
        while(received != True):
            for c in channels.keys():
                sock = channels.get(c)
                ready = select.select([sock], [], [], 1)
                if(ready[0]):
                    data = sock.recv(1024).decode()
                    print(data)
                    received = True
        return



    def commands(self):
    #we need to implement the replicate, stop, resume, total, print merge 
        cont = True
        while cont:
            cmd = raw_input("Enter Command: ")
            print(cmd)
            input_string = cmd.split()
            print(input_string)
                    
                    #set up blank message
                    # msg = ''
                    #character "*" used as delimiter for future message processing
           
            if(input_string[0] == "map"):
                if(len(input_string) != 4):
                    print("Invalid number of args, need 3 args")
                    continue
                file = input_string[1]
                self.mapFile(file)
            
            elif(input_string[0] == "reduce"):
                if(len(input_string) < 2):
                    print("Invalid number of args, need more than 2 inputs")
                    continue
                files = "reduce"
                for i in range(1, len(input_string)):
                    files += input_string[i] + " "
                files += "*"
                reducerSock.sendall(files.encode())
                receive(incomingTCP)
            
            elif input_string[0] == 'print':
                    if(len(input_string) != 1):
                        print("Print")
                        continue
                    prmSock.sendall("print*".encode())
                    receive(incomingTCP)
            
            elif input_string[0] == 'stop':
                if(len(input_string) != 1):
                    print("stop")
                    continue
                prmSock.sendall("stop*".encode())
                receive(incomingTCP)
            
            elif input_string[0] == 'resume':
                if(len(input_string) != 1):
                    print("resume")
                    continue
                prmSock.sendall("resume*".encode())
                receive(incomingTCP)
            
            elif input_string[0] == 'merge':
                #if correct num of args
                if len(input_string) == 3:
                    f1 = input_string[1]
                    f2 = input_string[2]
                    data = "merge" + f1 + " " + f2 + "*"
                    prmSock.sendall(data.encode())
                else:
                    print("Invalid number of args, need 3 args.")
            
            elif input_string[0] == 'total':
                #if improper number of args
                if len(input_string) < 2:
                    print("Invalid number of args, need 3 args.")
                    continue
                else:
                    data = "total"
                    for i in range(1, len(input_string)):
                        data += input_string[i] + " "
                    data += "*"
                    prmSock.sendall(data.encode())
                    receive(incomingTCP)  
           
            elif input_string[0] == 'replicate':
                #if correct num of args
                if len(input_string) == 2:
                    f = input_string[1] #filename
                    data = "replicate" + input_string[1] + "*"
                    prmSock.sendall(data.encode())
                    receive(incomingTCP)
                else:
                    print("Invalid number of args, need 2 args.")

            elif input_string[0] == 'exit':
                cont = False
            
            else:
                print("no matching command found.")
                print("Valid commands: print, stop, resume, merge, total, replicate")
                continue
                               
            if input_string != '':
                continue

test = cli()
test.prmConnect()
test.mapperConnect(self, 1, mapPort1)
test.mapperConnect(self, 2, mapPort2)
test.reducerConnect(self, reducerPort)
test.setup()
test.commands()
print("done")
