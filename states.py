from enum import Enum, auto

class State(Enum):
    INIT = auto()
    WEG_BEFAHREN = auto()
    WEGPUNKT_ANALYSIEREN = auto()
    WEGPUNKT_AUSRICHTEN = auto()
    ZIEL_IDENTIFIZIEREN = auto()
    HINDERNIS_ANHEBEN = auto()
    ERROR = auto()