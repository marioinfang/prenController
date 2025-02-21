import time
from states import State
from communication.uart_handler import UARThandler

class CarStateMachine:
    def __init__(self, uart):
        """Initialisiert die State Machine mit einer UART-Schnittstelle"""
        self.uart = uart
        self.state = State.INIT

    def transition(self):
        """Führt Zustandswechsel basierend auf der aktuellen Aufgabe durch"""
        if self.state == State.INIT:
            print("[INIT] Initialisiere Fahrzeug...")
            self.uart.send("INIT_COMPLETE")
            time.sleep(1)
            self.state = State.WEG_BEFAHREN

        elif self.state == State.WEG_BEFAHREN:
            print("[WEG_BEFAHREN] Fahrzeug fährt...")
            self.uart.send("FAHRE_WEITER")
            response = self.uart.receive()
            if response == "WEGPUNKT_ERREICHT":
                self.state = State.WEGPUNKT_ANALYSIEREN

        elif self.state == State.WEGPUNKT_ANALYSIEREN:
            print("[WEGPUNKT_ANALYSIEREN] Analysiere Wegpunkt...")
            self.uart.send("ANALYSIERE_WEGPUNKT")
            response = self.uart.receive()
            if response == "AUSRICHTUNG_NOTWENDIG":
                self.state = State.WEGPUNKT_AUSRICHTEN
            elif response == "ZIEL_ERKANNT":
                self.state = State.ZIEL_IDENTIFIZIEREN
            else:
                self.state = State.WEG_BEFAHREN

        elif self.state == State.WEGPUNKT_AUSRICHTEN:
            print("[WEGPUNKT_AUSRICHTEN] Fahrzeug richtet sich aus...")
            self.uart.send("AUSRICHTEN")
            time.sleep(2)
            self.state = State.WEG_BEFAHREN

        elif self.state == State.ZIEL_IDENTIFIZIEREN:
            print("[ZIEL_IDENTIFIZIEREN] Identifiziere Ziel...")
            self.uart.send("IDENTIFIZIERE_ZIEL")
            response = self.uart.receive()
            if response == "HINDERNIS_GEFUNDEN":
                self.state = State.HINDERNIS_ANHEBEN
            else:
                self.state = State.WEG_BEFAHREN

        elif self.state == State.HINDERNIS_ANHEBEN:
            print("[HINDERNIS_ANHEBEN] Hindernis wird angehoben...")
            self.uart.send("HEBEN")
            time.sleep(3)
            self.uart.send("HEBEN_FERTIG")
            self.state = State.WEG_BEFAHREN

        elif self.state == State.ERROR:
            print("[ERROR] Fehler erkannt! Zurücksetzen...")
            self.uart.send("ERROR_RESET")
            time.sleep(2)
            self.state = State.INIT

    def run(self):
        """Startet die State Machine"""
        try:
            while True:
                self.transition()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Beende Programm...")
            self.uart.close()