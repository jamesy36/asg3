import sys
import socket 
import time
import select

incomingTCP = dict()
outgoingTCP = dict()
sites = []


stop = False #if a process gets stopped it'll be true

class PRM(object):

	def _init_(self, index, id ):
		self.accepts = dict()
		self.ballotNum = [0,0]
		self.ackList = [] #we need to keep track of the acks from other sites
		self.propVal = None #null until a value has been proposed
		self.acceptNum = [0,0]
		self.numVotes = 1
		self.leader = False #starts at false 
		self.acceptVal = None #null until a value has been accepted 
		self.id = id

	def reinit():
		self.accepts.clear()
		self.ballotNum = [0,0]
		self.ackList.clear() #we need to keep track of the acks from other sites
		self.propVal = None #null until a value has been proposed
		self.acceptNum = [0,0]
		self.numVotes = 1
		self.leader = False #starts at false 
		self.acceptVal = None #null until a value has been accepted 
		


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
		for data in the log:
			print(data[0])

	def merge(files)
	#merge cmd implemented
		words = dict()
		for filename in files:
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
				return False

		return True  


	def highestBallot(logs):
		ballotNum = 0
		site = 0
		highest = [0,0]
		for ack in logs:
			if(logs[0][0] > ballotNum or (logs[0][0] == balllotNum and log[0][1] > site)):
				ballotNum = logs[0][1]
				site = logs[0][1]
				highest = [ballotNum, site]

		return highest


	def receive(channels):
		global stop

		for i in channels.keys():
			sock = channels.get(i)
			ready = select.select([sock], [], [], 1)
			if(ready[0]):
				data = sock.recv(1024).decode()
				splitData = data.split("*")
				dataList = splitData[0].split()
				print(dataList)

				if


	def rcvPrep(self, data, channel):



	def rcvAck(self, data, channel):



#either we can do this through messages, or like actual functions idk

	def prepare(self, incomingMessages):


	def resolution()