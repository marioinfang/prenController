from detection.yolo_detector import YoloDetector
from detection.pi_camera import PiCamera

class DetectionService:
    def __init__(self, model_path="detection/model/best.onnx"):
        self.yolo_detector = YoloDetector(model_path)
        self.camera = PiCamera()
        self.last_results = []

    def capture_and_detect(self):
        img = self.camera.take_picture()
        self.last_results = self.yolo_detector.detect_objects(img)
        return self.last_results, img

    # Returns the last detected objects as a list of dictionaries
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

    def is_object_detected(self, object_name):
        return any(obj["name"] == object_name for obj in self.get_detected_objects())

    def get_distance_to_nearest_object(self, object_name=None):
        min_distance = float("inf")
        closest_object = None

        for obj in self.get_detected_objects():
            if object_name is None or obj["name"] == object_name:
                distance = self._get_distance_to_object(obj["box"])
                if distance < min_distance:
                    min_distance = distance
                    closest_object = obj["name"]

        return min_distance if min_distance != float("inf") else -1, closest_object

    def _get_distance_to_object(self, box_coordinates):
        _, y1, _, y2 = map(int, box_coordinates)
        return y2
