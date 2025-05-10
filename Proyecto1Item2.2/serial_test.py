import serial
import time

try:
    # Ajusta el puerto COM si es necesario
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)  # Esperar un momento para inicializar la comunicación

    # Enviar un comando de prueba
    print("Enviando comando de prueba: p-250")
    arduino.write(b"p-250\n")
    time.sleep(1)

    print("Enviando evento especial: a-1")
    arduino.write(b"a-1\n")
    time.sleep(1)

    print("Enviando evento especial: a-4")
    arduino.write(b"a-4\n")
    time.sleep(1)

    arduino.close()
except Exception as e:
    print(f"Error al comunicar con Arduino: {e}")
