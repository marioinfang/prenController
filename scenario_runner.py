import time
from state_machine.state_machine import StateMachine
from state_machine.types.decision_state import Decision
from utils.log_config import get_logger

logger = get_logger(__name__)

def run_scenario(decisions):
    """Runs a scenario with a predefined list of decisions."""
    state_machine = StateMachine()

    logger.info("Starting scenario execution...")

    for i, decision in enumerate(decisions):
        logger.info(f"Step {i+1}: Current State = {state_machine.state.__class__.__name__}")

        # Override decision logic in the current state
        state_machine.state.get_decision = lambda: decision


        state_machine.change()
        time.sleep(1)

    logger.info("Scenario execution completed.")

scenario_1 = [
    Decision.START,
    Decision.FOLLOW_LINE,
    Decision.WAYPOINT_DETECTED,
    (Decision.WAYPOINT_REACHED, [0, 90, 180, 270]),
    Decision.FOLLOW_LINE,
    Decision.WAYPOINT_DETECTED,
    (Decision.WAYPOINT_REACHED, [0, 90, 180, 270]),
    Decision.FOLLOW_LINE,
    Decision.WAYPOINT_DETECTED,
    (Decision.WAYPOINT_REACHED, [0, 90, 180, 270]),
    Decision.FOLLOW_LINE,
    Decision.FINISH_LINE_REACHED
]

if __name__ == "__main__":
    run_scenario(scenario_1)