from audio.audio_player import play_target_reached
from utils.log_config import get_logger
from .base_state import BaseState

logger = get_logger(__name__)


class FinishLineReached(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        logger.info("Entered State: FinishLineReached")
        play_target_reached()
        "missing logic"
