from .base_state import BaseState
from .decision_state import Decision

from detection.path_analyzer import PathAnalyzer
from camera.pi_camera import PiCamera

class AnalyzePath(BaseState):
    def __init__(self, machine):
        self.machine = machine

    def context(self):
        print("State: AnalyzePath")

        # inizialation
        path_analyzer = PathAnalyzer('detection/model/best.onnx')
        camera = PiCamera()

        # take image
        img = camera.take_picture()

        # analyze image
        cone_on_path, barrier_on_path, distances = path_analyzer.analyze_path(img)

        if cone_on_path:
            decision = None
        else:
            decision = Decision.FOLLOW_LINE

        if decision == Decision.FOLLOW_LINE:
            from .follow_line import FollowLine
            self.machine.set_state(FollowLine(self.machine))
        else:
            from .error import Error
            self.machine.set_state(Error(self.machine))