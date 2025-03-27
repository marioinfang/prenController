from vehicle_control.types.detection_type import StopTypes
from vehicle_control.exceptions.command_execution_exception import CommandExecutionError
from vehicle_control.vehicle_control_service import VehicleControlService
from utils.log_config import get_logger
from .base_state import BaseState
from state_machine.types.decision_state import Decision
from .error import Error

logger = get_logger(__name__)


class ConeDetected(BaseState):
    def __init__(self, machine):
        self.machine = machine
        self.vehicle_control_service = VehicleControlService()


    def context(self):
        logger.info("Entered State: ConeDetected")
        try:
            self.vehicle_control_service.stop(state=Decision.CONE_DETECTED, reason=StopTypes.CONE)

            decision = self.get_decision()

            if decision == Decision.FOLLOW_LINE:
                from .follow_line import FollowLine
                self.machine.set_state(FollowLine(self.machine))

        except CommandExecutionError as e:
            self.machine.set_state(Error(self.machine))

    def get_decision(self):
        """
        Placeholder for real decision-making logic.
        Replace this with actual sensor input, AI processing, or UART responses.
        """
        return Decision.FOLLOW_LINE