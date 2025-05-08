// Pines de conexión
const int ledRojo = 9;
const int ledVerde = 6;
const int ledAzul = 3;
const int buzzer = 5;
const int botonReset = 13;

// Variables de control
bool estadoBoton = false;
String comando = "";
int poblacion = 0;

void setup() {
    Serial.begin(9600);
    pinMode(ledRojo, OUTPUT);
    pinMode(ledVerde, OUTPUT);
    pinMode(ledAzul, OUTPUT);
    pinMode(buzzer, OUTPUT);
    pinMode(botonReset, INPUT_PULLUP);

    // Apagar todos los LEDs inicialmente
    digitalWrite(ledRojo, LOW);
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledAzul, LOW);
}

void loop() {
    // Lectura del botón físico
    if (digitalRead(botonReset) == LOW && !estadoBoton) {
        estadoBoton = true;
        Serial.println("r");
        delay(500); // Anti-rebote
    } else if (digitalRead(botonReset) == HIGH) {
        estadoBoton = false;
    }

    // Recepción de datos seriales
    if (Serial.available()) {
        comando = Serial.readStringUntil('\n');
        
        if (comando.startsWith("p-")) {
            poblacion = comando.substring(2).toInt();
            actualizarLEDs(poblacion);
        } else if (comando.startsWith("a-")) {
            int evento = comando.substring(2).toInt();
            activarEvento(evento);
        }
    }
}

void actualizarLEDs(int poblacion) {
    // Apagar todos los LEDs antes de actualizar
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledRojo, LOW);
    digitalWrite(ledAzul, LOW);

    if (poblacion < 200) {
        digitalWrite(ledVerde, HIGH); // Estabilidad
    } else if (poblacion >= 200 && poblacion <= 500) {
        digitalWrite(ledAzul, HIGH);  // Subpoblación
    } else {
        digitalWrite(ledRojo, HIGH);  // Sobrepoblación
    }
}

void activarEvento(int evento) {
    switch (evento) {
        case 1:
            tone(buzzer, 1000, 500); // Sonido de infección masiva
            break;
        case 2:
            tone(buzzer, 1200, 500); // Sonido de infección masiva mutada
            break;
        case 3:
            tone(buzzer, 800, 500); // Sonido de ritual de purificación
            break;
        case 4:
            tone(buzzer, 400, 500); // Sonido de "I am Atomic!"
            break;
    }
}