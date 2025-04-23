import time
from detection.detection_service import DetectionService
from utils.log_config import get_logger

logger = get_logger(__name__)

SAFE_DISTANCES = {
    "cone": 100,
    "barrier": 30,
    "waypoint": 30
}

OBJECT_STATES = {
    "cone": "ConeDetected",
    "barrier": "BarrierDetected",
    "waypoint": "WaypointDetected"
}

def main():
    logger.info("=== TESTING: FollowLine Behavior (SIMULATED) ===")
    
    detection_service = DetectionService()
    drive_distance = 100

    try:
        while True:
            time.sleep(0.5)

            # Simulate driving (no real command)
            logger.info(f"Would send drive command: drive(state=FOLLOW_LINE, blocked=False, distance={drive_distance})")

            # Detect object in path
            detection_service.capture_and_detect()
            obj = detection_service.get_object_in_path()

            if obj:
                logger.info(f"Detected object in path: {obj}")
                distance = obj["distance_from_bottom"]
                name = obj["name"]

                safe_distance = SAFE_DISTANCES.get(name, 100)

                if distance <= safe_distance:
                    logger.info(f"Would send STOP due to {name} at distance {distance}px")
                    next_state = OBJECT_STATES.get(name, "Unknown")
                    logger.info(f"Would transition to state: {next_state}")
                    break  # End simulation after stop
            else:
                logger.info("No relevant object detected in path")

    except KeyboardInterrupt:
        logger.info("Manual test interrupted by user.")

if __name__ == "__main__":
    main()
