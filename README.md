# asg3
Notes about CLI:  
        relies on passing messages using * as the delimiter. Commands with multiple parts separate args with '|'  
        For example: cli would pass stop to the PRM as stop*  
		   cli would pass merge as: merge|arg1|arg2*  
		   cli would pass replicate as: replicate|file*  
      relies on receiving ack or nack to determine whether success was achieved!   
      if any of the messages are confusing in terms of format, look at the wait_response function at the end and
      the commands function.  
      
 Notes about PRM:
 
For the most part works by receiving the message from the CLI, and detemining whether it was receieved b Clii
or not. If it was it'll be outputting to all nodes minus CLI. Once it receieves a command, it'll process the command
in the PRM. It then does paxos through prepare, ack, and accept. 
