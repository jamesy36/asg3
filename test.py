#!/usr/bin/env python3
import sys
import time
import select
from socket import *

PRM = []  #Holds all Paxos instances
prmBackup = []
incomingConnections = dict() #Maintains incoming connections
outgoingConnections = dict() #Maintains outgoing connections
siteData = []  #Contains IP and Port of all sites in order of siteNum
isStopped = False  #True if the process is stopped, False otherwise
numAccepts = dict()

#Have a variable that determines if you are the first propser or not.
#If youre the first proposer, your value is decided, otherwise, your value will be ignored

class Paxos(object):

    def __init__(self, ballotNum = [0, 0], acceptBallot = [0, 0], acceptVal = ["-1", "-1"],
                 proposedVal = ["-1" , "-1"], numVotes = 1, leader = False):
        #self.numAccepts = numAccepts     #number of accepts received on ballotNum b
        self.ballotNum = ballotNum
        self.acceptBallot = acceptBallot
        self.acceptVal = acceptVal      #File/Dictionary pair
        self.ackList = []#ackList          #Contains acks received from other sites
        self.proposedVal = proposedVal  #-1 acts as a stub, or null
        self.numVotes = numVotes        #Starts at 1 cuz a process votes for itself
        self.leader = leader            #Starts at False and changes to true if it wants to propose a val

    def reinstantiate(self):
        #This is to reinitialize variables to their initial vals
        #after a value has been decided from a paxos round
        #numAccepts.clear()
        self.ballotNum = [0, 0]
        self.acceptBallot = [0, 0]
        self.acceptVal = ["-1", "-1"]
        self.numVotes = 1
        self.ackList.clear()
        self.proposedVal = ["-1", "-1"]
        self.leader = False

    def printPaxos(self):
        sys.stdout.write("ballotNum: ")
        print(self.ballotNum)
        sys.stdout.write("acceptBallot: ")
        print(self.acceptBallot)
        sys.stdout.write("acceptVal: ")
        print(self.acceptVal)
        sys.stdout.write("ackList: ")
        print(self.ackList)
        sys.stdout.write("proposedVal: ")
        print(self.proposedVal)
        sys.stdout.write("numVotes: ")
        print(self.numVotes)
        sys.stdout.write("leader: ")
        print(self.leader)

def printFiles(theList):
    #theList in this case is the PRM list
    dataList = ""
    for data in theList:
        dataList += data[0]  #Index 0 is the filename
        dataList += " "
    return dataList


def merge(theList):
    words = dict()
    for string in theList:
        newList = string.split()
        for i in range(0, len(newList), 2):
            word = newList[i]
            count = int(newList[i+1])
            if(word in words.keys()):
                oldCount = words.get(word)
                newCount = int(oldCount + count)
                words[word] = newCount
            else:
                words[word] = count
    print(words)
    return words


def total(theList):
    total = 0
    for string in theList:
        newList = string.split()
        for i in range(0, len(newList), 2):
            total += int(newList[i+1])
    #print(total)
    return total


def checkIfAcksAreNull(theList):
    for ack in theList:
        if(ack[2][0] != "-1" and ack[2][1] != "-1"): #This means accVal isn't null
            return False
    return True

def ackWithHighestBal(theList):
    #print(theList)
    balNum = 0
    siteid = 0
    highest = [0, 0]
    for ack in theList:
        if(int(ack[0][0]) > balNum or(int(ack[0][0]) == balNum and int(ack[0][1]) > siteid)):
            balNum = theList[0][0]
            siteid = theList[0][1]
            highest = [balNum, siteid]
    return highest

