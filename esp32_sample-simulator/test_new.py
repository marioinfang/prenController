import serial
import time


SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 115200


commands = [
    "WEG_BEFAHREN",
    "WEGPUNKT_ANALYSIEREN",
    "ZIEL_IDENTIFIZIEREN",
    "HINDERNIS_ANHEBEN"
]

def send_command(ser, command):
    """Send a command to the ESP32 and wait for a response."""
    print(f"Sending: {command}")
    ser.write((command + "\n").encode())  # Befehl senden

    response = ""

    # Warte auf eine Antwort, ohne Timeout
    while True:
        if ser.in_waiting > 0:  # Falls Daten verfügbar sind
            response = ser.readline().decode().strip()  # Antwort lesen
            break  # Schleife beenden, wenn eine Antwort empfangen wurde

    print(f"Response: {response}")
    return response

def main():
    try:
        # Serielle Verbindung öffnen
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=None)  # Kein Timeout
        time.sleep(2)  # Warten auf Verbindung

        print("Connected to ESP32 via UART.")

        # Befehle einzeln senden
        for command in commands:
            response = send_command(ser, command)

            # Falls eine Fehlermeldung kommt
            if response == "ERROR":
                print("ESP32 returned an error!")
            time.sleep(1)  # Verzögerung vor dem nächsten Befehl

        ser.close()
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nUser interrupted.")

if __name__ == "__main__":
    main()