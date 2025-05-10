import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import convolve2d
import serial
import threading
import time
import random
from matplotlib.colors import ListedColormap


class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self)

        # Dimensiones de la grilla y configuración inicial
        self.grid_size = 100
        self.grid = np.random.choice([0, 1, 2], self.grid_size**2, p=[0.2, 0.5, 0.3]).reshape(self.grid_size, self.grid_size)
        self.life_points = np.random.randint(50, 201, size=(self.grid_size, self.grid_size))

        # Configuración del gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout = QVBoxLayout(self.findChild(QWidget, "plotWidget"))
        layout.addWidget(self.canvas)

        # Colormap personalizado
        colors = ['black', 'white', 'red']  # Zombie -> Negro, Humano -> Blanco, Muerto -> Rojo
        self.cmap = ListedColormap(colors)

        self.img = self.ax.imshow(self.grid, cmap=self.cmap, interpolation='nearest')
        self.ax.axis('off')

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)
        self.default_speed = 200
        self.timer.start(self.default_speed)  # Velocidad inicial

        # Conexión Serial
        self.serial_port = serial.Serial('COM3', 9600, timeout=1)
        self.serial_thread = threading.Thread(target=self.listen_to_arduino, daemon=True)
        self.serial_thread.start()

        # Conexión del slider para controlar la velocidad
        self.speedSlider.valueChanged.connect(self.adjust_speed)

        # Botones de la interfaz gráfica
        self.a_1.clicked.connect(self.infeccion_masiva)
        self.a_2.clicked.connect(self.infeccion_masiva_mutada)
        self.a_3.clicked.connect(self.ritual_purificacion)
        self.a_4.clicked.connect(self.i_am_atomic)

    def adjust_speed(self):
        """
        Ajusta la velocidad del timer en función del valor del slider.
        """
        value = self.speedSlider.value()
        speed = self.default_speed - (value * 10)
        if speed < 50: 
            speed = 50
        print(f"Velocidad ajustada a: {speed} ms por actualización")
        self.timer.setInterval(speed)

    def update_grid(self):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

        neighbors = convolve2d(self.grid > 0, kernel, mode='same', boundary='fill')
        zombies = convolve2d(self.grid == 0, kernel, mode='same', boundary='fill')
        humans = convolve2d(self.grid == 1, kernel, mode='same', boundary='fill')

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i, j] == 1:
                    self.life_points[i, j] -= 5 * zombies[i, j]
                    if self.life_points[i, j] <= 0:
                        self.grid[i, j] = 0
                        self.life_points[i, j] = 100

                elif self.grid[i, j] == 0:
                    if humans[i, j] < 2:
                        self.life_points[i, j] -= 10
                    elif humans[i, j] > 3:
                        self.life_points[i, j] -= 30

                    if self.life_points[i, j] <= 0:
                        if random.random() < 0.1:
                            self.grid[i, j] = 1
                            self.life_points[i, j] = 100
                        else:
                            self.grid[i, j] = 2

                elif self.grid[i, j] == 2:
                    if humans[i, j] >= 2 and zombies[i, j] < 2:
                        self.grid[i, j] = 1
                        self.life_points[i, j] = 100
                    elif zombies[i, j] >= 2:
                        self.grid[i, j] = 0
                        self.life_points[i, j] = 100

        self.img.set_data(self.grid)
        self.canvas.draw()

    def listen_to_arduino(self):
        while True:
            try:
                if self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode().strip()
                    print(f"📡 Recibido desde Arduino: {line}")
                    if line == "r":
                        self.reset_grid()
                    elif line == "e1":
                        self.infeccion_masiva()
                    elif line == "e2":
                        self.infeccion_masiva_mutada()
                    elif line == "e3":
                        self.ritual_purificacion()
                    elif line == "e4":
                        self.i_am_atomic()
            except Exception as e:
                print(f"Error leyendo de Arduino: {e}")
            time.sleep(0.1)

    def infeccion_masiva(self):
        print("🔥 Infección Masiva Activada")
        x, y = random.randint(0, self.grid_size - 5), random.randint(0, self.grid_size - 5)
        self.grid[x:x + 5, y:y + 5] = 0
        self.life_points[x:x + 5, y:y + 5] = 200
        self.img.set_data(self.grid)
        self.canvas.draw()

    def infeccion_masiva_mutada(self):
        print("🧬 Infección Masiva Mutada Activada")
        x, y = random.randint(0, self.grid_size - 13), random.randint(0, self.grid_size - 13)
        self.grid[x:x + 13, y:y + 13] = 0
        self.life_points[x:x + 13, y:y + 13] = 200
        self.img.set_data(self.grid)
        self.canvas.draw()

    def ritual_purificacion(self):
        print("🔄 Ritual de Purificación Activado")
        x, y = random.randint(0, self.grid_size - 15), random.randint(0, self.grid_size - 15)
        for i in range(x, x + 15):
            for j in range(y, y + 15):
                if self.grid[i, j] == 0 and random.random() < 0.8:
                    self.grid[i, j] = 1
                    self.life_points[i, j] = 200
        self.img.set_data(self.grid)
        self.canvas.draw()

    def i_am_atomic(self):
        print("💥 I am Atomic Activado")
        x, y = random.randint(0, self.grid_size - 25), random.randint(0, self.grid_size - 25)
        self.grid[x:x + 25, y:y + 25] = 2
        self.img.set_data(self.grid)
        self.canvas.draw()

    def reset_grid(self):
        self.grid = np.random.choice([0, 1, 2], self.grid_size**2, p=[0.2, 0.5, 0.3]).reshape(self.grid_size, self.grid_size)
        self.life_points = np.random.randint(50, 201, size=(self.grid_size, self.grid_size))
        self.img.set_data(self.grid)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())