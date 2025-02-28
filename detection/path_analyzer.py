from detection.yolo_detector import YoloDetector

class PathAnalyzer:
    def __init__(self, model_path):
        self.yolo_detector = YoloDetector(model_path)
        self.object_names = self.yolo_detector.model.names
        print(self.object_names)

    def is_path_clear(self, img):
        return_value = True
        results = self.yolo_detector.detect_objects(img)

        for result in results:
            boxes = result.boxes  # Bounding Boxes
            for box in boxes:
                xyxy = box.xyxy[0]  # Koordinaten der Bounding Box (x1, y1, x2, y2)
                conf = box.conf[0]  # Konfidenzwert
                cls = box.cls[0]  # Klassenbezeichnung
                
                print(f"{self.object_names[int(cls)]} erkannt an Position: ({xyxy}) mit Wahrscheinlichkeit: {conf}")

                if self.object_names[int(cls)] == 'cone':
                    # Position des Objekts extrahieren
                    x1, y1, x2, y2 = map(int, xyxy)

                    # Mittelpunkt des Objekts berechnen
                    center_x = (x1 + x2) / 2

                    # Mittelpunkt des Bildes berechnen
                    height, width, _ = img.shape
                    image_center_x = width / 2

                    # Toleranzbereich definieren
                    tolerance = 50  # Pixel

                    if abs(center_x - image_center_x) < tolerance:
                        print('Cone is in Middle')
                        return_value = False
                    else:
                        print('Cone is NOT in Middle')

            return return_value
