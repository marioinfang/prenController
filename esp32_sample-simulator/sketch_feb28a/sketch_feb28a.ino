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

      
        if (command.startsWith("drive")) {
            delay(random(500, 1500));
            uart.println("ACK");
        }
        else if (command == "stop") {
            delay(random(500, 1500));
            uart.println("ACK");
        }
        else if (command == "drive_to_waypoint") {
            delay(random(500, 1500));
            uart.println("ACK");
        } 
        else if (command == "rotate") {
            delay(random(500, 1500));
            uart.println("ACK");
        }
    }
}