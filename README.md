# asg3

Overall goal: 
We tried very hard to make the code as dynamic as possible, so if there will be any changes it can be easily changed. We've accomplished this by implementing a single mapper function, rather than hard coding 2 servers. We also did this by making various helper functions that can be altered for future uses.

Notes about CLI:  
relies on passing messages using * as the delimiter. Commands with multiple parts separate args with '|'  
For example: cli would pass stop to the PRM as stop*  
	
      relies on receiving ack or nack to determine whether success was achieved!   
      if any of the messages are confusing in terms of format, look at the wait_response function at the end and
      the commands function.  
 
Notes about PRM:
 
For the most part works by receiving the message from the CLI, and detemining whether it was receieved by Cli
or not. If it was it'll be outputting to all nodes minus CLI. Once it receieves a command, it'll process the command
in the PRM. It then does paxos through prepare, ack, accept and a decide function to determine which value will be the agreed upon value.  

EUC Changes: We've changed our setup files in order to be binded towards the proper Euca private IP addresses. 


How to run: 

python PRM.py $1 $2&
python mapper.py 5002 5001 1&
python mapper.py 5003 5001 2&
python reducer.py 5004 5001&
python CLI.py

or in this case we've provided a script that runs it for you. Therefore the correct way to run it is:

./run.sh [id] setup[id].txt




Example:
./run.sh 1 setup1.txt


