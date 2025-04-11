from detection.path_analyzer import PathAnalyzer
from camera.pi_camera import PiCamera
import cv2

# YOLO-Modell initialisieren
path_analyzer = PathAnalyzer('detection/model/best.onnx')
cam = PiCamera()

try:
    while True:
        img = cam.take_picture()

        cone_on_path, barrier_on_path, distances = path_analyzer.analyze_path(img)

        if (cone_on_path):
            print("Search other path")
        else:
            print("Take this path")

except KeyboardInterrupt:
    print("End loop")
