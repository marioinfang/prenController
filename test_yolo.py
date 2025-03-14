from picamera2 import Picamera2
from detection.path_analyzer import PathAnalyzer
from detection.pi_camera import PiCamera
from datetime import datetime
import cv2
import numpy as np
import os

# YOLO-Modell initialisieren
path_analyzer = PathAnalyzer('detection/model/best.onnx')
cam = PiCamera()

# Konfiguration der Kamera (Auflösung, Framerate, etc.)
config = cam.create_still_configuration(main={"size": (640, 480)}) # Beispielauflösung
cam.configure(config)

cam.start()

try:
    while True:
        # Frame erfassen
        array = cam.capture_array()

        resized = cv2.resize(array, (640, 640), interpolation=cv2.INTER_LINEAR)

        # Farbraumkonvertierung von BGR nach RGB
        rgb_array = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        # Bild speichern tests
        #timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #file_path = os.path.join('/home/minfang/Car/imgArchive', f"capture_{timestamp}.jpg")
        #cv2.imwrite(file_path, rgb_array)

        # Bildverarbeitung mit YOLO
        cone_on_path, barrier_on_path, distances = path_analyzer.analyze_path(rgb_array)

        # ... (Ergebnisse ausgeben) ...
        if (cone_on_path):
            print("Search other path")
        else:
            print("Take this path")

except KeyboardInterrupt:
    print("End loop")

finally:
    cam.stop()