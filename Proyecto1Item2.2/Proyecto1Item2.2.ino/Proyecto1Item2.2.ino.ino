const int boton1 = 12;    // Infección masiva
const int boton2 = 11;    // Infección masiva mutada
const int boton3 = 10;    // Ritual de purificación
const int boton4 = 8;     // I am atomic!

const int ledVerde = 6;
const int ledAzul = 3;
const int ledRojo = 9;

String comando = "";

void setup() {
    Serial.begin(9600);
    
    pinMode(boton1, INPUT_PULLUP);
    pinMode(boton2, INPUT_PULLUP);
    pinMode(boton3, INPUT_PULLUP);
    pinMode(boton4, INPUT_PULLUP);

    pinMode(ledVerde, OUTPUT);
    pinMode(ledAzul, OUTPUT);
    pinMode(ledRojo, OUTPUT);

    digitalWrite(ledVerde, LOW);
    digitalWrite(ledAzul, LOW);
    digitalWrite(ledRojo, LOW);
}

void loop() {
    if (Serial.available()) {
        comando = Serial.readStringUntil('\n');
        comando.trim();

        if (comando == "sobrepoblacion") {
            digitalWrite(ledVerde, HIGH);
            digitalWrite(ledAzul, LOW);
            digitalWrite(ledRojo, LOW);
        } else if (comando == "estabilidad") {
            digitalWrite(ledVerde, LOW);
            digitalWrite(ledAzul, HIGH);
            digitalWrite(ledRojo, LOW);
        } else if (comando == "subpoblacion") {
            digitalWrite(ledVerde, LOW);
            digitalWrite(ledAzul, LOW);
            digitalWrite(ledRojo, HIGH);
        }
    }

    if (digitalRead(boton1) == LOW) {
        Serial.println("e1");
        delay(300);  // Anti-rebote
    }
    if (digitalRead(boton2) == LOW) {
        Serial.println("e2");
        delay(300);
    }
    if (digitalRead(boton3) == LOW) {
        Serial.println("e3");
        delay(300);
    }
    if (digitalRead(boton4) == LOW) {
        Serial.println("e4");
        delay(300);
    }
}