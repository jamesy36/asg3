#!/usr/bin/env python3
import sys
import time
import select
from socket import *

def reducer(theList, fname):
    words = dict()
    for filename in theList:
        with open(filename) as f:
            for line in f.readlines():
                currentLine = line.split()
                word = currentLine[0]
                count = int(currentLine[1])
                if(word in words.keys()):
                    oldCount = words.get(word)
                    newCount = int(oldCount + count)
                    words[word] = newCount
                else:
                    words[word] = count
    #Create the file to write to
    splitFile = fname.split('_')[0]
    newFile = splitFile + "_reduced"
    openFile = open(newFile, "w")
    for k in words.keys():
        openFile.write(str(k))
        openFile.write(" ")
        openFile.write(str(words.get(k)))
        openFile.write("\n")
    openFile.close()
    return

myIncomingConnections = []
myOutgoingConnections = []

ip = '127.0.0.1'
port = 5004
cliPort = 5001

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
time.sleep(5)
sock.connect(addr)
myOutgoingConnections.append(sock)

#Listen for commads
while(True):
    data = conn.recv(1024).decode()
    if(not data):
        continue
    else:
        #print(data)
        fileList = []
        dataList = data.split()
        if(dataList[0].find("reduce") != -1):
            fname = dataList[1]
            for i in range(1, len(dataList)):
                f = dataList[i]
                fileList.append(f)
            reducer(fileList, fname)
            sendSock = myOutgoingConnections[0]
            toSend = "Reducer done."
            sendSock.sendall(toSend.encode())