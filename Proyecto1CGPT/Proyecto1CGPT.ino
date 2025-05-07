#include "Volume.h"
#define TONE_USE_INT
#define TONE_PITCH 440
#include <TonePitch.h>

Volume vol;

const int botones[] = {13, 12, 11, 10, 8};  // Pines de botones
const int leds[] = {2, 3, 4, 7, 9};         // Cambié el LED que estaba en el pin 5 al pin 7
const char* notareal[] = {"Do", "Re", "Mi", "Sol", "La"};

const int notasMatrix[3][5] = {
  {NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4},
  {NOTE_A4, NOTE_B4, NOTE_C5, NOTE_D5, NOTE_E5},
  {NOTE_F5, NOTE_G5, NOTE_A5, NOTE_B5, NOTE_C6}
};

int x = 0;       // Fila actual
int y = 255;     // Volumen

void setup() {
  vol.begin(); // ¡Sin parámetros!
  for (int i = 0; i < 5; i++) {
    pinMode(botones[i], INPUT_PULLUP);
    pinMode(leds[i], OUTPUT);
  }
  Serial.begin(9600);
  Serial.println("Sistema iniciado. Esperando comandos...");
}

void loop() {
  procesarBotones();
  procesarComando();
}

void procesarBotones() {
  for (int i = 0; i < 5; i++) {
    if (digitalRead(botones[i]) == LOW) {
      for (int j = 0; j < 5; j++) digitalWrite(leds[j], LOW);
      digitalWrite(leds[i], HIGH);

      vol.tone(notasMatrix[x][i], (byte)y);
      Serial.print("Volumen Seteado: ");
      Serial.print(y);
      Serial.print(" Botón Presionado: ");
      Serial.print(i + 1);
      Serial.print(". Nota: ");
      Serial.println(notareal[i]);

      vol.delay(300);
      vol.noTone();
      digitalWrite(leds[i], LOW);

      while (digitalRead(botones[i]) == LOW);
        delay(100);
        break;
    }
  }
}

void procesarComando() {
  if (Serial.available()) {
    String a = Serial.readStringUntil('\n');
    a.trim();

    if (a.charAt(0) == 'T') {
      int nuevoX = a.substring(1).toInt();
      if (nuevoX >= 0 && nuevoX < 3) {
        x = nuevoX;
        Serial.print("Fila de notas cambiada a: ");
        Serial.println(x);
      } else {
        Serial.println("Error: Fila fuera de rango (0-2)");
      }
    }
    else if (a.charAt(0) == 'V') {
      int nuevoY = a.substring(1).toInt();
      if (nuevoY >= 0 && nuevoY <= 255) {
        y = nuevoY;
        Serial.print("Volumen actualizado a: ");
        Serial.println(y);
      } else {
        Serial.println("Error: Volumen fuera de rango (0-255)");
      }
    }
    else {
      Serial.println("Comando inválido. Use T0-T2 o V000-V255");
    }
  }
}