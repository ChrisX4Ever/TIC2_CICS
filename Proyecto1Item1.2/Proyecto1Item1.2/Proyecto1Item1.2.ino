#include <TonePitch.h>

// Definición de pines
const int buzzerPin = 5;
const int ledPins[5] = {9, 3, 4, 7, 2};
const int buttonPins[5] = {13, 12, 11, 10, 18};

// Definición de tonos para cada LED/Botón
int notes[5] = {NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4};

// Variables para el juego
int dificultad = 0;
int velocidad = 0;
int puntuacion = 0;
int racha = 0;
int multiplicador = 1;
bool gameOver = false;
TonePitch tonePlayer;

// Canciones predefinidas (se pueden expandir)
int marioBros[] = {0, 2, 1, 3, 4, 0, 2, 1, 3, 4};
int starWars[] = {1, 3, 4, 2, 0, 1, 3, 4, 2, 0};
int harryPotter[] = {4, 3, 2, 1, 0, 4, 3, 2, 1, 0};

int *cancionSeleccionada;
int tamanoCancion;

// Configuración inicial
void setup() {
    Serial.begin(9600);
    tonePlayer.begin(buzzerPin);
    
    for (int i = 0; i < 5; i++) {
        pinMode(ledPins[i], OUTPUT);
        pinMode(buttonPins[i], INPUT_PULLUP);
    }

    menuSeleccion();
}

// Menú de selección
void menuSeleccion() {
    Serial.println("Selecciona una dificultad:");
    Serial.println("1. Fácil");
    Serial.println("2. Medio");
    Serial.println("3. Difícil");
    
    while (dificultad < 1 || dificultad > 3) {
        if (Serial.available()) {
            dificultad = Serial.parseInt();
        }
    }
    
    velocidad = (dificultad == 1) ? 1000 : (dificultad == 2) ? 700 : 500;

    Serial.println("Selecciona una canción:");
    Serial.println("1. Mario Bros");
    Serial.println("2. Star Wars");
    Serial.println("3. Harry Potter");
    
    int seleccion = 0;
    while (seleccion < 1 || seleccion > 3) {
        if (Serial.available()) {
            seleccion = Serial.parseInt();
        }
    }
    
    switch (seleccion) {
        case 1:
            cancionSeleccionada = marioBros;
            tamanoCancion = sizeof(marioBros) / sizeof(int);
            break;
        case 2:
            cancionSeleccionada = starWars;
            tamanoCancion = sizeof(starWars) / sizeof(int);
            break;
        case 3:
            cancionSeleccionada = harryPotter;
            tamanoCancion = sizeof(harryPotter) / sizeof(int);
            break;
    }

    iniciarJuego();
}

void iniciarJuego() {
    puntuacion = 0;
    racha = 0;
    multiplicador = 1;
    gameOver = false;

    for (int i = 0; i < tamanoCancion; i++) {
        if (gameOver) break;
        
        int nota = cancionSeleccionada[i];
        digitalWrite(ledPins[nota], HIGH);
        tonePlayer.play(notes[nota], velocidad);

        unsigned long startTime = millis();
        bool acierto = false;

        while (millis() - startTime < velocidad) {
            if (digitalRead(buttonPins[nota]) == LOW) {
                acierto = true;
                break;
            }
        }

        digitalWrite(ledPins[nota], LOW);
        tonePlayer.stop();

        if (acierto) {
            procesarAcierto();
        } else {
            procesarError();
        }
    }
    finalizarJuego();
}

void procesarAcierto() {
    puntuacion += 10 * multiplicador;
    racha++;
    
    if (racha == 5) multiplicador = 2;
    else if (racha == 10) multiplicador = 4;
    else if (racha == 15) multiplicador = 8;
    else if (racha == 20) multiplicador = 16;
}

void procesarError() {
    puntuacion -= 5;
    racha = 0;
    multiplicador = 1;

    if (puntuacion <= 0) {
        gameOver = true;
        Serial.println("Game Over!");
        tonePlayer.play(NOTE_B2, 1000); // Tono de Game Over
    }
}

void finalizarJuego() {
    if (gameOver) {
        Serial.println("Juego terminado, tu puntuación fue: 0");
    } else {
        Serial.print("¡Juego completado! Tu puntuación final fue: ");
        Serial.println(puntuacion);
    }
    Serial.println("¿Deseas jugar de nuevo? (S/N)");

    while (true) {
        if (Serial.available()) {
            char respuesta = Serial.read();
            if (respuesta == 'S' || respuesta == 's') {
                menuSeleccion();
                break;
            } else if (respuesta == 'N' || respuesta == 'n') {
                Serial.println("Juego finalizado. ¡Gracias por jugar!");
                break;
            }
        }
    }
}
