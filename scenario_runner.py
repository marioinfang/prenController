import time
import logging
from state_machine.state_machine import StateMachine
from state_machine.types.decision_state import Decision

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_scenario(decisions):
    """Runs a scenario with a predefined list of decisions."""
    state_machine = StateMachine()

    logging.info("Starting scenario execution...")

    for i, decision in enumerate(decisions):
        logging.info(f"Step {i+1}: Current State = {state_machine.state.__class__.__name__}")

        # Override decision logic in the current state
        state_machine.state.get_decision = lambda: decision

        # Execute the state logic
        state_machine.change()
        time.sleep(1)  # Simulate real-time execution

    logging.info("Scenario execution completed.")

# Define a basic scenario (Idle -> Start -> FollowLine -> WaypointDetected -> WaypointReached -> FollowLine -> ObstacleDetected)
scenario_1 = [
    Decision.START,               # Idle -> Start
    Decision.FOLLOW_LINE,         # Start -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
    Decision.FOLLOW_LINE,         # WaypointReached -> FollowLine
    Decision.FINISH_LINE_REACHED
]

scenario_2 = [
    Decision.START,               # Idle -> Start
    Decision.FOLLOW_LINE,         # Start -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
    Decision.FOLLOW_LINE,         # WaypointReached -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
    Decision.FOLLOW_LINE,         # WaypointReached -> FollowLine
    Decision.WAYPOINT_DETECTED,   # FollowLine -> WaypointDetected
    Decision.WAYPOINT_REACHED,    # WaypointDetected -> WaypointReached
    Decision.FOLLOW_LINE,         # WaypointReached -> FollowLine
    Decision.BARRIER_DETECTED
]

if __name__ == "__main__":
    run_scenario(scenario_2)