#!/usr/bin/env python3
import sys
import time
import select
from socket import *

def mapper(fname, offset, size):
    global myid
    #Create dictionary for words
    words = dict()
    #Create an empty string to hold what is read in
    text = ""
    #Open file and seek to the offset
    f = open(fname, "r")
    entireFile = f.read().replace('\n', '')
    #Check if we're at the beginning of a word (but not the first word)
    if(offset > 0):
        if(entireFile[offset - 1] == ' ' and entireFile[offset] != ' '):
            offset -= 1
            size += 1
            
    f.seek(offset)
    #Continue reading file for size characters and store in a string
    for i in range(size):
        text += f.read(1)

    #If offset is in middle of word, mapper1 reads the word, mapper2 skips it
    if(myid == 1):
        while(text[-1] != ' '):
            text += f.read(1)
            #size += 1
            #offset += 1
    if(myid == 2):
        while(text[0] != ' '):
            text = text[1:]
            #size -= 1
            #offset += 1

    f.close()        
    #Split the string by whitespace
    splitText = text.split()
    #Add all words to dictionary and keep track of counts
    for theWord in splitText:
        if(theWord in words.keys()):
            oldCount = words.get(theWord)
            newCount = int(oldCount) + 1
            words[theWord] = newCount
        else:
            words[theWord] = 1
    #Write the dictionary to the file
    newFname = fname.split('.')[0]
    newFile = open(newFname + "_I_" + str(myid), "w")
    for k in words.keys():
        newFile.write(str(k))
        newFile.write(" ")
        newFile.write(str(words.get(k)))
        newFile.write("\n")
    newFile.close()
    return
        

myIncomingConnections = []
myOutgoingConnections = []

ip = '127.0.0.1'
cliPort = 5001
myid = int(sys.argv[1])

if(myid == 1):
    port = 5002
if(myid == 2):
    port = 5003

#Listen for connection from CLI
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('0.0.0.0', int(port)))
server.listen(5)
conn, addr = server.accept()
myIncomingConnections.append(conn)

#Open up connection with CLI
sock = socket(AF_INET, SOCK_STREAM)
addr = (ip, int(cliPort))
time.sleep(3)
sock.connect(addr)
myOutgoingConnections.append(sock)

#Listen for commads
while(True):
    data = conn.recv(1024).decode()
    if(not data):
        continue
    else:
        #print(data)
        dataList = data.split()
        if(dataList[0].find("map") != -1):
            fname = dataList[1]
            size = int(dataList[2])
            offset = int(dataList[3])
            mapper(fname, offset, size)
            sendSock = myOutgoingConnections[0]
            thisMapper = "Mapper " + str(myid)
            toSend = thisMapper + " done."
            sendSock.sendall(toSend.encode())