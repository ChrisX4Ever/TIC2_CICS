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

class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self)  # Asegúrate de que el archivo UI se llama interface.ui

        self.speedSlider.valueChanged.connect(self.on_slider_value_changed)

        self.grid_size = 100
        self.grid = np.random.choice([0, 1], self.grid_size**2, p=[0.8, 0.2]).reshape(self.grid_size, self.grid_size)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout = QVBoxLayout(self.findChild(QWidget, "plotWidget"))
        layout.addWidget(self.canvas)

        self.img = self.ax.imshow(self.grid, interpolation='nearest')
        self.ax.axis('off')

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)
        self.timer.start(self.speedSlider.value() * 100)  # Actualiza cada 100 ms

        self.serial_port = serial.Serial('COM5', 9600, timeout=1)  # Cambia COM3 si es necesario
        self.serial_thread = threading.Thread(target=self.listen_to_arduino, daemon=True)
        self.serial_thread.start()

        self.serial_timer = QTimer()
        self.serial_timer.timeout.connect(self.send_alive_cells_to_arduino)
        self.serial_timer.start(10000)  # Cada 10 segundos

    def on_slider_value_changed(self, value):
        gameSpeed = value * 100
        self.timer.setInterval(500 - gameSpeed)
        print(500 - gameSpeed)

    def update_grid(self):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

        convolved = convolve2d(self.grid, kernel, mode='same', boundary='fill')
        birth = (convolved == 3) & (self.grid == 0)
        survive = ((convolved == 2) | (convolved == 3)) & (self.grid == 1)
        self.grid[:, :] = 0
        self.grid[birth | survive] = 1

        self.img.set_data(self.grid)
        self.canvas.draw()

    def send_alive_cells_to_arduino(self):
        if self.serial_port.is_open:
            alive_cells = int(np.sum(self.grid))
            print(f"Enviando comando a Arduino: {alive_cells}")
            self.serial_port.write(f"{alive_cells}\n".encode())

    def listen_to_arduino(self):
        while True:
            try:
                if self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode().strip()
                    if line == "RESET":
                        self.reset_grid()
            except Exception as e:
                print(f"Error leyendo de Arduino: {e}")
            time.sleep(0.1)

    def reset_grid(self):
        self.grid = np.random.choice([0, 1], self.grid_size**2, p=[0.8, 0.2]).reshape(self.grid_size, self.grid_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())