def receive(channels):
    global isStopped
    global numAccepts
    global PRM
    global prmBackup
    
    for c in channels.keys():
        sock = channels.get(c)
        ready = select.select([sock], [], [], 1)
        if(ready[0]):
            theData = sock.recv(1024).decode()
            while(theData[-1] != '*'):
                theData += sock.recv(1024).decode()
            #sys.stdout.write("theData: ")
            #print(theData)
            splitData = theData.split("*")
            #if(splitData[0] != ''):
                #sys.stdout.write("splitData: ")
                #print(splitData)
            for data in range(0, len(splitData) - 1):
                dataList = splitData[data].split()
                #sys.stdout.write("dataList: ")
                #print(dataList)
                if(dataList[0].find("resume") != -1):
                    #print("resume")
                    isStopped = False
                    PRM = prmBackup[:]
                    for c in outgoingConnections.keys():
                        if(c == "cli"):
                            #Send to cli only
                            sock = outgoingConnections.get(c)
                            sock.sendall("Process resumed".encode())
                #Make sure dataList isn't empty
                elif(not dataList or isStopped or dataList[0] == ''):
                    #print("dataList is empty or process is stopped")
                    if(isStopped and dataList and dataList[0].find("decide") != -1):
                        val = dataList[1]
                        dictionary = dataList[2]
                        prmBackup.append([val, dictionary])
                    continue
                elif(dataList[0].find("merge") != -1):
                    #print("merge")
                    #dataList[1] and dataList[2] are the positions
                    f1 = PRM[int(dataList[1])][1]
                    f2 = PRM[int(dataList[2])][1]
                    fileList = [f1, f2]
                    merge(fileList)
                elif(dataList[0].find("total") != -1):
                    #print("total")
                    fileList = []
                    for i in range(1, len(dataList)):
                        f = PRM[int(dataList[i])][1]
                        fileList.append(f)
                    theTotal = str(total(fileList))
                    for c in outgoingConnections.keys():
                        if(c == "cli"):
                            #Send to cli only
                            sock = outgoingConnections.get(c)
                            sock.sendall(theTotal.encode())
                elif(dataList[0].find("replicate") != -1):
                    prmObj.ballotNum[0] = 1   #Increase ballotNum of PRM object
                    prmObj.ballotNum[1] = mySiteid
                    prmObj.proposedVal[0] = dataList[1]  #filename being proposed
                    dictionary = ""
                    for i in range(2, len(dataList)):
                        dictionary += dataList[i]
                        dictionary += " "
                    prmObj.proposedVal[1] = dictionary
                    prmObj.leader = True
                    toSend = "prepare " + str(prmObj.ballotNum[0]) + " " + str(prmObj.ballotNum[1]) + "*"
                    for c in outgoingConnections.keys():
                        if(c != "cli"):
                            #Send to everyone except cli
                            sock = outgoingConnections.get(c)
                            sock.sendall(toSend.encode())
                elif(dataList[0].find("stop") != -1):
                    #print("stop")
                    isStopped = True
                    for c in outgoingConnections.keys():
                        if(c == "cli"):
                            #Send to cli only
                            sock = outgoingConnections.get(c)
                            sock.sendall("Process stopped".encode())
                elif(dataList[0].find("print") != -1):
                    #print("print")
                    toSend = printFiles(PRM)
                    for c in outgoingConnections.keys():
                        if(c == "cli"):
                            #Send to cli only
                            sock = outgoingConnections.get(c)
                            sock.sendall(toSend.encode())
                elif(dataList[0].find("prepare") != -1):
                    bal = int(dataList[1])    #Ballot
                    siteid = dataList[2]      #id of site it came from
                    if(int(prmObj.ballotNum[0]) < bal or (int(prmObj.ballotNum[0]) == bal and int(prmObj.ballotNum[1]) < int(siteid))):
                        #print("Ballot num less in prepare")
                        prmObj.ballotNum[0] = bal
                        prmObj.ballotNum[1] = siteid
                        toSend = "ack " + str(prmObj.ballotNum[0]) + " "  + str(prmObj.ballotNum[1]) + " " + str(prmObj.acceptBallot[0]) + " " + str(prmObj.acceptBallot[1]) + " " + prmObj.acceptVal[0] + " " + prmObj.acceptVal[1] + " "  + mySiteid + "*"
                        sock = outgoingConnections.get(siteid) #Get socket associated w id
                        sock.sendall(toSend.encode())
                elif(dataList[0].find("ack") != -1):
                    balNum = [dataList[1], dataList[2]]
                    accBal = [dataList[3], dataList[4]]
                    accVal = [dataList[5], dataList[6]]
                    fromSite = dataList[7]
                    thisAck = [balNum, accBal, accVal, fromSite]
                    prmObj.ackList.append(thisAck)
                    #Check if site has acks from majority
                    if(len(prmObj.ackList) + 1 >= 2): # +1 cuz site votes for itself 
                        if(checkIfAcksAreNull(prmObj.ackList)):
                            #If yes and all vals are null, then acceptVal = my initial proposed val
                            prmObj.acceptVal = prmObj.proposedVal[:]
                        else:
                            #Else acceptVal = received val with highest ballot num
                            prmObj.acceptVal = ackWithHighestBal(prmObj.ackList)[:]
                        #Send accept, ballotNum, acceptVal to all
                        for c in outgoingConnections.keys():
                            if(c != "cli"):
                                #Send to everyone except cli
                                sock = outgoingConnections.get(c)
                                toSend = "accept " + str(prmObj.ballotNum[0]) + " "  + str(prmObj.ballotNum[1]) + " " + prmObj.acceptVal[0] + " " + prmObj.acceptVal[1] + "*"
                                sock.sendall(toSend.encode())
                elif(dataList[0].find("accept") != -1):
                    #print("IN ACCEPT")
                    ballot = str(dataList[1]) + str(dataList[2])

                    if(int(ballot[0]) == int(prmObj.ballotNum[0]) and int(ballot[1]) == int(prmObj.ballotNum[1]) and prmObj.leader and ballot[1] == mySiteid):
                        if(ballot in numAccepts):
                            #If its in the dict, increase its count
                            numAccepts[ballot] += 1
                        else:
                            #If its not in the dict, put it in and set its count to 1
                            numAccepts[ballot] = 1
                        #print("THEY ARE EQUAL")
                        if(numAccepts[ballot] >= 1 and prmObj.leader): # >= 2?
                            #print("DECIDING VALUE")
                            #Decide value
                            PRM.append([prmObj.acceptVal[0], prmObj.acceptVal[1]])
                            prmBackup.append([prmObj.acceptVal[0], prmObj.acceptVal[1]])
                            toSend = "decide " + str(prmObj.acceptVal[0]) + " " + str(prmObj.acceptVal[1]) + "*"
                            for c in outgoingConnections.keys():
                                if(c != "cli"):
                                    sock = outgoingConnections.get(c)
                                    sock.sendall(toSend.encode())
                            for c in outgoingConnections.keys():
                                if(c == "cli"):
                                    time.sleep(1)
                                    toSend = "The winner was " + str(prmObj.acceptVal[0])
                                    sock = outgoingConnections.get(c)
                                    sock.sendall(toSend.encode())
                            #print("Reinstantiate")
                            prmObj.reinstantiate()
                            numAccepts.clear()
                            #Flush out the incoming channels to prepare for the next round
                            for c in incomingConnections.keys():
                                sock = channels.get(c)
                                ready = select.select([sock], [], [], 1)
                                if(ready[0]):
                                    theData = sock.recv(1024).decode()
                            return  # NEW ***
                    
                    elif(int(prmObj.ballotNum[0]) < int(dataList[1]) or (int(prmObj.ballotNum[0]) == int(dataList[1]) and int(prmObj.ballotNum[1]) <= int(dataList[2]))):
                        #Assign ballotNum, acceptBallot, and acceptVal if my ballotNum is less
                        dictionary = ""
                        for i in range(4, len(dataList)):
                            dictionary += dataList[i]
                            dictionary += " "
                        prmObj.ballotNum[0] = int(dataList[1])
                        prmObj.ballotNum[1] = int(dataList[2])
                        prmObj.acceptBallot[0] = int(dataList[1])
                        prmObj.acceptBallot[1] = int(dataList[2])
                        accVal = [dataList[3], dictionary]
                        prmObj.acceptVal = accVal[:]
                        prmObj.leader = False
                        ballot = str(prmObj.ballotNum[0]) + str(prmObj.ballotNum[1])  #NEW
                        if(ballot in numAccepts):
                            #If its in the dict, increase its count
                            numAccepts[ballot] += 1
                            #print("numAccepts[ballot] += 1")
                        else:
                            #If its not in the dict, put it in and set its count to 1
                            numAccepts[ballot] = 1
                            #print("numAccepts[ballot] = 1")
                        if(numAccepts[ballot] == 1):
                            #print("numAccepts[ballot] == 1")
                            #First accept received by this ballotNum b
                            toSend = "accept " + str(dataList[1]) + " " + str(dataList[2]) + " " + str(dataList[3]) + " " + dictionary + "*"
                            for c in outgoingConnections.keys():
                                if(c != "cli"):
                                    #Send to everyone except cli
                                    sock = outgoingConnections.get(c)
                                    sock.sendall(toSend.encode())
                        #break; #NEW ***

                elif(dataList[0].find("decide") != -1):
                    dictionary = ""
                    for i in range(2, len(dataList)):
                        dictionary += dataList[i]
                        dictionary += " "
                    accVal = [dataList[1], dictionary]
                    PRM.append(accVal)
                    prmBackup.append(accVal)
                    numAccepts.clear()
                    #prmObj.printPaxos()
                    #sys.stdout.write("Printing PRM: ")
                    #print(PRM)
                    for c in outgoingConnections.keys():
                        if(c == "cli" and prmObj.proposedVal[0] != "-1"):
                            time.sleep(1)
                            toSend = "The winner was " + str(dataList[1])
                            sock = outgoingConnections.get(c)
                            sock.sendall(toSend.encode())
                    prmObj.reinstantiate()
                    #Flush out the incoming channels to prepare for the next round
                    for c in incomingConnections.keys():
                        sock = channels.get(c)
                        ready = select.select([sock], [], [], 1)
                        if(ready[0]):
                            theData = sock.recv(1024).decode()
            
                    return # NEW ***
                elif(dataList[0].find("quit") != -1):
                    #Terminate process
                    for c in outgoingConnections.keys():
                        if(c != "cli"):
                            #Send quit to other PRMs
                            sock = outgoingConnections.get(c)
                            sock.sendall("quit*".encode())
                    time.sleep(1)
                    sys.exit("Terminating PRM")
                    
                else:
                    continue
    return

