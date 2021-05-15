import sys 
import os
import socket
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import threading
server = socket.socket()


connection = None



class MainWindow(QWidget):
    def __init__(self):
        self.count = False
        super().__init__()
        self.msg_ls = []
        self.temp_snd_msg = ''
        loadUi('server_chat_GUI/form.ui',self)
        self.setWindowTitle('server')
        self.snd_btn.clicked.connect(self.onsendcl)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_msg)
        self.timer.start(100)
        self.Start_server_btn.clicked.connect(self.close_server)
        self.show()        

    def onsendcl(self):
        self.temp_snd_msg = self.send_text.text()
        server.send(self.temp_snd_msg.encode())
        self.msg_ls.append(f'{self.temp_snd_msg} : You \n')
        
    
    def close_server(self): 
        self.count = True
        # print(self.count)
    def update_msg(self):
        if len(self.msg_ls) != 0:
            self.result = ''
            for i in self.msg_ls:
                self.result += i
            self.send_rec_msg.setText(self.result)

class  server_thread():
    def __init__(self, window):
        self.window = window
        port = 23453
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        server.bind(('127.0.1.1', port))
        server.listen(5)
        print("server is listening")
        # print(window.count)
        global connection
        connection, addr = server.accept()
        print(f"Got connection from {addr}") 
        while True:
            msg = connection.recv(1024).decode()
            print(msg)
            if msg == 'END':
                server.close()
                break
            window.msg_ls.append(f'client : {msg} \n')
         

app = QApplication([])
window = MainWindow()

server_t = threading.Thread(target=server_thread, args=[window])


server_t.start()

print(f"exit {window.count}")

app.exec_()
server.close()


