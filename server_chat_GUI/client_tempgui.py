import socket
import sys
import threading

client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client has started Start chatting....")
port = 23447
host = socket.gethostname()
ip = socket.gethostbyname(host)
client.connect((str(ip), port))


def Send_msg(client):
    while True:
        # print("sender thread is active")
        send_message = input("enter your messsage :")
        client.send(send_message.encode())
        if send_message == 'END':
            print("-----End communication-----") 
            client.close()
            break  

def rec_msg(client):
    while True:
        # print("reciever thead is active")
        msg = client.recv(1024).decode()
        if msg == 'END':
            print("-----End communication-----") 
            client.close()
            break
        elif msg:
            print("Server: ", msg)


sndthrd = threading.Thread(target=Send_msg, args=[client])
recthrd = threading.Thread(target=rec_msg, args=[client])


recthrd.start()
sndthrd.start()

sys.exit()