from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap
from time import sleep
from random import randint


class MoveMyImageEvent:
    """
    Las instancias de esta clase
    contienen la informacion necesaria
    para que la ventana actualice
    la posicion de la imagen
    """
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class Food(QThread):
    trigger = pyqtSignal(MoveMyImageEvent)

    # pyqtSignal recibe *args que le indican
    # cuales son los tipos de argumentos que seran enviados
    # en este caso, solo se enviara un argumento:
    #   objeto clase MoveMyImageEv

    def __init__(self, parent, x, y, max_width, max_height):
        """
        Un Food es un QThread que movera una imagen de comida
        en una ventana. El __init__ recibe los parametros:
            parent: ventana
            x e y: posicion inicial en la ventana
        """
        super().__init__()
        self.life = 100
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
        # Guardamos los limites de la ventana para que no pueda salirse de ella
        self.max_width = max_width
        self.max_height = max_height
        self.start()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

        # El trigger emite su señal a la ventana cuando cambiamos la posición
        self.trigger.emit(MoveMyImageEvent(
            self.label, self.position[0], self.position[1]
        ))


    def run(self):

        while self.life > 0:
            self.life -= 1
            sleep(0.1)
            new_x = self.position[0] + 1
            if new_x > self.max_width:
                new_x = randint(0, self.max_width)
            new_y = self.position[1] + 1
            if new_y > self.max_height:
                new_y = randint(0, self.max_height)
            self.position = (new_x, new_y)
        self.quit()
        self.label.deleteLater()


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
        self.food_creator_timer.start(50)

        self.foods = []

    def food_creator(self):
        new_food = Food(parent=self, x=randint(0, self.width()),
                        y=randint(0, self.height()), max_width=self.width(),
                        max_height=self.height())
        new_food.trigger.connect(self.actualizar_imagen)
        self.foods.append(new_food)
        self.food_created += 1
        print("Has creado {} unidades de comida\n".format(self.food_created))

    @staticmethod
    def actualizar_imagen(myImageEvent):
        # Recibo el objeto con la información necesaria para mover a la comida
        label = myImageEvent.label
        label.move(myImageEvent.x, myImageEvent.y)


if __name__ == '__main__':
    app = QApplication([])
    ex = MyWindow()
    app.exec_()
