import threading

from utils.log_config import get_logger

try:
    from gpiozero import Button
    RASPBERRY_PI = True
except ImportError:
    RASPBERRY_PI = False

logger = get_logger(__name__)

BUTTON_PINS = {
    "A": 17,
    "B": 27,
    "C": 22
}

class ButtonService:
    def __init__(self, button_callback):
        self.button_callback = button_callback
        self.running = True
        self.listen_thread = None

        if RASPBERRY_PI:
            self._initialize_real_buttons()
        else:
            self._initialize_mock_buttons()

    def _initialize_real_buttons(self) -> None:
        logger.info("Initializing real GPIO buttons")
        self.buttons = {name: Button(pin) for name, pin in BUTTON_PINS.items()}
        for name, button in self.buttons.items():
            button.when_pressed = lambda name: self.button_callback(name)

    def _initialize_mock_buttons(self) -> None:
        logger.info("Initializing mock button input")
        self.listen_thread = threading.Thread(target=self._mock_input, daemon=True)
        self.listen_thread.start()

    def _mock_input(self) -> None:
        while self.running:
            key = input("Press 'A', 'B', or 'C' to start, or 'Q' to quit: ").strip().upper()
            if key in BUTTON_PINS:
                self.button_callback(key)
                break
            elif key == "Q":
                logger.info("Exiting test mode.")
                self.running = False
                exit(0)
            else:
                print("Invalid input. Press 'A', 'B', or 'C' to start or 'Q' to quit.")

    def stop(self) -> None:
        self.running = False