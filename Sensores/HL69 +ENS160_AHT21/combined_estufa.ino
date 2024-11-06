
#include <Wire.h>
#include <Adafruit_AHTX0.h>
#include "ScioSense_ENS160.h"

// Definição dos pinos
int ArduinoLED_Red = 8;    // LED vermelho para temperatura
int ArduinoLED_Yellow = 9; // LED amarelo para CO2
int ArduinoLED_Green = 10;  // LED verde para umidade do solo
int rainPin = A0;          // Sensor de umidade do solo

// Sensores e variáveis
Adafruit_AHTX0 aht;
ScioSense_ENS160 ens160(ENS160_I2CADDR_1); //0x53 para ENS160

// Variáveis para leituras
int tempC;
int humidity;
int soilMoistureValue;


int co2Limit = 600;      // Limite de CO2 em ppm
int tempLimit = 30;       // Limite de temperatura em graus Celsius
int soilMoistureLimit = 800; // Limite para umidade do solo
int humidityLimit = 50; //Limite de umidade do ar

void setup() {
  Serial.begin(9600);

  // Inicialização dos pinos
  pinMode(ArduinoLED_Red, OUTPUT);
  pinMode(ArduinoLED_Yellow, OUTPUT);
  pinMode(ArduinoLED_Green, OUTPUT);
  pinMode(rainPin, INPUT);

  digitalWrite(ArduinoLED_Red, LOW);
  digitalWrite(ArduinoLED_Yellow, LOW);
  digitalWrite(ArduinoLED_Green, LOW);

  // Inicialização do sensor AHT
  if (!aht.begin()) {
    Serial.println("Erro ao inicializar AHT!");
    while (1) delay(10);
  }
  Serial.println("AHT20 inicializado!");

  // Inicialização do sensor ENS160
  if (ens160.begin()) {
    Serial.println("ENS160 inicializado!");
    ens160.setMode(ENS160_OPMODE_STD);
  } else {
    Serial.println("Erro ao inicializar ENS160!");
  }
}

void loop() {
  // Leitura do sensor de temperatura e umidade (AHT20)
  sensors_event_t humidityEvent, tempEvent;
  aht.getEvent(&humidityEvent, &tempEvent);
  tempC = tempEvent.temperature;
  humidity = humidityEvent.relative_humidity;
  Serial.print("Temperatura: ");
  Serial.print(tempC);
  Serial.println(" C");
  Serial.print("Umidade: ");
  Serial.print(humidity);
  Serial.println(" %");

  // Leitura do sensor de CO2 (ENS160)
  ens160.set_envdata(tempC, humidity);
  ens160.measure(true);
  int co2Value = ens160.geteCO2();
  Serial.print("CO2: ");
  Serial.print(co2Value);
  Serial.println(" ppm");

  // Leitura do sensor de umidade do solo
  soilMoistureValue = analogRead(rainPin);
  Serial.print("Umidade do Solo: ");
  Serial.println(soilMoistureValue);

  // Verificação dos limites e ativação dos LEDs
  if (tempC > tempLimit) {
    digitalWrite(ArduinoLED_Red, HIGH);   // Temperatura elevada
  } else {
    digitalWrite(ArduinoLED_Red, LOW);
  }

  if (co2Value > co2Limit) {
    digitalWrite(ArduinoLED_Yellow, HIGH); // CO2 elevado

  } else {
    digitalWrite(ArduinoLED_Yellow, LOW);
  }

  if (soilMoistureValue > soilMoistureLimit) {
    digitalWrite(ArduinoLED_Green, HIGH);  // Umidade do solo baixa
  } else {
    digitalWrite(ArduinoLED_Green, LOW);
  }

    if (humidity > humidityLimit) {
    digitalWrite(ArduinoLED_Green, HIGH);  // Umidade do ar baixa
    digitalWrite(ArduinoLED_Red, HIGH);   // Umidade do ar baixa
  } else {
    digitalWrite(ArduinoLED_Green, LOW);
    digitalWrite(ArduinoLED_Red, LOW);
  }

  delay(5000); // Atraso para a próxima leitura
}
