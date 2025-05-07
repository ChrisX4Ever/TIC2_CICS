const int LED_RED = 5;
const int LED_GREEN = 6;
const int LED_BLUE = 3;
const int BUTTON_PIN = 13;

unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
bool lastButtonState = HIGH;
bool buttonPressed = false;

void setup() {
  Serial.begin(9600);

  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // Botón con resistencia pull-up interna
}

void loop() {
  // Lectura serial (desde Python)
  if (Serial.available()) {
    String input = Serial.readStringUntil('\\n');
    int population = input.toInt();

    // Apagar todos los LEDs primero
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_BLUE, LOW);

    // Clasificar población
    if (population < 500) {
      digitalWrite(LED_RED, HIGH); // Subpoblación
    } else if (population >= 500 && population <= 1500) {
      digitalWrite(LED_GREEN, HIGH); // Estabilidad
    } else {
      digitalWrite(LED_BLUE, HIGH); // Sobrepoblación
    }
  }

  // Lectura del botón
  bool currentButtonState = digitalRead(BUTTON_PIN);
  if (currentButtonState == LOW && lastButtonState == HIGH && (millis() - lastDebounceTime) > debounceDelay) {
    lastDebounceTime = millis();
    Serial.println("RESET");  // Enviar mensaje a Python
  }
  lastButtonState = currentButtonState;
}
