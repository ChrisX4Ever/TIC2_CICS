const int botones[] = {13, 12, 11, 10, 8};  // Pines de los botones
const int leds[] = {2, 3, 4, 5, 6};         // Pines de los LEDs
const int buzzer = 9;                       // Pin del buzzer
const int notas[] = {261, 294, 329, 392, 440}; // Frecuencias en Hz

void setup() {
    for (int i = 0; i < 5; i++) {
        pinMode(botones[i], INPUT_PULLUP); // Activa resistencias internas pull-up
        pinMode(leds[i], OUTPUT);
    }
    pinMode(buzzer, OUTPUT);
}

void loop() {
    bool botonPresionado = false;

    for (int i = 0; i < 5; i++) {
        if (digitalRead(botones[i]) == LOW) {
            botonPresionado = true;
            digitalWrite(leds[i], HIGH);
            tone(buzzer, notas[i]);          // Reproduce la nota correspondiente
            delay(500);                      // Espera 0.5 segundos
            noTone(buzzer);                  // Detiene el sonido
            digitalWrite(leds[i], LOW);      // Apaga el LED

            // Espera a que se suelte el botón antes de continuar
            while (digitalRead(botones[i]) == LOW);
            delay(50); // Pequeño retardo para evitar rebotes
            break; // Evita detectar otros botones durante este ciclo
        }
    }

    if (!botonPresionado) {
        noTone(buzzer); // Asegura que el buzzer esté apagado si no hay pulsaciones
    }
}