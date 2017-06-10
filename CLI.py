#!/usr/bin/env python3
from socket import *
import time
import sys

class cli:

    def __init__(self):
	   #needs to be able to determine how many sockets there will be
	   #needs to keep track of prm sockets
	   self.socket_to_map = None
	   self.socket_to_reduce = None
	   self.socket_prm_in = None #incoming from PRM
	   self.socket_prm_out = None #outgoing to PRM
	   print("CLI init'd")

    def setup(self):
        print("setup path taken")
	   #setup the cli
        ip = "127.0.0.1"
        nodePort = sys.argv[1]
        prmPort = sys.argv[2]
        #mapPort1 = sys.argv[3]
        #mapPort2 = sys.argv[4]
        #reducerPort = sys.argv[5]

        #incomingTCP = dict()
        #outgoingTCP = dict()
        prm_out_sock = socket(AF_INET, SOCK_STREAM)
        address = (ip, int(prmPort))
        time.sleep(5)
        print(" Init' the CLI at the address: ", address)
                
        #set up sockets 
        try:
            prm_out_sock.connect(address)
        except error:
            time.sleep(5)
        self.socket_prm_out = prm_out_sock
        #outgoingTCP.append(sock)
        print("CONNECTED")

        #Start server for PRM
        prm_in_sock = socket(AF_INET, SOCK_STREAM)
        prm_in_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        prm_in_sock.bind(('', int(nodePort)))
        prm_in_sock.listen(10)
        print("Receiving connection from PRMs")
        connection, address = prm_in_sock.accept()
        self.socket_prm_in = connection
        #incomingTCP.append(connection)
        print("Connection Successful")
		#move onto command execution
        #self.mapperConnect(1, mapPort1, server)
        #self.mapperConnect(2, mapPort2, server)
        #self.reducerConnect(reducerPort,server)
        #self.commands()

    def mapperConnect(self, id, port, server):
        #connect to mapper
        mapSock = socket(AF_INET, SOCK_STREAM)
        addr = (ip, int(port))
        print("connecting to mapper " + id)
        mapSock.connect(addr)
        outgoingTCP["mapper" + id] = mapSock

        #receive connection from mapper
        print("cli receiving connection from mapper1")
        connect = server.accept()
        addr = server.accept()
        incomingTCP["mapper" + id] = connect
        print("cli has connect with mapper" + id )

    def reducerConnect(self, port, server):
        reducerSock = socket(AF_INET, SOCK_STREAM)
        addr = (ip, int(port))
        print("connectig to reducer")
        reducerSock.connect(addr)
        outgoingTCP["reducer"] = reducerSock
        print("cli connected to reducer")

        #receive connection from reducer
        print("cli receiving connection from reducer")
        connection = server.accept()
        addr = server.accept()
        incomingTCP["reducer"] = connection
        print("cli has received connection from reducer")



    def commands(self):
	#we need to implement the replicate, stop, resume, total, print merge 
        name = raw_input("Enter Command: ")
        input_string = "lol"
        for line in name:
            print(line)
            #input_string = line.split()
                    
                    #set up blank message
                    # msg = ''
                    #character "*" used as delimiter for future message processing
            if(input_string[0] == "map"):
                if(len(input_string) != 4):
                    print("Invalid number of args, need 3 args")
                    continue
                file = input_string[1]
                offset = input_string[2]
                size = input_string[3]
                message = "map" + file + " " + offset + " " + size


            if input_string[0] == 'print':
                    if(len(input_string) != 1):
                        print("Print")
                        continue
                    sock.sendall("Print*".encode())
            elif line == 'stop':
                if(len(input_string) != 1):
                    print("stop")
                    continue
                print("worked")
                sock.sendall("stop*".encode())
            elif input_string[0] == 'resume':
                if(len(input_string) != 1):
                    print("resume")
                    continue
                sock.sendall("resume*".encode())
            elif input_string[0] == 'merge':
                #if correct num of args
                if len(input_string) == 3:
                    f1 = input_string[1]
                    f2 = input_string[2]
                    data = "merge" + f1 + " " + f2 + "*"
                    sock.sendall(data.encode())
                else:
                    print("Invalid number of args, need 3 args.")
            elif input_string[0] == 'total':
                #if correct num of args
                if len(input_string) == 3:
                    msg = 'total|'+input_string[1]+'|'+input_string[2]+'*'
                else:
                    print("Invalid number of args, need 3 args.")
                    continue
            elif input_string[0] == 'replicate':
                #if correct num of args
                if len(input_string) == 2:
                    f = input_string[1] #filename
                    data = "replicate" + input_string[1] + "*"
                    sock.sendall(data.encode())
                else:
                    print("Invalid number of args, need 2 args.")
            else:
                print("no matching command found.")
                print("Valid commands: print, stop, resume, merge, total, replicate")
                continue
                               
            if input_string != '':
                continue

test = cli()
test.setup()
while True:
    test.commands()
print("done")

