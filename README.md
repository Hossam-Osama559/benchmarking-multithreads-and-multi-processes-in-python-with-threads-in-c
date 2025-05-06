simple listining socket that will each new connection it spin off 
a new thread in c and new thread or new process in python 
and the function that resposible of handling the connection in all cases 
just print simple string in the terminal "|" and update the cursor to make the printing vertical 
and making a dummy loop that just iterate for one billion iteration to mimic a cpu bound function 

and a seprate function that checks all the connections that at specific cursor position it quit and the whole program exit 

in c when making a new thread for each connection and thread for the function that checks the possitions of cursors 
and spin a cmd command to fire 9 cmds each with a connection using net cat "for /l %i in (0,1,8) do start cmd -c /k "nc localhost 5000""

it took 335 second to finish (refer to the img dir in the repo )

in python when making the same thing but using process not threads each connection took the 
first step "|" and still wainting for the second 


and not waiting for a better timing from the threads with all the restrcitions of the GIL .....

