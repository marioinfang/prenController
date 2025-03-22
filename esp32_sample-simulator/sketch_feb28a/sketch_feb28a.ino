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
        delay(random(500, 1000));
        uart.println("ACK");
    }
}