import sys 
import os
import socket
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import threading

connection = None

class MainWindow(QWidget):
    def __init__(self, server):
        self.server = server
        super().__init__()
        self.activate = True
        
        self.msg_ls = []
        loadUi('server_chat_GUI/form.ui',self)
        self.setWindowTitle('server')
        self.snd_btn.clicked.connect(self.onsendcl)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_msg)
        self.timer.start(100)
        self.Start_server_btn.clicked.connect(self.start_server)
        self.close_server_btn.clicked.connect(self.stop_server)
        self.show()        

    def onsendcl(self):
        self.temp_snd_msg = self.send_text.text()
        global connection
        connection.send(self.temp_snd_msg.encode())
        self.msg_ls.append(f'You : {self.temp_snd_msg} \n')
        self.send_text.setText("")
    
    def stop_server(self):
        self.server.close()
        

    def start_server(self):
        global connection 
        port = 23447
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        self.server.bind((str(ip), port))
        self.server.listen(5)
        
        connection, addr = self.server.accept()
        self.msg_ls.append(f"Got connection\n")
        self.recieve_message(self.activate)

    def update_msg(self):
        self.send_rec_msg.setText('Click to Start Server \n')
        if len(self.msg_ls) != 0:
            self.result = ''
            for i in self.msg_ls:
                self.result += i
            self.send_rec_msg.setText(self.result)

        
    def recieve_message(self, activate):
        def rec(self):
            while (not activate == False):
                self.msg = connection.recv(1024).decode()
                if self.msg == 'END':
                    self.server.close()
                    break
                self.msg_ls.append(f'client : {self.msg} \n')
            print("server stopped")

        
        rec_thread = threading.Thread(target=rec, args=[self])
    
        rec_thread.start()
    

    

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app = QApplication([])
window = MainWindow(server)
app.exec_()



