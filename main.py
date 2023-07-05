import sys
import json
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter, QPixmap, QColor

import main_window
from client_server import ClientServer
from chat_dialog import ChatDialog


c = ClientServer()


class MainWidget(QWidget):
    global c
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(800,480)
        self.ui = main_window.Ui_MainWidget()
        self.ui.setupUi(self)
        self.initFile()
        self.pixmap = QPixmap(640, 420)
        self.pixmap.fill(QColor(1, 1, 1, 0))
        self.ui.ChatArea.setPixmap(self.pixmap)
        update_draw = threading.Thread(target=self.updateDraw)
        update_draw.daemon = True
        update_draw.start()

    def initFile(self):
        c.lock.acquire()
        try:
            with open('./messages.json', 'w') as f:
                list = []
                json.dump(list, f, indent=4)
        finally:
            c.lock.release()

    @pyqtSlot()
    def on_SendButton_clicked(self):
        msg = self.ui.InputBox.toPlainText()
        time_ = time.strftime('%m-%d %H:%M:%S', time.localtime())
        print(time_)
        self.ui.InputBox.clear()
        if msg == '':
            return
        dict = {'user_name': c.getUserName(), 'state': 'send', 'message': msg, 'time': time_}
        json_dict = json.dumps(dict)
        c.client.send(json_dict.encode())

    @pyqtSlot()
    def on_SettingButton_clicked(self):
        input_dialog = QInputDialog()
        input_dialog.setOkButtonText('就它了')
        input_dialog.setCancelButtonText('再想想')
        input_dialog.setWindowTitle('更改用户名')
        input_dialog.setLabelText('请输入要更改的昵称：')
        if input_dialog.exec_():
            with open('./user_info.json', 'w') as f:
                user_name = {'user_name': input_dialog.textValue()}
                json.dump(user_name, f)


    def paintEvent(self, event):
        qp = QPainter(self.ui.ChatArea.pixmap())
        top_line = 410
        #读取json文件中存放的消息
        try:
            c.lock.acquire()
            try:
                with open('./messages.json', 'r') as f:
                    message_list = json.load(f)
                    #print(message_list[-1])
                    for item in reversed(message_list):
                        dia = ChatDialog(qp, 0, item['sender_name'], item['time'], item['message'], False)
                        padding = dia.padding
                        message_height, title_height = dia.getInfo()
                        del(dia)
                        top_line -= (message_height + title_height + padding)
                        dia = ChatDialog(qp, top_line, item['sender_name'], item['time'], item['message'], False)
                        dia.draw()
                        if top_line <= 0:
                            break
            finally:
                c.lock.release()
        except:
            c.lock.acquire()
            try:
                with open('./messages.json', 'w') as f:
                    list = []
                    json.dump(list, f, indent=4)
            finally:
                c.lock.release()

        qp.end()

    def updateDraw(self):
        while True:
            if c.is_draw:
                c.lock.acquire()
                try:
                    self.ui.ChatArea.clear()
                    self.ui.ChatArea.setPixmap(self.pixmap)
                    self.update()
                    c.is_draw = False
                finally:
                    c.lock.release()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window_ = MainWidget()
    main_window_.show()
    sys.exit(app.exec_())