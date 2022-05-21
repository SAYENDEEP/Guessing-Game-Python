import socket
HEADER = 64
PORT  =  6600
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def sending(message, connection):
    message=message.encode("utf-8")
    length = len(message)
    length = str(length).encode("utf-8")
    length += b" " * (64 - len(length))
    connection.send(length)
    connection.send(message)

    

while True:
    
    message = client.recv(64).decode("utf-8")
    if "GAME ENDED" in message or "Score" in message or 'ERROR' in message:
        print(message)
        input()
        break
    elif 'STARTING' in message:
        print('.......')
    else:
        print(message)
        letter = input("CLIENT: ")
        sending(letter,client)

