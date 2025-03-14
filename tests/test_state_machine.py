from unittest import TestCase
from unittest.mock import MagicMock

from state_machine.state_machine import CarStateMachine
from states import State

class TestCarStateMachine(TestCase):
    def setUp(self):
        self.mock_uart = MagicMock()
        self.state_machine = CarStateMachine(self.mock_uart)

    def test_initial_state(self):
        self.assertEqual(self.state_machine.state, State.INIT)

    def test_transition_from_init_to_weg_befahren(self):
        self.state_machine.transition()
        self.mock_uart.send.assert_called_with("INIT_COMPLETE")
        self.assertEqual(self.state_machine.state, State.WEG_BEFAHREN)

    def test_transition_from_weg_befahren_to_wegpunkt_analysieren(self):
        self.state_machine.state = State.WEG_BEFAHREN
        self.mock_uart.receive.return_value = "WEGPUNKT_ERREICHT"
        self.state_machine.transition()
        self.mock_uart.send.assert_called_with("FAHRE_WEITER")
        self.assertEqual(self.state_machine.state, State.WEGPUNKT_ANALYSIEREN)

    def test_transition_from_wegpunkt_analysieren_to_wegpunkt_ausrichten(self):
        self.state_machine.state = State.WEGPUNKT_ANALYSIEREN
        self.mock_uart.receive.return_value = "AUSRICHTUNG_NOTWENDIG"
        self.state_machine.transition()
        self.mock_uart.send.assert_called_with("ANALYSIERE_WEGPUNKT")
        self.assertEqual(self.state_machine.state, State.WEGPUNKT_AUSRICHTEN)

    def test_transition_from_wegpunkt_analysieren_to_ziel_identifizieren(self):
        self.state_machine.state = State.WEGPUNKT_ANALYSIEREN
        self.mock_uart.receive.return_value = "ZIEL_ERKANNT"
        self.state_machine.transition()
        self.mock_uart.send.assert_called_with("ANALYSIERE_WEGPUNKT")
        self.assertEqual(self.state_machine.state, State.ZIEL_IDENTIFIZIEREN)

    def test_transition_from_ziel_identifizieren_to_hindernis_aufnehmen(self):
        self.state_machine.state = State.ZIEL_IDENTIFIZIEREN
        self.mock_uart.receive.return_value = "HINDERNIS_GEFUNDEN"
        self.state_machine.transition()
        self.mock_uart.send.assert_called_with("IDENTIFIZIERE_ZIEL")
        self.assertEqual(self.state_machine.state, State.HINDERNIS_ANHEBEN)

    def test_transition_from_hindernis_aufnehmen_to_weg_befahren(self):
        self.state_machine.state = State.HINDERNIS_ANHEBEN
        self.state_machine.transition()
        self.mock_uart.send.assert_any_call("HEBEN")
        self.mock_uart.send.assert_any_call("HEBEN_FERTIG")
        self.assertEqual(self.state_machine.state, State.WEG_BEFAHREN)

    def test_error_state_transition(self):
        self.state_machine.state = State.ERROR
        self.state_machine.transition()
        self.mock_uart.send.assert_called_with("ERROR_RESET")
        self.assertEqual(self.state_machine.state, State.INIT)