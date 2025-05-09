from detection.yolo_detector import YoloDetector
# from camera.pi_camera import PiCamera

class DetectionService:
    def __init__(self, model_path="detection/model/best2.pt", use_camera=True):
        self.yolo_detector = YoloDetector(model_path)
        self.camera = None
        self.last_results = []

        if use_camera:
            try:
                from camera.pi_camera import PiCamera
                self.camera = PiCamera()
            except ImportError:
                print("Kamera-Modul konnte nicht geladen werden (wahrscheinlich kein Raspberry Pi).")


    def capture_and_detect(self):
        img = self.camera.take_picture()
        self.last_results = self.yolo_detector.detect_objects(img)
        return self.last_results

    def detect_from_image(self, img):
        self.last_results = self.yolo_detector.detect_objects(img)
        return self.last_results

    def get_detected_objects(self):
        detected_objects = []
        for result in self.last_results:
            for box in result.boxes:
                object_class_id = int(box.cls[0])
                object_name = self.yolo_detector.object_names[object_class_id]
                detected_objects.append({
                    "name": object_name,
                    "confidence": float(box.conf[0]),
                    "box": box.xyxy[0].tolist()
                })
        return detected_objects

    def get_object_in_path(self, image_width=640, x_tolerance=50):
        """
        Gibt das Objekt zurück, das sich auf der vertikalen Linie direkt vor dem Fahrzeug befindet.
        x_tolerance definiert, wie weit es seitlich von der Bildmitte (X-Achse) abweichen darf.
        Das Objekt mit der größten unteren Y-Koordinate (am nächsten zur Kamera) wird gewählt.
        """
        center_x = image_width // 2
        closest_obj = None
        max_y = -1 

        for result in self.last_results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                object_center_x = (x1 + x2) / 2

                if abs(object_center_x - center_x) <= x_tolerance:
                    if y2 > max_y:
                        max_y = y2
                        object_class_id = int(box.cls[0])
                        object_name = self.yolo_detector.object_names[object_class_id]
                        closest_obj = {
                            "name": object_name,
                            "confidence": float(box.conf[0]),
                            "box": box.xyxy[0].tolist(),
                            "distance_from_bottom": y2
                        }

        return closest_obj
