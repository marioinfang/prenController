from detection.path_analyzer import PathAnalyzer
import cv2

# YOLO-Modell initialisieren
path_analyzer = PathAnalyzer('detection/model/best.onnx')

# Bild laden (Beispielbild)
img_path = "../images/T4.jpg"  # Pfad zu deinem Testbild
img = cv2.imread(img_path)

# Falls Bild nicht geladen werden konnte
if img is None:
    print("Fehler: Bild konnte nicht geladen werden.")
    exit()

# Objekterkennung durchführen
path_clear = path_analyzer.is_path_clear(img)

# Ergebnisse ausgeben
if path_clear:
    print('Weg befahrbar')
else:
    print('Weg NICHT befahrbar')