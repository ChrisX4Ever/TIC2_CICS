const int botones[] = {7, 8, 9, 10, 11};  // Pines de los botones
const int leds[] = {2, 3, 4, 5, 6};       // Pines de los LEDs
const int buzzer = 12;                    // Pin del buzzer

void setup() {
    for (int i = 0; i < 5; i++) {
        pinMode(botones[i], INPUT_PULLUP); // Activa resistencias internas pull-up
        pinMode(leds[i], OUTPUT);
    }
    pinMode(buzzer, OUTPUT);
}

void loop() {
    for (int i = 0; i < 5; i++) {
        if (digitalRead(botones[i]) == LOW) {  // Botón presionado
            digitalWrite(leds[i], HIGH);  // Enciende LED
            tone(buzzer, 200 + (i * 100)); // Suena una nota diferente
        } else {
            digitalWrite(leds[i], LOW);  // Apaga LED
        }
    }
}
