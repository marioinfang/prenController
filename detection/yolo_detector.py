from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="model/best.onnx"):
        self.model = YOLO("C:/Users/minfang/HSLU/PREN/prenController/detection/model/best.onnx")
        self.object_names = self.model.names
    
    def detect_objects(self, img):
        """ Scann image with model """
        return self.model(img)