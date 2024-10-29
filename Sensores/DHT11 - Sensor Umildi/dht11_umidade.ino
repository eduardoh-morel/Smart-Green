#include <DHT.h>

#define DHTPIN 2          // Define o pino de dados do sensor DHT11
#define DHTTYPE DHT11     // Define o tipo do sensor como DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);    // Inicia a comunicação serial
  dht.begin();           // Inicia o sensor DHT11
}

void loop() {
  delay(2000);  // Aguarda 2 segundos entre as leituras

  float temperatura = dht.readTemperature(); // Lê a temperatura em Celsius
  float umidade = dht.readHumidity();        // Lê a umidade relativa

  // Verifica se houve erro na leitura
  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Falha na leitura do sensor DHT11!");
    return;
  }

  // Exibe os valores lidos no monitor serial
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" °C");

  Serial.print("Umidade: ");
  Serial.print(umidade);
  Serial.println(" %");
}
