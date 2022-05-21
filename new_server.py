# server
import random
import socket
import threading

def sending(message, connection):
    message=message.encode("utf-8")
    length = len(message)
    length = str(length).encode("utf-8")
    length += b" " * (64 - len(length))
    connection.send(length)
    connection.send(message)

def receive(connection):
    rec = connection.recv(64).decode("utf-8")
    if rec:
        rec=int(rec)
        mes = connection.recv(rec).decode("utf-8")
    return mes

HEADER = 64
PORT =  6600
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f"[CONNECTION] {addr} connected")

    conn.send(f"\n Press 'Start Game' to begin\nSERVER: _ _ _ _ _".encode(FORMAT))
    #while True:
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        strt_game = conn.recv(msg_length).decode(FORMAT).strip()
        if strt_game.upper() != 'START GAME':
            conn.send(f"\nERROR STARTING GAME\nPress <Enter> to close".encode(FORMAT))
        else:
            conn.send(f"\nSTARTING GAME NOW....".encode(FORMAT))
            #break



    
    with open('/Users/mtxit/Desktop/untitled folder 4/guess.txt', 'r') as f:
        word_choice = [line.strip() for line in f]
    word_count=random.choice(word_choice)
    line = list(len(word_count)*"_")
    count = 0
    err_mes_1 = 'Input must contain "5" characters'
    err_mes_2 = 'INVALID GUESS'
    print(word_count)
    
    while True:
        conn.send(f"SERVER: {''.join(line)}".encode(FORMAT))
        while True:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                guess = conn.recv(msg_length).decode(FORMAT).strip()
                if guess.upper() == 'STOP':
                    conn.send(f"GAME ENDED".encode(FORMAT))
                    break
                else:
                    while len(guess) != 5:
                        conn.send(f"{err_mes_1}\n{''.join(line)}".encode(FORMAT))
                        msg_length = conn.recv(HEADER).decode(FORMAT)
                        if msg_length:
                            msg_length = int(msg_length)
                            guess = conn.recv(msg_length).decode(FORMAT).strip()
                    if guess.upper() == word_count:
                        count+=1
                        conn.send(f"Your Score: {count}".encode(FORMAT))
                        break
                    else:
                        for i in range(len(guess)):
                            if guess[i] == word_count[i]:
                                line[i] = guess[i]
                                print(line)
                            elif guess[i] in list(word_count):
                                line[i] = guess[i].lower()
                        count+=1
                        conn.send(f"\n{err_mes_2}\nSERVER: {''.join(line)}".encode(FORMAT))
                        line = list(len(word_count)*"_")
        conn.close()
    

     
def start_point():
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn,addr = server.accept()
        thread_con = threading.Thread(target=handle_client, args=(conn,addr))
        thread_con.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("server is starting")
start_point()
