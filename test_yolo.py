from libcamera import controls, encoders, Frame, Pipeline, preview
import cv2
import numpy as np

# ... (YOLO-Modell initialisieren) ...

pipeline = Pipeline()
camera = pipeline.add_camera()

# Konfiguration der Kamera (Auflösung, Framerate, etc.)
camera.controls.ExposureTime = 10000  # Beispiel
camera.controls.AnalogueGain = 1.0  # Beispiel

# Encoder erstellen (für die Verarbeitung der Frames)
encoder = encoders.JpegEncoder()
pipeline.add_encoder(encoder)

# Pipeline starten
pipeline.start()

try:
    while True:
        # Frame erfassen
        frame = pipeline.wait_frame()

        # Frame in ein Numpy-Array konvertieren (Beispiel)
        image = np.array(frame.array).reshape((frame.height, frame.width, 3))

        # Bildverarbeitung mit YOLO
        path_clear = path_analyzer.is_path_clear(image)

        # ... (Ergebnisse ausgeben) ...

except KeyboardInterrupt:
    print("Schleife beendet")

finally:
    pipeline.stop()
    pipeline.close()