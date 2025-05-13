# # ----------------------------------------------------------------------------------- generators (take control of suspend and resume execution) 



from colorama import init

import socket  , sys ,time 

begin=time.perf_counter()
init()



thread_id=0
game_over=0
winner=0
thread_cursor_pos=[0,0,0,0,0,0,0,0,0,0]

connections=[]


speed=1000000
space=5
text="|"


def print_vertical(x, y_start, text):
    for i, char in enumerate(text):
       
        sys.stdout.write(f"\033[{y_start + i};{x}H{char}")
        sys.stdout.flush()







def who_is_the_winner():

    global winner 
    global game_over


    for i in range(10):

        if thread_cursor_pos[i]==30:

            winner=i
            game_over=1

            break








def handle_connection_generator(client_sock):
    
    global thread_id
    global game_over
    x=thread_id
    thread_id+=1

    
    while thread_cursor_pos[x]<30 and not game_over:
    
        print_vertical(x*space,thread_cursor_pos[x],text)
        thread_cursor_pos[x]+=1

        for i in range(speed):

            ...
        yield 


    if thread_cursor_pos[x]>=30:

        game_over=1
        winner=x


def set_socket():

    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server_socket.bind(('localhost',5000))

    server_socket.listen(10)
    server_socket.settimeout(0.0003)    

    return server_socket 



if __name__=='__main__':

    print("\033[2J", end="",flush=True)




    server_socket=set_socket()




    while game_over==0 :



        try:
        


            client_sock,client_address=server_socket.accept()

            connections.append(handle_connection_generator(client_sock))
        
        except TimeoutError:

            pass  


        for connection in connections:


            try:

                next(connection)

            except:
                pass 


        # who_is_the_winner()

        


    sys.stdout.write("\033[40;1H")  
    sys.stdout.flush()




    sys.stdout.write(f"here is the champ: thread {winner}")



    sys.stdout.write("\033[50;1H")  
    sys.stdout.flush()


    end=time.perf_counter()

    print(f"{end-begin:.6f}")
