#!/usr/bin/env python3
import sys
from socket import * 
import time
import select

incomingTCP = []
outgoingTCP = []

def mapper(File, offset, size):
	words = dict()
	#create dictionary to hold words from file
	temp = ""
	#create a temp empty string to hold what's being read into it
	f = open(fname, "r")
	f.seek(offset)
	#read file for chracters that fit the given size, and store in temp
	for i in range(size):
		temp += f.read(1)
	f.close()

	splitText = temp.split()
	#split the string's whitespace

	#the loop basically will add all words to dictionary while keeping track of how many
	for keywords in splitText:
		if(keywords in words.keys()):
			oldCounter = words.get(keywords)
			newCounter = int(oldCounter) + 1
			words[keywords] = newCounter
		else:
			words[keywords] = 1

	result = open(File, + "_I_" + uniqueid, "w")
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
print("mapper listening for CLI")
connection, address = cliServer.accept()
#address = cliServer.accept()
incomingTCP.append(connection)
print("CLI successfully connected to mapper")
#listen for connection from CLI

sock = socket(AF_INET,SOCK_STREAM)
address = (ip, int(cli))
time.sleep(5)
print("Mapper attempting to connect to CLI")
sock.connect(address)
outgoingTCP.append(sock)
print("Mapper successfully connected to CLI")
#open connection with CLI

while(True):
	#waiting for command
	process = connection.recv(1024).decode()
	if(not process):
		continue
	else:
		input_string_star = process.split("*")
                input_string = input_string_star[0].split()
		#command, check to see if its map
		if(input_string[0].find("map") != -1):
			#if it is the correct command, call the mapper function
			File = input_string[1]
			File_strip = File.encode('ascii','ignore')
			offset = input_string[2]
			offset_s = offset.encode('ascii', 'ignore')
                        #offset_strip = offset_s.replace("*", "")
			size = input_string[3]
			size_strip = size.encode('ascii', 'ignore')
                        print("MAPPER: File, offset, size:", File_strip, offset_strip, size_strip)
			mapper(File_strip, int(offset_strip), int(size_strip))
			send = "Mapper done"
			sock.sendall(send.encode()) 





