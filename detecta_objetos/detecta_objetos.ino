#define LEDPIN 13
#define SENSORPIN 4

// Variables que cambiarán:
int sensorState = 0, lastState = HIGH;
unsigned long lastDetectionTime = 0;  // Tiempo de la última detección
unsigned long lastClearTime = 0;      // Tiempo desde que el sensor quedó despejado
const unsigned long detectionDelay = 3000;  // 3 segundos de retraso

void setup() {
  // Inicializar el pin LED como salida:
  pinMode(LEDPIN, OUTPUT);
  // Inicializar el pin del sensor como entrada:
  pinMode(SENSORPIN, INPUT);
  digitalWrite(SENSORPIN, HIGH); // Activar el pullup

  Serial.begin(9600);
}

void loop() {
  // Leer el estado del sensor:
  sensorState = digitalRead(SENSORPIN);

  // Verificar si el sensor detecta un objeto
  if (sensorState == LOW && lastState == HIGH) {
    // Si no ha pasado suficiente tiempo desde la última detección, ignorar
    if (millis() - lastClearTime >= detectionDelay) {
      Serial.println("Broken");
      digitalWrite(LEDPIN, HIGH);  // Encender el LED
      lastDetectionTime = millis();  // Actualizar el tiempo de la detección
    }
  }

  // Verificar si el haz ya no está interrumpido
  if (sensorState == HIGH && lastState == LOW) {
    Serial.println("Unbroken");
    digitalWrite(LEDPIN, LOW);  // Apagar el LED
    lastClearTime = millis();  // Actualizar el tiempo cuando el haz quedó libre
  }

  // Actualizar lastState
  lastState = sensorState;
}
