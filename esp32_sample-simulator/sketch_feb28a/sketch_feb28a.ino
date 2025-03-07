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
            bool randomizedNumb = random(0, 1);
            if (randomizedNumb) {
                uart.println("WEGPUNKT_ERREICHT");
            } else {
                uart.println("ack");
            }
        }
        else if (command == "WEG_BEFAHREN") {
            delay(random(500, 4000));
             bool randomizedNumb = random(0, 2);
            if (randomizedNumb == 0) {
                uart.println("AUSRICHTUNG_NOTWENDIG");
            } else if(randomizedNumb == 1){
                uart.println("ZIEL_ERKANNT");
            } else {
                uart.println("ack");
            }
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
        else if (command == "IDENTIFIZIERE_ZIEL"){
            bool randomizedNumb = random(0, 1);
            if (randomizedNumb) {
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