#!/usr/bin/env python3
import sys
from socket import * 
import time
import select

incomingTCP = dict()
outgoingTCP = dict()
siteInfo = [] #a list that contains ip/port for nodes 

log = [] #holds all of the instances for paxos during the process
backupLog  = [] #this will counter in case a node fails, it needs to brought up to date
stop = False #if a process gets stopped it'll be true

accepts = dict()

class PRM(object):

	

	def _init_(self, index, id ):
		self.accepts = dict()
		self.ballotNum = [0,0]
		self.ackList = [] #we need to keep track of the acks from other siteInfo
		self.propVal = None #null until a value has been proposed
		self.acceptBal = [0,0]
		self.numVotes = 1
		self.leader = False #starts at false 
		self.acceptVal = None #null until a value has been accepted 
		self.id = id
		self.p = 0 #port

	def reinit(self):
		#the point is to restart the ballots/values to initial vals
		#self.accepts.clear()
		#we don't clear top because we might need another round of paxos
		self.ballotNum = [0,0]
		self.ackList.clear() #we need to keep track of the acks from other siteInfo
		self.propVal = None #null until a value has been proposed
		self.acceptBal = [0,0]
		self.numVotes = 1
		self.leader = False #starts at false 
		self.acceptVal = None #null until a value has been accepted 
		self.p = 0
		


	def total(files):
		total = 0
		for filename in files:
			with open(filename) as f:
				for line in f.readlines():
					with open(filename) as f:
						for line in f.readlines():
							currentLine = line.split()
							counter = int(currentLine[1])
							total += counter
		return total



	def printFiles(log):
		#print out log, but it could realistically work with others
		result = ""
		for data in log:
			result += data[0]
			result += " "
		return result

	def merge(input_string):
		words = dict()
		for filename in input_string:
			with open(filename) as f:
				for line in f.readlines():
					currentLine = line.split()
					word = currentline[0]
					count = int(currentLine[1])
					if(word in words.keys()):
						oldCount = words.get(word)
						newCount = int(oldCount + count)
						words[word] = newCount
					else:
						words[word] = count
		print(words)
		return words



	def acknowledgeCheck(logs):
		for ack in logs:
			if(ack[2][0] != None and ack[2][1] != None ):
				return True

		return False 


	def highestBallot(logs):
		ballotNum = 0
		siteNum = 0
		highest = [0,0]
		for ack in logs:
			if(logs[0][0] > ballotNum or (logs[0][0] == ballotNum and log[0][1] > siteNum)):
				ballotNum = logs[0][1]
				siteNum = logs[0][1]
				highest = [ballotNum, siteNum]

		return highest


        def receive(self, channels):
		global stop
		global log
		global backupLog


		for c in channels.keys():
			sock = channels.get(c)	
			ready = select.select([sock], [], [], 1)
			if(ready[0]):
				data = sock.recv(1024).decode()
				#print(data)
				#above to help with debug
				splitData = data.split("*")
				if(splitData[0] != " "):
					sys.stdout.write("processes:")
					print(process)
				for data in range(0 , len(splitData) - 1):
					process = splitData[data].split()
					sys.stdout.write("processes:")
					print(process)
					if(process[0].find("resume") != -1):
						#in case we're rerunning it
						print("resume")
						stop = False
						log = backupLog[:]
						for c in outgoingTCP.keys():
							if(c == "cli"):
								sock = outgoingTCP.get(c)
								sock.sendall("process resuming".encode())
					#WE NEED TO INCLUDE A FAIL SAFE IN CASE self CRASHES
					#BACKUP self?!?!?!?!!?
					#backup printt
					elif(not process and stop and process[0] == " "):
						print("error: process has been stopped/is empty")
						if(stop and (process != 0) and (process.find("decide") != -1)):
							key = process[1]
							value = process[2]
							backupLog.append([key, value])
						continue

					elif(process[0].find("total") != -1):
						print("total")
						files = []
						for i in range(1, len(process)):
							f = log[int(process[i])][1]
							files.append(f)
						result = str(total(files))
						for c in outgoingTCP.keys():
							if(c == "cli"):
								print("cli key!")
								sock = outgoingTCP.get(c)
								sock.sendall(result.encode())
					
					elif(process[0].find("print") != -1):
						print("print")
						result = printFiles(log) 
						for c in outgoingTCP.keys():
							if(c == "cli"):
								sock = outgoingTCP.get(c)
								sock.sendall(result.encode())
					
					elif(process[0].find("merge") != -1):
						print("merge")
						f1 = log[int(process[1])][0]
						f2 = log[int(process[2])][0]
						files = [f1, f2]
						merge(files)
					
					elif(process[0].find("replicate") != -1):
						print("replicate")
						self.ballotNum[0] = 1
						self.ballotNum[1] = siteNum
						self.propVal[0] = process[1]
						propList = " "
						for i in range(2, len(input_string)):
							propList += input_string[i]
							propList += " "
						self.propVal[1] = propList
						self.leader = True
						prepSend = "prepare" + str(self.ballotNum[0]) + " " + str(self.balltNum[1]) + "*"
						for c in outgoingTCP.keys():
							if(c != "cli"):
								sock = outgoingTCP.get(c)
								sock.sendall(prepSend.encode())
					
					elif(process[0].find("stop") != -1):
						print("stop")
						stop = True
						for c in outgoingTCP.keys():
							if(c == "cli"):
								sock = outgoingTCP.get(c)
								sock.sendall("process stopped".encode())
	
					
					elif(process[0].find("prepare") != -1):
						print("prepare")
						ballot = int(process[1]) 
						#ballodID
						siteNum = process[2] 
						#id for the siteNum
						
						if(self.ballotNum[0] < ballot or (self.ballotNum[0] == ballot and self.ballotNum[1] < int(siteNum))):
							self.ballotNum[0] = ballot 
							self.ballotNum[1] = siteNum
							prepSend = "ack" + str(self.ballotNum[0]) + " " + str(self.ballotNum[1])
							sock = outgoingTCP.get(siteNum)
							sock.sendall(prepSend.encode())
					
					elif(process[0].find("ack") != -1):
						print("acknowledge")
						balNum = [process[1], process[2]]
						acceptBal = [process[3], process[4]]
						acceptVal = [process[5], process[6]]
						rcvsiteNum = process[7]
						thisAck = [balNum, acceptBal, acceptVal, rcvsiteNum]
						self.acklist.append(thisAck)
						if(len(self.ackList) + 1 >= 2):
							#if majority of acks
							if(acknowledgeCheck(self.ackList)):
								#if yes and there is a value
								self.acceptVal = highestBallot(self.ackList)[:]
							else:
								self.acceptVal = self.propVal[:]
							for c in outgoingTCP.keys():
								if( c != "cli"):
									sock = outgoingTCP.get(c)
									prepSend = "accept" + str(self.ballotNum[0]) + " " + str(self.ballotNum[1]) + " " + self.acceptVal[0] + " " + self.acceptVal[1] + "*"
									sock.sendall(prepSend.encode())
					
					elif(process.find("accept") != -1):
						print(accepted!)
						bal = str(process[1]) + str(process[2])
						if(self.accepts[bal] >= 1 and self.leader):
							print("now deciding value...")
							log.append([self.acceptVal[0], self.acceptVal[1]])
							backupLog.append([self.acceptVal[0], self.acceptVal[1]])
							prepSend = "decide" + str(self.acceptVal[0]) + " " + str(self.acceptVal[1]) + "*"
							for c in outgoingTCP.keys():
								if(c != "cli"):
									sock = outgoingTCP.get(c)
									sock.sendall(prepSend.encode())
								else:
									time.sleep(1)
									prepSend: "Paxos winner is " + str(self.acceptVal[0])
									sock = outgoingTCP.get(c)
									sock.sendall(prepSend.encode())
							print("reinitializing paxos ballot values")
							self.reinit()
							accepts.clear()
							#The above functions are restarting paxos values, and clearing our accepted channels
							for c in incomingTCP.keys():
								sock = channels.get(c)
								ready = select.select([sock], [], [], 1)
								if(ready[0]):
									data = sock.recv(1024).decode()
							return

						elif(int(self.ballotNum[0]) < int(process[1]) or (int(self.ballotNum[0]) == int(process[1]) and int(self.ballotNum[1]) <= int(process[2]))):
							#this is the case in case if our ballot is less than other ones
							propList = ""
							for i in range(4,len(process)):
								propList += process[i]
								propList += " "
							self.ballotNum[0] = int(process[1])
							self.ballotNum[1] = int(process[2])
							self.acceptBal[0] = int (process[1])
							self.acceptBal[1] = int (process[2])
							acceptVal = [process[3], propList]
							self.acceptVal = accVal[:]
							self.leader = False
							#you aren't the leader now
							if(bal in accepts):
								accepts[bal] += 1
								print("accepts have been incremented")
								#testing print above
							else:
								accepts[bal] = 1
								print("accepts is 1")
								#if not in accepts, init it to 1
								prepSend = "accept" + str(process[1]) + " " + str(process[2]) + " " + str(process[3]) + " " + propList + "*"
								for c in outgoingTCP.keys():
									if(c != "cli"):
										sock = outgoingTCP.get(c)
										sock.sendall(prepSend.encode())

	
					
					elif(process[0].find("decide") != -1):
						propList = ""
						for i in range(2 , len(process)):
							propList += process[i]
							propList += " "
						acceptVal = [process[1], process[2]]
						log.append(acceptVal)
						backupLog.append(acceptVal)
						accepts.clear()
						sys.stdout.write("printing prm's log:")
						print(log)
						for c in outgoingTCP.keys():
							if(c == "cli" and self.propVal[0] != None):
								time.sleep(2)
								prepSend = "Winner paxos value is " + str(process[1])
								sock = outgoingTCP.get(c)
								sock.sendall(prepare.encode())
						self.reinit
						for c in incomingTCP.keys():
								sock = channels.get(c)
								ready = select.select([sock], [], [], 1)
								if(ready[0]):
									data = sock.recv(1024).decode()
							return
					else:
						continue
			return


