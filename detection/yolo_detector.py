from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="model/best.onnx"):
        self.model = YOLO(model_path)
        self.object_names = self.model.names
    
    def detect_objects(self, img):
        """ Scann image with model """
        return self.model(img)