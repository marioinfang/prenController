import serial
import time

SERIAL_PORT = "/dev/serial0"  # Falls ein USB-Adapter genutzt wird: "/dev/ttyUSB0"
BAUD_RATE = 115200

commands = [
    "WEG_BEFAHREN",
    "WEGPUNKT_ANALYSIEREN",
    "ZIEL_IDENTIFIZIEREN",
    "HINDERNIS_ANHEBEN"
]

def send_command(ser, command):
    """Send a command to the ESP32 and read the response."""
    print(f"Sending: {command}")
    ser.write((command + "\n").encode())  # Send command
    time.sleep(0.1)  # Small delay for ESP32 to process

    response = ser.readline().decode().strip()  # Read response
    print(f"Response: {response}")
    return response

def main():
    try:
        # Open serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Wait for connection to establish

        print("Connected to ESP32 via UART.")

        # Send commands one by one
        for command in commands:
            response = send_command(ser, command)

            # Handle specific responses if needed
            if response == "ERROR":
                print("ESP32 returned an error!")
            time.sleep(1)  # Delay before sending next command

        ser.close()
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nUser interrupted.")

if __name__ == "__main__":
    main()
