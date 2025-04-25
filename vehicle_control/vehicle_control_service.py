from communication.uart_service import UARTService
from state_machine.types.decision_state import Decision
from utils.log_config import get_logger
from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from vehicle_control.types.detection_type import StopTypes
from vehicle_control.types.direction_type import DirectionType

logger = get_logger(__name__)

class VehicleControlService:
    def __init__(self):
        self.uart_service = UARTService()

    def drive(self, state: Decision, blocked: bool, distance: int) -> None:
        #self._send_command(f"drive({state},{blocked},{distance})")
        self._send_command("T 40 50")

    def stop(self, state: Decision, reason: StopTypes) -> None:
        #self._send_command(f"stop({state},{reason})")
        self._send_command(f"stop({state},{reason})")

    def drive_to_waypoint(self, state: Decision) -> None:
        self._send_command(f"V 40 50")

    def rotate(self, state: Decision, direction: DirectionType, angle: int) -> None:
        #self._send_command(f"rotate({state},{direction},{angle})")
        self._send_command(f"CCW 525 50") #90 degrees

    #TODO add move obstacle method

    def _send_command(self, command: str) -> None:
        response = self.uart_service.send(command)
        if self._is_error_response(response):
            error_msg = f"Error on command execution response-> {response}"
            logger.error(error_msg)
            raise CommandExecutionError(error_msg)

    def start_listen(self):
        self.uart_service.start_listening()

    def get_received_message(self) -> str:
        return self.uart_service.get_received_message()

    def stop_listen(self):
        self.uart_service.stop_listening()


    @staticmethod
    def _is_error_response(response: str) -> bool:
        return response.startswith("ERR")