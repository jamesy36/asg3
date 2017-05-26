# asg3
Notes about CLI:  
        relies on passing messages using * as the delimiter. Commands with multiple parts separate args with '|'  
        For example: cli would pass stop to the PRM as stop*  
		   cli would pass merge as: merge|arg1|arg2*  
		   cli would pass replicate as: replicate|file*  
      relies on receiving ack or nack to determine whether success was achieved!   
      if any of the messages are confusing in terms of format, look at the wait_response function at the end and
      the commands function.  
