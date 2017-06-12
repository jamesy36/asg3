#!/usr/bin/env python3
from socket import *
import time
import sys
import os
import select
import fileinput

initPort = 5001
mapPort1 = 5002
mapPort2 = 5003
reducerPort = 5004
prmPort = 5005
incomingTCP = dict()
outgoingTCP = dict()

class cli:

    #initPort = 5001
    #mapPort1 = 5002
    #mapPort2 = 5003
    #reducerPort = 5004
    #prmPort = 5005

    #incomingTCP = dict()
    #outgoingTCP = dict()

    def __init__(self):
       #needs to be able to determine how many sockets there will be
       #needs to keep track of prm sockets
       self.socket_to_map = None
       self.socket_to_reduce = None
       self.prmSock = socket(AF_INET, SOCK_STREAM)
       self.mapSock1 = socket(AF_INET, SOCK_STREAM) 
       self.mapSock2 = socket(AF_INET, SOCK_STREAM)
       self.reducerSock = socket(AF_INET, SOCK_STREAM) 
       self.mapsockets = []
       self.server = socket(AF_INET, SOCK_STREAM)
       self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
       self.server.bind(("0.0.0.0", int (initPort)))
       self.server.listen(10)
        #since we have multiple mappers, and i want it to be dynamic i'm trying this
       print("CLI init'd")



    #def setup(self):

        #setting up connections
        #server = socket(AF_INET)
        #server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #server.bind(("0.0.0.0", int (initPort)))
        #server.listen(10)
        
        
  
    def prmConnect(self, port):
        self.ip = "0.0.0.0"
        addr = (self.ip, int(port))
        time.sleep(5)
        print("cli connecting to prm")
        self.prmSock.connect(addr)
        outgoingTCP["prm"] = self.prmSock
        print("cli connected to prm")
        print("cli receiving connection from prm")
        connection, address = self.server.accept()
        #address = server.accept()
        incomingTCP["prm"] = connection
        print("cli received connection from prm")


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
            offset = fileSize - fileSize//2
        f = open(file)
        while(True):
            c = f.read(1)
            if c == " ":
                break
            offset += 1
        msg1 = f + " " + "0" + " " + str(offset) + "*" #issue here can't add f and str
        msg2 = f + " " + str(offset) + " " + str(file_size//2) + "*"
        try:
            self.mapSock1.sendall(msg1.encode())
        except socket.error:
            time.sleep(5)
        try:
            self.mapSock2.sendall(msg2.encode())
        except socket.error:
            time.sleep(5)
        receive(incomingTCP)

    def fileTranslation(file):
        result = ""
        with open(file) as f:
            for line in f.readlines():
                current = line.split()
                result += current[0] + " " + current[1] + " "
        return result



    def mapperConnect(self, ID, port):
        #connect to mapper
        #s = socket(AF_INET, SOCK_STREAM)
        addr = (self.ip, int(port))
        print("connecting to mapper " + str(ID))
        if ID == 1:
            self.mapSock1.connect(addr)
        elif ID == 2:
            self.mapSock2.connect(addr)
        outgoingTCP["mapper" + str(ID)] = s 

        #receive connection from mapper
        print("cli receiving connection from mapper " + str(ID))
        connect, addr = self.server.accept()
        #addr = server.accept()
        incomingTCP["mapper" + str(ID)] = connect
        print("cli has connect with mapper" + str(ID) )

    def reducerConnect(self, port):
        self.reducerSock = socket(AF_INET, SOCK_STREAM)
        addr = (self.ip, int(port))
        print("connecting to reducer")
        self.reducerSock.connect(addr)
        outgoingTCP["reducer"] = self.reducerSock
        print("cli connected to reducer")

        #receive connection from reducer
        print("cli receiving connection from reducer")
        connection, addr = self.server.accept()
        #addr = self.server.accept()
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
                print("CLI: map")
                if(len(input_string) != 2):
                    print("Invalid number of args, need 2 args")
                    continue
                file = input_string[1]
                self.mapFile(file)
            
            elif(input_string[0] == "reduce"):
                print("CLI: reduce")
                if(len(input_string) < 2):
                    print("Invalid number of args, need more than 2 inputs")
                    continue
                files = "reduce"
                for i in range(1, len(input_string)):
                    files += input_string[i] + " "
                files += "*"
                try:
                    self.reducerSock.sendall(files.encode())
                except socket.error:
                    time.sleep(5)
                self.receive(incomingTCP)
            
            elif input_string[0] == 'print':
                print("CLI: print")
                if(len(input_string) != 1):
                    print("Print")
                    continue
                try:
                    self.prmSock.sendall("print*".encode())
                except socket.error:
                    time.sleep(5)
                self.receive(incomingTCP)
            
            elif input_string[0] == 'stop':
                print("CLI: stop")
                if(len(input_string) != 1):
                    print("stop")
                    continue
                try:
                    self.prmSock.sendall("stop*".encode())
                except socket.error:
                    time.sleep(5)
                self.receive(incomingTCP)
            
            elif input_string[0] == 'resume':
                print("CLI: resume")
                if(len(input_string) != 1):
                    print("resume")
                    continue
                try:
                    self.prmSock.sendall("resume*".encode())
                except socket.error:
                        time.sleep(5)
                self.receive(incomingTCP)
            
            elif input_string[0] == 'merge':
                print("CLI: merge")
                #if correct num of args
                if len(input_string) == 3:
                    f1 = input_string[1]
                    f2 = input_string[2]
                    data = "merge" + f1 + " " + f2 + "*"
                    try:
                        self.prmSock.sendall(data.encode())
                    except socket.error:
                        time.sleep(5)
                else:
                    print("Invalid number of args, need 3 args.")
            
            elif input_string[0] == 'total':
                print("CLI: total")
                #if improper number of args
                if len(input_string) < 2:
                    print("Invalid number of args, need 3 args.")
                    continue
                else:
                    data = "total"
                    for i in range(1, len(input_string)):
                        data += input_string[i] + " "
                    data += "*"
                    try:
                        self.prmSock.sendall(data.encode())
                    except socket.error:
                        time.sleep(5)
                    self.receive(incomingTCP)  
           
            elif input_string[0] == 'replicate':
                print("CLI: replicate")
                #if correct num of args
                if len(input_string) == 2:
                    f = input_string[1] #filename
                    data = "replicate" + input_string[1] + "*"
                    try:
                        self.prmSock.sendall(data.encode())
                    except socket.error:
                        time.sleep(5)
                    self.receive(incomingTCP)
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
test.prmConnect(prmPort)
test.mapperConnect(1, mapPort1)
test.mapperConnect(2, mapPort2)
test.reducerConnect(reducerPort)
#test.setup()
print("-----------------------")
print("Outgoing TCP: ", outgoingTCP)
print("-----------------------")
print("Incoming TCP: ", incomingTCP)
print("-----------------------")
while True:
    test.commands()
print("done")
