const int buttonPin13 = 13;  // Pin para el botón de reset
const int buttonPin12 = 12;  // Infección masiva
const int buttonPin11 = 11;  // Infección masiva mutada
const int buttonPin10 = 10;  // Ritual de purificación
const int buttonPin8 = 8;    // I am atomic!

bool lastState13 = HIGH;
bool lastState12 = HIGH;
bool lastState11 = HIGH;
bool lastState10 = HIGH;
bool lastState8 = HIGH;

unsigned long debounceDelay = 50;  // 50 ms para evitar rebotes
unsigned long lastDebounceTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin13, INPUT_PULLUP);
  pinMode(buttonPin12, INPUT_PULLUP);
  pinMode(buttonPin11, INPUT_PULLUP);
  pinMode(buttonPin10, INPUT_PULLUP);
  pinMode(buttonPin8, INPUT_PULLUP);
}

void loop() {
  unsigned long currentTime = millis();

  if ((digitalRead(buttonPin13) == LOW) && (lastState13 == HIGH) && (currentTime - lastDebounceTime > debounceDelay)) {
    Serial.println("r");
    lastState13 = LOW;
    lastDebounceTime = currentTime;
  } else if (digitalRead(buttonPin13) == HIGH) {
    lastState13 = HIGH;
  }

  if ((digitalRead(buttonPin12) == LOW) && (lastState12 == HIGH) && (currentTime - lastDebounceTime > debounceDelay)) {
    Serial.println("e1");
    lastState12 = LOW;
    lastDebounceTime = currentTime;
  } else if (digitalRead(buttonPin12) == HIGH) {
    lastState12 = HIGH;
  }

  if ((digitalRead(buttonPin11) == LOW) && (lastState11 == HIGH) && (currentTime - lastDebounceTime > debounceDelay)) {
    Serial.println("e2");
    lastState11 = LOW;
    lastDebounceTime = currentTime;
  } else if (digitalRead(buttonPin11) == HIGH) {
    lastState11 = HIGH;
  }

  if ((digitalRead(buttonPin10) == LOW) && (lastState10 == HIGH) && (currentTime - lastDebounceTime > debounceDelay)) {
    Serial.println("e3");
    lastState10 = LOW;
    lastDebounceTime = currentTime;
  } else if (digitalRead(buttonPin10) == HIGH) {
    lastState10 = HIGH;
  }

  if ((digitalRead(buttonPin8) == LOW) && (lastState8 == HIGH) && (currentTime - lastDebounceTime > debounceDelay)) {
    Serial.println("e4");
    lastState8 = LOW;
    lastDebounceTime = currentTime;
  } else if (digitalRead(buttonPin8) == HIGH) {
    lastState8 = HIGH;
  }
}