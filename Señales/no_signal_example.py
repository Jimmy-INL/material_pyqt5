from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QPixmap
from time import sleep
from random import randint, uniform
from math import pi, cos, sin


class Food(QThread):

    def __init__(self, parent, x, y, max_width, max_height):
        """
        Un Character es un QThread que movera una imagen
        en una ventana. El __init__ recibe los parametros:
            parent: ventana
            x e y: posicion inicial en la ventana
            wait: cuantos segundos esperar
                antes de empezar a mover su imagen
        """
        super().__init__()
        # Guardamos el path de la imagen que tendrá el Label
        self.food_image = "assets/{}.png".format(randint(1, 9))
        # Creamos el Label y definimos su tamaño
        self.label = QLabel(parent)
        self.label.setGeometry(x, y, 50, 50)
        self.label.setPixmap(QPixmap(self.food_image))
        self.label.setScaledContents(True)
        self.label.show()
        self.label.setVisible(True)
        # Seteamos la posición inicial y la guardamos para usarla como una property
        self.__position = (0, 0)
        self.position = (x, y)
        self.direction_angle = uniform(0, 2 * pi)
        self.radio = randint(1, 3)
        #Guardamos los limites de la ventana para que no pueda salirse de ella
        self.max_width = max_width
        self.max_height = max_height
        self.start()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.label.move(self.position[0], self.position[1])

    def run(self):

        while True:
            sleep(0.1)
            new_x = self.position[0] + cos(self.direction_angle) * self.radio
            new_y = self.position[1] + sin(self.direction_angle) * self.radio
            if (new_x > self.max_width - self.label.width() or new_x < 0
                or new_y <0 or new_y > self.max_height - self.label.height()):
                self.direction_angle += pi
                new_x = self.position[0] + cos(
                    self.direction_angle) * self.radio
                new_y = self.position[1] + sin(
                    self.direction_angle) * self.radio
            self.position = (new_x, new_y)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.titulo = QLabel(self)
        self.titulo.setText("Ejemplo")
        self.titulo.move(160, 10)
        self.titulo.show()
        self.setGeometry(100, 100, 1200, 800)
        self.show()

        # Contador de cuanta comida hemos creado
        self.food_created = 0

        # Creamos un Timer que se encargara de crear la comida
        self.food_creator_timer = QTimer(self)
        self.food_creator_timer.timeout.connect(self.food_creator)
        self.food_creator_timer.start(randint(50, 300))

        self.foods = []

    def food_creator(self):
        new_food = Food(parent=self, x=self.width() // 2, y=self.height() // 2,
                        max_width=self.width(), max_height=self.height())
        self.foods.append(new_food)
        self.food_created += 1
        print("Has creado {} unidades de comida\n".format(self.food_created))

if __name__ == '__main__':
    app = QApplication([])
    ex = MyWindow()
    app.exec_()
