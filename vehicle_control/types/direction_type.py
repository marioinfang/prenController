from enum import Enum

class DirectionType(Enum):
    LEFT = 0
    RIGHT = 1

def get_direction_type(value: int) -> DirectionType:
    try:
        return DirectionType(value)
    except ValueError:
        raise ValueError(f"Invalid direction type: {value}")