import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import convolve2d
import serial
import threading
import time
import random
import pygame

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
        self.img = self.ax.imshow(self.grid, cmap='inferno', interpolation='nearest')
        self.ax.axis('off')

        # Inicialización de Pygame
        pygame.mixer.init()

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)
        self.timer.start(100)

        # Conexión Serial
        self.serial_port = serial.Serial('COM5', 9600, timeout=1)
        self.serial_thread = threading.Thread(target=self.listen_to_arduino, daemon=True)
        self.serial_thread.start()

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
            pygame.mixer.music.load('victory.mp3')
            pygame.mixer.music.play()
            self.reset_grid()

        elif np.all((self.grid == 0) | (self.grid == 2)):
            print("DERROTA: Todas las células son zombies")
            pygame.mixer.music.load('defeat.mp3')
            pygame.mixer.music.play()
            self.reset_grid()

        self.img.set_data(self.grid)
        self.canvas.draw()

    def listen_to_arduino(self):
        while True:
            try:
                if self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode().strip()
                    if line == "r":
                        self.reset_grid()
            except Exception as e:
                print(f"Error leyendo de Arduino: {e}")
            time.sleep(0.1)

    def reset_grid(self):
        self.grid = np.random.choice([0, 1, 2], self.grid_size**2, p=[0.2, 0.5, 0.3]).reshape(self.grid_size, self.grid_size)
        self.life_points = np.random.randint(50, 201, size=(self.grid_size, self.grid_size))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())
