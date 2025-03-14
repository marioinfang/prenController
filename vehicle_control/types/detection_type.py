from enum import Enum

class StopTypes(Enum):
    WAYPOINT = 1
    CONE = 2
    OBSTACLE = 3
    PATH = 4

def get_stop_type(value: int) -> StopTypes:
    try:
        return StopTypes(value)
    except ValueError:
        raise ValueError(f"Invalid stop type: {value}")