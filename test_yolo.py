from picamera2 import Picamera2
from detection.path_analyzer import PathAnalyzer
import cv2
import numpy as np

# YOLO-Modell initialisieren
path_analyzer = PathAnalyzer('detection/model/best.onnx')

picam2 = Picamera2()

# Konfiguration der Kamera (Auflösung, Framerate, etc.)
config = picam2.create_still_configuration(main={"size": (640, 480)}) # Beispielauflösung
picam2.configure(config)

picam2.start()

try:
    while True:
        # Frame erfassen
        array = picam2.capture_array()

        resized = cv2.resize(array, (640, 640), interpolation=cv2.INTER_LINEAR)

        # Bildverarbeitung mit YOLO
        path_clear = path_analyzer.is_path_clear(resized)

        # ... (Ergebnisse ausgeben) ...
        if (path_clear):
            print("Weg befahren")
        else:
            print("Gesperrt")

except KeyboardInterrupt:
    print("Schleife beendet")

finally:
    picam2.stop()