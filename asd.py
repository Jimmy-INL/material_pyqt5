import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):
        self.setGeometry(300, 100, 225, 450)
        self.setMaximumHeight(450)
        self.setMaximumWidth(225)
        self.setWindowTitle('Move Event')
        self.azul_h = True
        self.verde_h = True
        self.label1 = QLabel('AZUL', self)
        self.label1.move(0, 0)
        self.label1.setGeometry(QRect(0, 0, 225, 225))  # (x, y, height, width)
        self.label2 = QLabel('VERDE', self)
        self.label2.move(0, 0)
        self.label2.setGeometry(QRect(0, 225, 225, 225))
        self.pixmap_azul = QPixmap('images/colors/azul.png')
        self.pixmap_verde = QPixmap('images/colors/verde.png')
        self.label1.setPixmap(self.pixmap_azul)
        self.label2.setPixmap(self.pixmap_verde)
        self.label1.show()
        self.label2.show()
        self.show()

    def mousePressEvent(self, event):
        if event.y() <= 225:
            if self.azul_h:
                self.label1.hide()
                self.azul_h = False
            else:
                self.label1.show()
                self.azul_h = True
        else:
            if self.verde_h:
                self.label2.hide()
                self.verde_h = False
            else:
                self.label2.show()
                self.verde_h = True


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())
