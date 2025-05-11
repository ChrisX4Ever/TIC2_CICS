// Definición de pines
const int ledPins[5] = {6, 3, 4, 7, 2};
const int buttonPins[5] = {13, 12, 11, 10, 8};

// Configuración inicial
void setup() {
    Serial.begin(9600);
    for (int i = 0; i < 5; i++) {
        pinMode(ledPins[i], OUTPUT);
        pinMode(buttonPins[i], INPUT_PULLUP);
    }
    Serial.println("Prueba de LEDs y botones iniciada.");
    Serial.println("Presiona un botón para encender su LED correspondiente.");
}

// Bucle principal
void loop() {
    for (int i = 0; i < 5; i++) {
        if (digitalRead(buttonPins[i]) == LOW) {
            digitalWrite(ledPins[i], HIGH);
            Serial.print("Botón ");
            Serial.print(i + 1);
            Serial.println(" presionado. LED encendido.");
        } else {
            digitalWrite(ledPins[i], LOW);
        }
    }
}