test = PRM()

#Create the server
port = 5005
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

siteNum = sys.argv[1]
setup = sys.argv[2]
print("Esablishing connection!")
with open(setup) as f:
	numSites = f.readline().strip() 
	for i in range(int(numSites)):
		line = f.readline().strip().split()
		siteInfo.append([data for data in line])

	#server.bind(('', int(siteInfo[int(siteNum) -1][1])))
	server.bind(("0.0.0.0", port))
	#use the 2nd one for euca
	server.listen(10)

	for line in f.readlines():
		nums = line.strip().split()
		if(nums[0] == siteNum):
			ip = siteInfo[int(nums[1]) -1][0]
			port = siteInfo[int(nums[1])-1][1]
			test.p = int(port)
			s = socket(AF_INET, SOCK_STREAM)
			addr = (ip, int(port))
			time.sleep(10)
			print(addr)
			run = True
                        while run:
			    try:
		            	s.connect(addr)
				print("Connected to ", nums[1])
				run = False
			    except error:
			    	time.sleep(5)
			outgoingTCP[nums[1]] = s
		if(nums[1] == siteNum):
			connect, addr = server.accept()
			#addr = server.accept()
			incomingTCP[nums[0]] = connect

#Receiving connection from the CLI

connect, addr = server.accept()
incomingTCP["cli"] = connect 
#print(connect)
#print(addr)
#print(incomingTCP)

#Opening a connection with the CLI
s = socket(AF_INET, SOCK_STREAM)
cli_port = int(test.p) - 4 
address = ("127.0.0.1", cli_port)
time.sleep(10)
keep_going = True
while keep_going:
    try:
        s.connect(address)
        keep_going = False
    except error:
        time.sleep(5)
        keep_going = True
outgoingTCP["cli"] = s
#print(outgoingTCP)

print("Ready for commands")
while(True):
    test.receive(incomingTCP)
    #time.sleep(1)