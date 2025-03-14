from detection.path_analyzer import PathAnalyzer
from detection.pi_camera import PiCamera

# YOLO-Modell initialisieren
path_analyzer = PathAnalyzer('detection/model/cleaned_best.onnx')
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