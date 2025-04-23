import cv2
import os
from detection.detection_service import DetectionService

# Kontrast & Helligkeit verbessern
def enhance_contrast_brightness(image, alpha=1, beta=15):
    """
    Erhöht Kontrast (alpha) und Helligkeit (beta)
    alpha > 1 = mehr Kontrast
    beta > 0 = heller
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# Bounding Boxes zeichnen
def draw_boxes(image, objects):
    for obj in objects:
        x1, y1, x2, y2 = map(int, obj["box"])
        label = f'{obj["name"]} ({obj["confidence"]*100:.1f}%)'
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(image, (x1, y1 - th - 4), (x1 + tw, y1), (0, 255, 0), -1)
        cv2.putText(image, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return image

def main():
    image_path = "testbild3.jpg"  # Dein Bild
    output_path = "erkannt_verbessert.jpg"

    detection_service = DetectionService(use_camera=False)

    if not os.path.exists(image_path):
        print(f"Bild nicht gefunden: {image_path}")
        return

    # Bild laden & verbessern
    image = cv2.imread(image_path)
    image = enhance_contrast_brightness(image, alpha=1.5, beta=40)

    # Objekte erkennen
    detection_service.detect_from_image(image)
    detected_objects = detection_service.get_detected_objects()

    # Ergebnis anzeigen
    if not detected_objects:
        print("Keine Objekte erkannt.")
    else:
        print(f"{len(detected_objects)} Objekte erkannt:")
        for obj in detected_objects:
            name = obj["name"]
            conf = round(obj["confidence"] * 100, 1)
            box = obj["box"]
            print(f" - {name} ({conf}%) bei {box}")

        # Bild mit Boxes speichern
        image_with_boxes = draw_boxes(image, detected_objects)
        cv2.imwrite(output_path, image_with_boxes)
        print(f"Verbessertes Bild gespeichert als: {output_path}")

if __name__ == "__main__":
    main()
