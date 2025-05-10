import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import convolve2d
import serial
import threading
import time
import random

class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self)

        self.speedSlider.valueChanged.connect(self.on_slider_value_changed)

        # Dimensiones de la grilla y configuración inicial
        self.grid_size = 100
        self.grid = np.random.choice([0, 1, 2], self.grid_size**2, p=[0.2, 0.5, 0.3]).reshape(self.grid_size, self.grid_size)
        self.life_points = np.random.randint(50, 201, size=(self.grid_size, self.grid_size))

        # Configuración del gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout = QVBoxLayout(self.findChild(QWidget, "plotWidget"))
        layout.addWidget(self.canvas)
        self.img = self.ax.imshow(self.grid, cmap='inferno', interpolation='nearest')
        self.ax.axis('off')

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)
        self.timer.start(self.speedSlider.value() * 100)

        # Conexión Serial
        self.serial_port = serial.Serial('COM5', 9600, timeout=1)
        self.serial_thread = threading.Thread(target=self.listen_to_arduino, daemon=True)
        self.serial_thread.start()

        # Inicializar reproductor de medios
        self.player = QMediaPlayer()

        # Configuración de botones
        self.init_buttons()

    def on_slider_value_changed(self, value):
        gameSpeed = value * 100
        self.timer.setInterval(500 - gameSpeed)
        print(500 - gameSpeed)

    def update_grid(self):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

        neighbors = convolve2d(self.grid > 0, kernel, mode='same', boundary='fill')
        zombies = convolve2d(self.grid == 0, kernel, mode='same', boundary='fill')
        humans = convolve2d(self.grid == 1, kernel, mode='same', boundary='fill')

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i, j] == 1:  # Humano
                    self.life_points[i, j] -= 5 * zombies[i, j]
                    if self.life_points[i, j] <= 0:
                        self.grid[i, j] = 0
                        self.life_points[i, j] = 100

                elif self.grid[i, j] == 0:  # Zombie
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

                elif self.grid[i, j] == 2:  # Muerto
                    if humans[i, j] >= 2 and zombies[i, j] < 2:
                        self.grid[i, j] = 1
                        self.life_points[i, j] = 100
                    elif zombies[i, j] >= 2:
                        self.grid[i, j] = 0
                        self.life_points[i, j] = 100

        # Verificar condiciones de victoria o derrota
        if np.all((self.grid == 1) | (self.grid == 2)):
            print("VICTORIA: Todas las células son humanas")
            self.play_sound('victory.wav')  # Usando QMediaPlayer
            self.reset_grid()

        elif np.all((self.grid == 0) | (self.grid == 2)):
            print("DERROTA: Todas las células son zombies")
            self.play_sound('defeat.wav')  # Usando QMediaPlayer
            self.reset_grid()

        self.img.set_data(self.grid)
        self.canvas.draw()

    def listen_to_arduino(self):
        while True:
            try:
                if self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode().strip()
                    print(f"📡 Recibido desde Arduino: {line}")  # <-- Esto imprime lo recibido

                    if line == "r":
                        self.reset_grid()
                    elif line == "e1":
                        print("🔥 Infección Masiva Activada desde Arduino")
                        self.infeccion_masiva()
                    elif line == "e2":
                        print("🧬 Infección Masiva Mutada Activada desde Arduino")
                        self.infeccion_masiva_mutada()
                    elif line == "e3":
                        print("🔄 Ritual de Purificación Activado desde Arduino")
                        self.ritual_purificacion()
                    elif line == "e4":
                        print("💥 I am Atomic Activado desde Arduino")
                        self.i_am_atomic()

        except Exception as e:
            print(f"Error leyendo de Arduino: {e}")
        time.sleep(0.1)


    def init_buttons(self):
        # Asignar eventos a los botones de la interfaz gráfica
        self.a_1.clicked.connect(self.infeccion_masiva)
        self.a_2.clicked.connect(self.infeccion_masiva_mutada)
        self.a_3.clicked.connect(self.ritual_purificacion)
        self.a_4.clicked.connect(self.i_am_atomic)

        # Configuración de botones físicos conectados al Arduino
        self.button_pin_12 = 12
        self.button_pin_11 = 11
        self.button_pin_10 = 10
        self.button_pin_8 = 8

        self.serial_port.write(b'B')  # Enviar señal inicial a Arduino

    def infeccion_masiva(self):
        print("⚠️ Infección Masiva Activada")
        x, y = random.randint(0, self.grid_size - 5), random.randint(0, self.grid_size - 5)
        self.grid[x:x + 5, y:y + 5] = 0  # 5x5 zombies con 200 puntos de vida
        self.life_points[x:x + 5, y:y + 5] = 200
        self.img.set_data(self.grid)
        self.canvas.draw()

    def infeccion_masiva_mutada(self):
        print("🧟‍♂️ Infección Masiva Mutada Activada")
        x, y = random.randint(0, self.grid_size - 13), random.randint(0, self.grid_size - 13)
        # Forma pulsar de 13x13
        self.grid[x:x + 13, y:y + 13] = 0
        self.life_points[x:x + 13, y:y + 13] = 200
        self.img.set_data(self.grid)
        self.canvas.draw()

    def ritual_purificacion(self):
        print("🔮 Ritual de Purificación Activado")
        x, y = random.randint(0, self.grid_size - 15), random.randint(0, self.grid_size - 15)
        for i in range(x, x + 15):
            for j in range(y, y + 15):
                if self.grid[i, j] == 0:  # Si es un zombie
                    if random.random() < 0.8:  # 80% de probabilidad de curarse
                        self.grid[i, j] = 1  # Pasa a ser humano
                        self.life_points[i, j] = 200
        self.img.set_data(self.grid)
        self.canvas.draw()

    def i_am_atomic(self):
        print("💣 I am Atomic! Activado")
        x, y = random.randint(0, self.grid_size - 25), random.randint(0, self.grid_size - 25)
        self.grid[x:x + 25, y:y + 25] = 2  # Área de 25x25 completamente destruida
        self.life_points[x:x + 25, y:y + 25] = 100
        self.img.set_data(self.grid)
        self.canvas.draw()

    def reset_grid(self):
        self.grid = np.random.choice([0, 1, 2], self.grid_size**2, p=[0.2, 0.5, 0.3]).reshape(self.grid_size, self.grid_size)
        self.life_points = np.random.randint(50, 201, size=(self.grid_size, self.grid_size))

    def play_sound(self, sound_file):
        """Reproducir sonido usando QMediaPlayer"""
        sound = QMediaContent(QUrl.fromLocalFile(sound_file))
        self.player.setMedia(sound)
        self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())