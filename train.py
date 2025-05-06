

# # ----------------------------------------------------------------------------------- threads 


from multiprocessing import Process , Value ,Array

from colorama import init

import socket ,threading , sys ,time 

begin=time.perf_counter()
init()



# global variables for the mutli threads 
thread_id=0
game_over=0
winner=0
thread_cursor_pos=[0,0,0,0,0,0,0,0,0,0]



speed=1000000000
space=5
text="|"


def print_vertical(x, y_start, text):
    for i, char in enumerate(text):
       
        sys.stdout.write(f"\033[{y_start + i};{x}H{char}")
        sys.stdout.flush()






def who_is_the_winer_process(thread_cursor_pos,winner,game_over):

    while True:



        for i in range(5):

            if thread_cursor_pos[i]==30:

                winner.value=i
                game_over.value=1

                break
        if game_over.value:
            break


def who_is_the_winer_thread():

    global winner 
    global game_over

    while True:



        for i in range(5):

            if thread_cursor_pos[i]==30:

                winner=i
                game_over=1

                break
        if game_over:
            break















def handle_connections_thread(client_sock):
    
    global thread_id
    global game_over
    x=thread_id
    thread_id+=1

    
    while not game_over:
    
        print_vertical(x*space,thread_cursor_pos[x],text)
        # print(f"process {x}")
        thread_cursor_pos[x]+=1

        for i in range(speed):

            ...
        


def handle_connections_process(client_sock,thread_id,thread_cursor_pos,game_over):
    
 
    x=thread_id.value
    thread_id.value+=1

    
    while not game_over.value:
    
        print_vertical(x*space,thread_cursor_pos[x],text)
        # print(f"process {x}")
        thread_cursor_pos[x]+=1

        for i in range(speed):

            ...
        
    







def set_socket():

    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server_socket.bind(('localhost',5000))

    server_socket.listen(10)
    server_socket.settimeout(1.0)    

    return server_socket 



if __name__=='__main__':

    print("\033[2J", end="",flush=True)









    # shared variables for the multi processes 

    thread_cursor_pos=Array('i',10)

    thread_id=Value("i",0)

    winner=Value("i",0)

    game_over=Value("i",0)





    server_socket=set_socket()


    #  for the multi processes

    check_winer_process=Process(target=who_is_the_winer_process,args=(thread_cursor_pos,winner,game_over,))
    check_winer_process.start()

    # for the mutli threads 

    # check_winer_thread=threading.Thread(target=who_is_the_winer_thread,args=(),daemon=True)
    # check_winer_thread.start()


    while game_over.value==0 :



        try:
        


            client_sock,client_address=server_socket.accept()



            
            #  for the multi processes

            prand_new_process=Process(target=handle_connections_process,args=(client_sock,thread_id,thread_cursor_pos,game_over))
            prand_new_process.start()



            # for the mutli threads 

            # new_thread=threading.Thread(target=handle_connections_thread,args=(client_sock,),daemon=True)
            # new_thread.start()

            
        
        except TimeoutError:

            continue
        


    sys.stdout.write("\033[40;1H")  
    sys.stdout.flush()




    sys.stdout.write(f"here is the champ: thread {winner.value}")



    sys.stdout.write("\033[50;1H")  
    sys.stdout.flush()


    end=time.perf_counter()

    print(f"{end-begin:.6f}")
