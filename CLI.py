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
                self.execute_commands()


	def commands(self):
		#we need to implement the replicate, stop, resume, total, print merge 

	def wait(self):
		#we need to waitfor a single process to finish before we do another


		#TODO:
		#So basically we can either implement the functions in here, or in the PRM 
		#It seems that we can just send messages to tell PRM to specific stuff
