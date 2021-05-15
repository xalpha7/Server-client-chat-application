import sys 
import os
import socket
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import threading

client = None

class MainWindow(QWidget):
    def __init__(self, client):
        self.client = client
        super().__init__()
        self.activate = True
        self.msg_ls = []
        loadUi('form.ui',self)
        self.setWindowTitle('Client')
        self.snd_btn.clicked.connect(self.onsendcl)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_msg)
        self.timer.start(100)
        self.Start_client_btn.clicked.connect(self.start_server)
        self.show()        

    def onsendcl(self):
        self.temp_snd_msg = self.send_text.text()
        global client
        client.send(self.temp_snd_msg.encode())
        self.msg_ls.append(f'You : {self.temp_snd_msg} \n')
        self.send_text.setText("")
        

    def start_server(self):
        port = 23447
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        self.client.connect((str(ip), port))
     
        self.msg_ls.append('client is connected to server \n')
        # self.msg_ls.append(f"Connected to server\n")
        self.recieve_message(self.activate)

    def update_msg(self):
        if len(self.msg_ls) != 0:
            self.result = ''
            for i in self.msg_ls:
                self.result += i
            self.send_rec_msg.setText(self.result)

        
    def recieve_message(self, activate):
        def rec(self):
            global client
            while (not activate == False):
                self.msg = client.recv(1024).decode()
                if self.msg == 'END':
                    client.close()
                    break
                self.msg_ls.append(f'client : {self.msg} \n')
            print("server stopped")
        
        rec_thread = threading.Thread(target=rec, args=[self])
    
        rec_thread.start()
    

    

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app = QApplication([])
window = MainWindow(client)
app.exec_()



