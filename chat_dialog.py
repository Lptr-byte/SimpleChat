from PyQt5.QtGui import QPainter, QFont, QStaticText, QPen, QColor, QBrush, QTextOption, QFontMetrics
from PyQt5.QtCore import QPointF, QRect, Qt

class ChatDialog():
    def __init__(self, qp: QPainter, y0: float, sender: str, time_: str, message: str, is_myself: bool):
        self.qp = qp
        self.is_myself = is_myself
        self.y0 = y0
        self.sender = sender
        self.time_ = time_
        self.message = message
        self.title_font_size = 12
        self.text_font_size = 15
        self.padding = 10
        self.cavans_width = 640
        self.formatMessage()

    def formatMessage(self):
        font = QFont()
        font.setPointSize(self.text_font_size)
        metrics = QFontMetrics(font)
        #x即单行文字最大数量 y即行数 - 1
        x = int(((.8 * self.cavans_width) / self.text_font_size) - 1)
        y = 0
        start = 0

        format_message = []
        t = ''
        for i in range(len(self.message)):
            c = self.message[i]
            if metrics.width(t + c) >= x * self.text_font_size:
                format_message.append(self.message[start:i])
                start = i
                t = ''
                y += 1
            t += c

        format_message.append(self.message[start:])


        self.message = ''
        for i in range(len(format_message)):
            self.message += format_message[i] + '\n'

        self.cows = x
        self.lines = y + 1
        
    def draw(self):
        font = QFont()
        pen = QPen()
        brush = QBrush(Qt.SolidPattern)
        title_color = QColor(0, 249, 26, 255) 
        rect_color = QColor(0, 0, 0, int(255 * .28))
        text_color = QColor(255, 255, 255, 255)

        if self.is_myself:
            x0 = self.cavans_width - self.padding
        else:
            x0 = self.padding
            
        rect = QRect(x0, self.y0 + self.padding + self.title_font_size, 
                     self.text_font_size * (self.cows + 1),
                     self.text_font_size * (self.lines + 1) + (self.lines - 1) * 5)

        #绘制发送者信息及时间信息
        font.setPointSize(self.title_font_size)
        self.qp.setFont(font)
        pen.setColor(title_color)
        self.qp.setPen(pen)
        sender_info = QStaticText(f'{self.sender} [{self.time_}]')
        self.qp.drawStaticText(QPointF(x0, self.y0), sender_info)

        #设置气泡框画笔及画刷
        font.setPointSize(self.text_font_size)
        self.qp.setFont(font)
        pen.setColor(rect_color)
        self.qp.setPen(pen)
        brush.setColor(rect_color)
        self.qp.setBrush(brush)

        #获取文本框大小
        flags = Qt.TextWordWrap
        metrics = QFontMetrics(font)
        word_rect = metrics.boundingRect(rect, flags, self.message) #获取文本框矩形
        font_h = metrics.height()

        #绘制气泡框
        rect.setRect(word_rect.x(), word_rect.y(), word_rect.width(), word_rect.height())
        rect.setWidth(rect.width() + font_h)
        self.qp.drawRoundedRect(rect, 15, 10)

        #绘制文本
        pen.setColor(text_color)
        self.qp.setPen(pen)
        word_rect.setY(word_rect.y() + int(font_h / 2))
        word_rect.setX(word_rect.x() + int(font_h / 2))
        word_rect.setWidth(word_rect.width() + int(font_h / 2))
        self.qp.drawText(word_rect, flags, self.message)

    
    def getInfo(self):
        font = QFont()
        font.setPointSize(self.text_font_size)
        x0 = self.padding
        rect = QRect(x0, self.y0 + self.padding + self.title_font_size, 
                     self.text_font_size * (self.cows + 1),
                     self.text_font_size * (self.lines + 1) + (self.lines - 1) * 5)
        flags = Qt.TextWordWrap
        metrics = QFontMetrics(font)
        word_rect = metrics.boundingRect(rect, flags, self.message) #获取文本框矩形
        rect.setRect(word_rect.x(), word_rect.y(), word_rect.width(), word_rect.height())
        rect.setWidth(rect.width() + metrics.height())
        font.setPointSize(self.title_font_size)
        metrics = QFontMetrics(font)
        return (rect.height(), metrics.height())
