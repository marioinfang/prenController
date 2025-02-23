from detection.path_analyzer import PathAnalyzer
from picamera import PiCamera
import time
import cv2
import numpy as np

# YOLO-Modell initialisieren
path_analyzer = PathAnalyzer('detection/model/best.onnx')

# Kamera initialisieren
camera = PiCamera()
camera.resolution = (640, 480)
camera.start_preview()
time.sleep(2)

try:
    while True:
        # Bild erfassen
        img = np.empty((480, 640, 3), dtype=np.uint8)
        camera.capture(img, 'bgr')

        # Objekterkennung durchführen
        path_clear = path_analyzer.is_path_clear(img)

        # Ergebnisse ausgeben
        if path_clear:
            print('Weg befahrbar')
        else:
            print('Weg NICHT befahrbar')

        # Optionale Pause (z.B. zur Steuerung der Framerate)
        time.sleep(0.1)  # Wartezeit in Sekunden

except KeyboardInterrupt:
    print('Schleife beendet')

finally:
    camera.stop_preview()
    camera.close()