import serial

class UARThandler:
    def __init__(self, port='/dev/serial0', baudrate=115200):
        """Initialisiert die UART-Schnittstelle"""
        self.ser = serial.Serial(port, baudrate, timeout=1)

    def send(self, command):
        """Sendet einen Befehl an den STM32"""
        if self.ser.is_open:
            self.ser.write(command.encode())
            print(f"[UART] Senden → STM32: {command}")

    def receive(self):
        """Empfängt Daten vom STM32"""
        if self.ser.in_waiting > 0:
            response = self.ser.readline().decode().strip()
            print(f"[UART] Empfangen ← STM32: {response}")
            return response
        return None

    def close(self):
        """Schließt die UART-Verbindung"""
        self.ser.close()