#Create prm object
prmObj = Paxos()


#Initialize server
port = 5005
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

mySiteid = sys.argv[1]   #ID of this site
setupFile = sys.argv[2]  #Setup file
print("Establishing connections...")
with open(setupFile) as f:
    numSites = f.readline().strip()   #Number of sites
    
    for i in range(int(numSites)):
        line = f.readline().strip().split()
        siteData.append([data for data in line])
    
    server.bind(('0.0.0.0', port)) #int(siteData[int(mySiteid) - 1][1])
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.listen(10)
    
    for line in f.readlines():
        #Establish Connections with other sites
        nums = line.strip().split()
        if(nums[0] == mySiteid):
            ip = siteData[int(nums[1])-1][0]
            port = siteData[int(nums[1])-1][1]
            s = socket(AF_INET, SOCK_STREAM)
            addr = (ip, int(port))
            time.sleep(3)
            try:
                s.connect(addr)
                print("Connected to ", (nums[1]))
            except error:
                print("IN EXCEPT")
                time.sleep(2)
            #Add socket to outgoing connections
            outgoingConnections[nums[1]] = s
            #sys.stdout.write("Outgoing: ")
            #print(outgoingConnections)
        if(nums[1] == mySiteid):
            #Incoming connection
            conn, addr = server.accept()
            #print("Got connection from ", (nums[0]))
            incomingConnections[nums[0]] = conn
            #sys.stdout.write("Incoming: ")
            #print(incomingConnections)

#Receive the connection from the CLI
conn, addr = server.accept()
incomingConnections["cli"] = conn
#print("Received connection from CLI")


#Open a connection with the CLI
cliPort = 5001 #int(siteData[int(mySiteid) - 1][1]) + 3  #3 greater than the port of this site
cliIP = '127.0.0.1'
s = socket(AF_INET, SOCK_STREAM)
addr = (cliIP, cliPort)
time.sleep(2)
s.connect(addr)
outgoingConnections["cli"] = s

#print(incomingConnections)
#print(outgoingConnections)

#print("Ready to process commands...")
while(True):
    receive(incomingConnections)