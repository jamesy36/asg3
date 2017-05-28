# asg3
Notes about CLI:  
relies on passing messages using * as the delimiter. Commands with multiple parts separate args with '|'  
For example: cli would pass stop to the PRM as stop*  
	
      relies on receiving ack or nack to determine whether success was achieved!   
      if any of the messages are confusing in terms of format, look at the wait_response function at the end and
      the commands function.  
 
Notes about PRM:
 
For the most part works by receiving the message from the CLI, and detemining whether it was receieved by Cli
or not. If it was it'll be outputting to all nodes minus CLI. Once it receieves a command, it'll process the command
in the PRM. It then does paxos through prepare, ack, and accept. 

How to run: 

To run PRM: ./PRM [siteInfo] setup.txt
To run CLI: ./cli [nodePort] [prmPort]

When you start the program, the sites begin connecting to each other, which takes some time for the connections to connect.
However once these connections are made, the program will let users know that the PRM can begin taking inputs and commands.

It's imperative that you  run the PRM first, and make sure to run the CLI  only after all of the PRMs have connected to each other. The CLIs listen on a port number that is 5 greater than the port number of its corresponding PRM. 


Example:
./PRM 1 setup.txt 
./PRM 2 setup.txt 
./PRM 3 setup.txt 


./cli 5006 5001
./cli 5007 5002
./cli 5008 5003


NOTE:it's not working due to errors, I've been debuggin all day but then I saw the piazza that said 
you'd just check through code if it doesn't work and I'd rather just submit what we have now. 


