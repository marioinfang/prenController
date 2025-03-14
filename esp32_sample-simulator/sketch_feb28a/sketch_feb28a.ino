#include <Arduino.h>

#define RX_PIN 16  // UART RX Pin
#define TX_PIN 17  // UART TX Pin
#define BAUD_RATE 115200

HardwareSerial uart(2);

void setup() {
    Serial.begin(BAUD_RATE);
    uart.begin(BAUD_RATE, SERIAL_8N1, RX_PIN, TX_PIN);
    Serial.println("ESP32 initialized");
}

void loop() {
    if (uart.available()) {
        String command = uart.readStringUntil('\n');
        command.trim();

        Serial.print("Received: ");
        Serial.println(command);

        if (command == "INIT_COMPLETE") {
            delay(random(500, 4000));
            uart.println("ack");
        }
        else if (command == "FAHRE_WEITER") {
            int randomValue = random(2);
            if (randomValue) {
                uart.println("WEGPUNKT_ERREICHT");
            } else {
                uart.println("ack");
            }
        }
        else if (command == "WEG_BEFAHREN") {
            delay(random(500, 4000));
            int randomValue = random(3);
            if (randomValue == 0) {
                uart.println("AUSRICHTUNG_NOTWENDIG");
            } else if(randomValue == 1){
                uart.println("ZIEL_ERKANNT");
            } else {
                uart.println("ack");
            }
        }
        else if (command == "ANALYSIERE_WEGPUNKT") {
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
        else if (command == "IDENTIFIZIERE_ZIEL"){
            int randomValue = random(2);
            if (randomValue) {
                uart.println("HINDERNIS_GEFUNDEN");
            } else {
                uart.println("ack");
            }
        }
        else {
            uart.println("ERROR");
        }
    }
}