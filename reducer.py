#!/usr/bin/env python3
import sys
from socket import * 
import time
import select


incomingTCP = []
outgoingTCP = []

def reducer(groupMed, File):
	#groupMed like group of Medium/intermediate hah
	words = dict()
	for files in groupMed:
		with open(files) as f:
                    for line in f.readlines():
                        l = line.split()
			word = l[0]
			print(l[1])
			counter = int(l[1])
			if(word in words.keys()):
				oldCounter = words.get(word)
				newCounter = int(oldCounter + counter)
				words[word] = newCounter
			else:
				words[word] = counter


	temp = File.split("_")[0]	
	newFile = temp + "_reduced"		
	result = open(File, "w")
	for i in words.keys():
		result.write(str(i))
		result.write(" ")
		result.write(str(words.get(i)))
		result.write("\n")
	result.close()
	return



ip = "127.0.0.1"
port = sys.argv[1]
cli = sys.argv[2]


cliServer = socket(AF_INET, SOCK_STREAM)
cliServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cliServer.bind(('', int(port)))
cliServer.listen(5)
print("Reducer listening for CLI connection")
connection, address = cliServer.accept()
incomingTCP.append(connection)
print("CLI successfully connected to Reducer")
#listen for connection from CLI

sock = socket(AF_INET,SOCK_STREAM)
address = (ip, int(cli))
time.sleep(5)
print("Reducer connecting to CLI")
sock.connect(address)
outgoingTCP.append(sock)
print("Reducer successfully connected to CLI")
#open connection with CLI

while(True):
	#waiting for command
	process = connection.recv(1024).decode()
        #print("REDUCER: ", process)
	if(not process):
		continue
	else:
		g = []
		input_string = process.split()
		#command, check to see if its map
		if(input_string[0].find("reduce") != -1):
			#if it is the correct command, call the mapper function
			File = input_string[1]
                        print("REDUCER: ", File)
			for i in range(1, len(input_string)):
			    f = input_string[i]
			    g.append(f)
			print("REDUCER: g line 83:", g)
			reducer(g, File)
			Ssock = outgoingTCP[0]
			send = "Reducer finished"
			Ssock.sendall(send.encode())
