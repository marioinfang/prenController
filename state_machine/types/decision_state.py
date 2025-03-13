from enum import Enum

class Decision(Enum):
    ERROR = 1
    IDLE = 2
    START = 3
    FOLLOW_LINE = 4
    WAYPOINT_DETECTED = 5
    BARRIER_DETECTED = 6
    CONE_DETECTED = 7
    WAYPOINT_REACHED = 8
    FINISH_LINE_REACHED = 9
