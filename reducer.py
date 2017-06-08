#!/usr/bin/env python3
import sys
from socket import * 
import time
import select


incomingTCP = []
outgoingTCP = []

def reducer(groupMed, file):
	#groupMed like group of Medium/intermediate hah
	words = dict()
	for files in groupMed:
		with open(files) as f:
			for line in f.readlines()
			word = currentLine[0]
			counter = int(currentLine[1])
			if(word in words.keys()):
				oldCounter = words.get(word)
				newCounter = int(oldCounter + counter)
				words[word] = newCounter
			else:
				words[word] = count


	temp = file.split("_")[0]	
	newFile = temp + "_reduced"		
	result = open(file, "w")
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
uniqueid = sys.argv[3]

cliServer = socket(AF_INET, SOCK_STREAM)
cliServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cliServer.bind(('', int(port)))
cliServer.listen(5)
connection = cliServer.accept()
address = cliServer.accept()
incomingTCP.append(connection)
#listen for connection from CLI

sock = socket(AF_INET,SOCK_STREAM)
address = (ip, int(cli))
time.sleep(5)
sock.connect(address)
outgoingTCP.append(sock)
#open connection with CLI

while(True):
	#waiting for command
	process = connection.recv(1024).decode()
	if(not process):
		continue
	else:
		groupMed = []
		input_string = process.split()
		#command, check to see if its map
		if(input_string[0].find("reduce") != -1):
			#if it is the correct command, call the mapper function
			file = input_string[1]
			for i in range(1, len(input_string)):
			f = input_string[i]
			groupMed.append(f)
			reducer(groupMed, file)
