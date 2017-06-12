#!/usr/bin/env python3
import sys
import time
import select
import os
from socket import *

#2nd and 3rd arguments will be ports of mappers.
#4th argument will be port of reducer.

myPort = 5001
map1Port = 5002
map2Port = 5003
reducerPort = 5004
prmPort = 5005 

myIncomingConnections = dict()
myOutgoingConnections = dict()

def fileToDict(theFile):
    result = ""
    with open(theFile) as f:
        for line in f.readlines():
            curLine = line.split()
            result += curLine[0] + " " + curLine[1] + " "
    return result


def receive(channels):
    received = False
    now = time.time()   #Current time
    future = now + 10
    #Time out feature
    while(not received):
        if(time.time() > future):
            print("Command timed out")
            return
        for c in channels.keys():
            sock = channels.get(c)
            ready = select.select([sock], [], [], 1)
            if(ready[0]):
                theData = sock.recv(1024).decode()
                print(theData)
                received = True
    return

#Splits file in half and determines size and offset parameters for the mappers
def splitFile(fname):
    fSize = os.path.getsize(fname) - 1
    f1Size = fSize//2        #Use integer division
    f2Size = fSize - f1Size  #In the case of an odd numbered size
    f1Offset = 0             #Offset for 1st mapper
    f2Offset = f1Size        #Offset for 2nd mapper
    return f1Size, f1Offset, f2Size, f2Offset


#Connect to PRM
ip = '127.0.0.1'
prmSock = socket(AF_INET, SOCK_STREAM)
prmAddr = (ip, int(prmPort))
time.sleep(2)
print("CLI connecting to PRM...")
prmSock.connect(prmAddr)
myOutgoingConnections["prm"] = prmSock
print("CLI connected to PRM")

#Initialize server for PRM, Mappers, and Reducer
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('0.0.0.0', int(myPort)))
server.listen(10)
print("CLI receiving connection from PRM...")
conn, addr = server.accept()
myIncomingConnections["prm"] = conn
print("CLI received connection from PRM")

#Connect to Mapper1
map1Sock = socket(AF_INET, SOCK_STREAM)
map1Addr = (ip, int(map1Port))
print("CLI connecting to Mapper1...")
map1Sock.connect(map1Addr)
myOutgoingConnections["map1"] = map1Sock
print("CLI connected to Mapper1")

#Receive connection from Mapper1
print("CLI receiving connection from Mapper1...")
map1Conn, map1Addr = server.accept()
myIncomingConnections["map1"] = map1Conn
print("CLI received connection from Mapper1")


#Connect to Mapper2
map2Sock = socket(AF_INET, SOCK_STREAM)
map2Addr = (ip, int(map2Port))
print("CLI connecting to Mapper2...")
map2Sock.connect(map2Addr)
myOutgoingConnections["map2"] = map2Sock
print("CLI connected to Mapper2")

#Receive connection from Mapper2
print("CLI receiving connection from Mapper2...")
map2Conn, map2Addr = server.accept()
myIncomingConnections["map2"] = map2Conn
print("CLI received connection from Mapper2")


#Connect to Reducer
reducerSock = socket(AF_INET, SOCK_STREAM)
reducerAddr = (ip, int(reducerPort))
print("CLI connecting to Reducer...")
reducerSock.connect(reducerAddr)
myOutgoingConnections["reducer"] = reducerSock
print("CLI connected to Reducer")

#Receive connection from Mapper1
print("CLI receiving connection from Reducer...")
reducerConn, reducerAddr = server.accept()
myIncomingConnections["reducer"] = reducerConn
print("CLI received connection from Reducer")
            

#Set up command line interface
for line in sys.stdin:
    theLine = line.split()

    if(theLine[0] == "map"):
        #Map function, send to one of the mappers
        if(len(theLine) != 2):
            print("Usage: map [file]")
            continue
        fname = theLine[1]
        f1Size, f1Offset, f2Size, f2Offset = splitFile(fname)
        toSend = "map " + fname + " " + str(f1Size) + " " + str(f1Offset)
        toSend2 = "map " + fname + " "+  str(f2Size) + " " + str(f2Offset)
        map1Sock.sendall(toSend.encode())
        map2Sock.sendall(toSend2.encode())
        receive(myIncomingConnections)
        
    elif(theLine[0] == "reduce"):
        #Reduce funciton, send to reducer
        if(len(theLine) < 2):
            print("Usage: reduce [fname1] [fname2] ...")
            continue
        files = "reduce "
        for i in range(1, len(theLine)):
            files += theLine[i] + " "
        #files += "*"
        reducerSock.sendall(files.encode())
        receive(myIncomingConnections)
        
    elif(theLine[0] == "replicate"):
        #Replicate funciton, send to PRM
        if(len(theLine) != 2):
            print("Usage: replicate [filename]")
            continue
        fname = theLine[1]
        dictionary = fileToDict(fname)  #Convert dict of file to a string
        data = "replicate " + fname + " " + dictionary + "*"
        prmSock.sendall(data.encode())  #Send a replicate
        receive(myIncomingConnections)
        
    elif(theLine[0] == "stop"):
        #Stop function, send to PRM
        if(len(theLine) != 1):
            print("Usage: stop")
            continue
        prmSock.sendall("stop*".encode())  #Send a stop msg
        receive(myIncomingConnections)
        
    elif(theLine[0] == "resume"):
        #Resume function, send to PRM
        if(len(theLine) != 1):
            print("Usage: resume")
            continue
        prmSock.sendall("resume*".encode())
        receive(myIncomingConnections)
        
    elif(theLine[0] == "total"):
        #Total function, send to PRM
        if(len(theLine) < 2):
            print("Usage: total [pos1] [pos2] ...")
            continue
        data = "total "
        for i in range(1, len(theLine)):
            data += theLine[i] + " "
        data += "*"
        prmSock.sendall(data.encode())
        receive(myIncomingConnections)
            
    elif(theLine[0] == "print"):
        #Print funciton, send to PRM
        if(len(theLine) != 1):
            print("Usage: print")
            continue
        prmSock.sendall("print*".encode())
        receive(myIncomingConnections)

    elif(theLine[0] == "merge"):
        #Merge function, send to PRM
        if(len(theLine) != 3):
            print("Usage: merge [pos1] [pos2]")
            continue
        f1 = theLine[1]
        f2 = theLine[2]
        data = "merge " + f1 + " " + f2 + "*" 
        prmSock.sendall(data.encode())
    elif(theLine[0] == "quit"):
        #Merge function, send to PRM
        if(len(theLine) != 1):
            print("Usage: quit")
        prmSock.sendall("quit*".encode())
    else:
        print("Command not recognized. Make sure commands don't include capital letters")
        continue