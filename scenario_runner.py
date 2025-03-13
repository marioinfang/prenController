import time
import logging
from state_machine.state_machine import StateMachine
from state_machine.types.decision_state import Decision
from utils.log_config import get_logger

# Initialize logging
logger = get_logger(__name__)

def run_scenario(decisions):
    state_machine = StateMachine()

    logging.info("Starting scenario execution...")

    for i, decision in enumerate(decisions):
        logging.info(f"Step {i+1}: Current State = {state_machine.state.__class__.__name__}")

        state_machine.state.get_decision = lambda: decision

        state_machine.change()
        time.sleep(1)

    logging.info("Scenario execution completed.")

scenario_1 = [
    Decision.START,               # Idle -> Start
    Decision.FOLLOW_LINE,         # Start -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
    Decision.FOLLOW_LINE,         # WaypointReached -> FollowLine
    Decision.BARRIER_DETECTED,   # FollowLine -> ObstacleDetected
]

scenario_2 = [
    Decision.START,               # Idle -> Start
    Decision.FOLLOW_LINE,         # Start -> FollowLine
    Decision.CONE_DETECTED,       # FollowLine -> ConeDetected
    Decision.FOLLOW_LINE,         # ConeDetected -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
]

scenario_3 = [
    Decision.START,               # Idle -> Start
    Decision.FOLLOW_LINE,         # Start -> FollowLine
    Decision.BARRIER_DETECTED,   # FollowLine -> ObstacleDetected
    Decision.FOLLOW_LINE,         # ObstacleDetected -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
    Decision.FOLLOW_LINE,         # ObstacleDetected -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
    Decision.CONE_DETECTED
]

if __name__ == "__main__":
    run_scenario(scenario_1)