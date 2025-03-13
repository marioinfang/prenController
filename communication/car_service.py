from communication.types.detection_type import StopTypes
from communication.types.direction_type import DirectionType
from state_machine.types.decision_state import Decision
from utils.log_config import get_logger
from .uart_service import UARTService

logger = get_logger(__name__)

class CarService:
    def __init__(self):
        self.uart_service = UARTService()

    def drive(self, state: Decision, blocked: bool, distance: int):
        self.uart_service.send(f"drive({state},{blocked},{distance})")

    def stop(self, state: Decision, reason: StopTypes):
        self.uart_service.send(f"stop({state},{reason})")

    def drive_to_waypoint(self, state: Decision):
        self.uart_service.send(f"drive_to_waypoint({state})")

    def rotate(self, state: Decision, direction: DirectionType, angle: int):
        self.uart_service.send(f"rotate({state},{direction},{angle})")