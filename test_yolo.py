from detection.path_analyzer import PathAnalyzer
import cv2

path_analyzer = PathAnalyzer('detection/model/best.onnx')

cap = cv2.VideoCapture(0)  # Oder den Index deiner Kamera

if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden.")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kein Frame gelesen.")
            break

        path_clear = path_analyzer.is_path_clear(frame) # Übergabe des frames an die is_path_clear funktion

        if path_clear:
            print('Weg befahrbar')
        else:
            print('Weg NICHT befahrbar')

        # Optionale Anzeige des Bildes (zur Überprüfung)
        # cv2.imshow('Kamerabild', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'): # Mit 'q' beenden
        #     break

except KeyboardInterrupt:
    print("Schleife beendet")

finally:
    cap.release()
    cv2.destroyAllWindows()