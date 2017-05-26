import socket
import time

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
		address = ('127.0.0.1', 6000 + self.id)
		address_out = ('127.0.0.1', 5000 +self.id)

		print("Init' the CLI at the address: ", address)
                
                #set up sockets
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(address)
		s.listen(1)
		connection, address_in = sock.accept()
                connection.setblocking(0)
                self.socket_prm_in = connection

                #when connection is successful
                print("conneection accepted from the PRM")

                #now try to connect to the PRM
                out_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               
                #keep trying until it works!!
                while True:
                    try:
                        out_sock.connect(address_out)
                        out_sock.setblocking(0)
                        #will only get here if previous 2 steps worked
                        print("connection established at address: ", address_out)

                        break
                    except socket.error:
                        #if it didn't work, just sleep and try again
                        time.sleep(1)

                self.socket_prm_out = out_sock
                #setup complete, notify CLI
                print("setup complete")

                #move onto command execution
                self.commands()


	def commands(self):
		#we need to implement the replicate, stop, resume, total, print merge 
                while True:
                    input_string = input("Input command: ")
                    input_string = input_string.strip().split()
                    
                    #set up blank message
                    msg = ''
                    #character "*" used as delimiter for future message processing
                    if input_string[0] == 'print':
                        msg = 'print*'
                    elif input_string[0] == 'stop':
                        msg = 'stop*'
                    elif input_string[0] == 'resume':
                        msg = 'resume*'
                    #for messages with multiple args, use "|" as splitter
                    elif input_string[0] == 'merge':
                        #if correct num of args
                        if len(input_string) == 3:
                            msg = 'merge|'+input_string[1]+'|'+input_string[2]+'*'
                        else:
                            print("Invalid number of args, need 3 args.")
                    elif input_string[0] == 'total':
                        #if correct num of args
                        if len(input_string) == 3:
                            msg = 'total|'+input_string[1]+'|'+input_string[2]+'*'
                        else:
                            print("Invalid number of args, need 3 args.")
                    if input_string[0] == 'replicate':
                        #if correct num of args
                        if len(input_string) == 2:
                            f = input_string[1] #filename
                            msg = 'replicate|'+f+'*'
                        else:
                            print("Invalid number of args, need 2 args.")
                    else:
                        print("no matching command found.")
                        print("Valid commands: print, stop, resume, merge, total, replicate")
                    
                    #send msg to all sockets
                    self.socket_prm_out.sendall(msg.encode())
                    #if msg has something, then wait.
                    if msg != '':
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


		#TODO:
		#So basically we can either implement the functions in here, or in the PRM 
		#It seems that we can just send messages to tell PRM to specific stuff
