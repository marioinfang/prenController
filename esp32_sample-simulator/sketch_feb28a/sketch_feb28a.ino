#include <Arduino.h>

#define RX_PIN 16  // UART RX Pin
#define TX_PIN 17  // UART TX Pin
#define BAUD_RATE 115200

HardwareSerial uart(2);

void setup() {
    Serial.begin(BAUD_RATE);
    uart.begin(BAUD_RATE, SERIAL_8N1, RX_PIN, TX_PIN);
    Serial.println("ESP32 UART gestartet");
}

void loop() {
    if (uart.available()) {
        String command = uart.readStringUntil('\n');
        command.trim();

        Serial.print("Empfangen: ");
        Serial.println(command);

        if (command == "WEG_BEFAHREN") {
            delay(random(500, 4000));
            uart.println("WEGPUNKT_ERREICHT");
        } 
        else if (command == "WEGPUNKT_ANALYSIEREN") {
            delay(random(500, 4000));
            uart.println("ZIEL_ERKANNT");
        } 
        else if (command == "ZIEL_IDENTIFIZIEREN") {
            delay(random(500, 4000));
            uart.println("HINDERNIS_GEFUNDEN");
        } 
        else if (command == "HINDERNIS_ANHEBEN") {
            uart.println("HEBEN");
            delay(random(500, 4000));
            uart.println("HEBEN_FERTIG");
        } 
        else {
            uart.println("ERROR");
        }
    }
}
