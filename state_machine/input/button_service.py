import threading
from gpiozero import Button
from utils.log_config import get_logger
from utils.raspberry_checker import is_raspberry_pi

logger = get_logger(__name__)

BUTTON_PINS = {
    "A": 6,
    "B": 13,
    "C": 25,
    "Start": 26
}

class ButtonService:
    _instance = None

    def __init__(self):
        if ButtonService._instance is not None:
            raise Exception("Use get_instance() to get the singleton instance")

        self.start_callback = None
        self.selected_destination = None
        self.running = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ButtonService()
        return cls._instance

    def set_start_callback(self, callback):
        self.start_callback = callback
        if is_raspberry_pi():
            self._initialize_real_buttons()
        else:
            self._initialize_mock_buttons()

    def get_selected_destination(self) -> str:
        return self.selected_destination

    def stop(self) -> None:
        self.running = False

    def make_callback(self,name):
        return lambda: self._handle_press(name)

    def _initialize_real_buttons(self):
        logger.info("Initializing real GPIO buttons")
        self.buttons = {name: Button(pin) for name, pin in BUTTON_PINS.items()}
        for name, button in self.buttons.items():
            button.when_pressed = self.make_callback(name)

    def _initialize_mock_buttons(self) -> None:
        logger.info("Initializing mock button input")
        self.listen_thread = threading.Thread(target=self._mock_input, daemon=True)
        self.listen_thread.start()

    def _handle_press(self, name: str):
        logger.info("Handling button press"+name)
        if name in ["A", "B", "C"]:
            self.selected_destination = name
            logger.info(f"Destination selected: {name}. Now press 'Start' to continue.")
        elif name == "Start":
            if self.selected_destination:
                logger.info(f"'Start' pressed after selecting {self.selected_destination}")
                self.running = False
                self.start_callback(self.selected_destination)
            else:
                logger.warning("Please select a destination (A/B/C) before pressing Start.")

    def _mock_input(self):
        while self.running:
            key = input("Press A, B, C to select destination, then press Start to continue (or Q to quit): ").strip().upper()
            if key in ["A", "B", "C"]:
                self.selected_destination = key
                logger.info(f"Destination selected: {key}.")
                self.running = False
                self.start_callback(self.selected_destination)
            elif key == "Q":
                logger.info("Exiting test mode.")
                self.running = False
                exit(0)
            else:
                print("Invalid input. Use A, B, C then START or Q to quit.")