from socket import *
import time
import sys

class cli:
   

    def _init_(self, id):
	   #needs to be able to determine how many sockets there will be
	   #needs to keep track of prm sockets
	   self.id = id
	   self.socket_to_map = None
	   self.socket_to_reduce = None
	   self.socket_prm_in = None #incoming from PRM
	   self.socket_prm_out = None #outgoing to PRM

    def setup(self):
	   #setup the cli
        ip = "127.0.0.1"
        nodePort = sys.argv[1]
        prmPort = sys.argv[2]
        #mapPort1 = sys.argv[3]
        #mapPort2 = sys.argv[4]
        #reducerPort = sys.argv[5]

        incomingTCP = []
        outgoingTCP = []
        sock = socket(AF_INET, SOCK_STREAM)
        address = (ip, int(prmPort))
        time.sleep(5)

		print(" Init' the CLI at the address: ", address)
                
         #set up sockets 
		sock.connect(address)
        outgoingTCP.append(sock)
        print("CONNECTED")

        #Start server for PRM
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_RESUSEADDR, 1)
        server.bind(('', int(nodePort)))
        server.listen(10)
        print("Receiving connection from RPMS")
        connection = server.accept()
        address = server.accept()
        incomingTCP.append(connection)
        print("Connection Successful")
		#move onto command execution
        self.commands()


	def commands(self):
		#we need to implement the replicate, stop, resume, total, print merge 
         for line in sys.stdin:
            print(line)
            input_string = line.split()
                    
                    #set up blank message
                    # msg = ''
                    #character "*" used as delimiter for future message processing
            if input_string[0] == 'print':
                if(len(input_string) != 1):
                    print("Print")
                    continue
                    sock.sendall("Print*".encode())
            elif input_string[0] == 'stop':
                if(len(input_string) != 1):
                    print("stop")
                    continue
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
                                       
            if input_string != '':
                        self.wait_response()
                    
	def wait_response(self):
		#we need to waitfor a single process to finish before we do another
		while True:  
            try:
                data_recv = self.socket_prm_in.recv(1024).decode()
                print("Data received: ", data_recv)

                data_proc = data_recv.strip().split('*')
                if len(data_recv) >= 1:
                    if data_proc[0] == 'ack':
                        print('msg successfully passed and exed')
                        return
                    if data_proc[0] == 'nack':
                        print('msg NOT successfully passed and exed--investigate further!')
                        return
            except socket.error:
                print("Socket error experienced--investigate further :(")
                continue
            time.sleep(1)


		