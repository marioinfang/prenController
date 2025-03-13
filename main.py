import time

from state_machine.state_machine import StateMachine
from utils.log_config import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    current_state = StateMachine()

    "To do real state change logic"

    logger.info("Starting state machine execution...")
    for i in range(10):
        logger.info(f"Cycle {i + 1}/20: Current State = {current_state.state.__class__.__name__}")
        current_state.change()
        time.sleep(1)

    logger.info("State machine execution completed.")
