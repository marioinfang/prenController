from detection.yolo_detector import YoloDetector

class PathAnalyzer:
    TOLERANCE = 50; # Deviation in pixel with which the pylon must be centered

    def __init__(self, model_path):
        self.yolo_detector = YoloDetector(model_path)

    def is_path_clear(self, img) -> bool:
        is_path_clear = True
        results = self.yolo_detector.detect_objects(img)

        for result in results:
            for box in result.boxes:
                box_coordinates = box.xyxy[0]  # Coordinates of Bounding Box (x1, y1, x2, y2)
                conf = box.conf[0]  # Confidence value
                object_class_id = int(box.cls[0])  # Id of object class
                
                print(f"{self.yolo_detector.object_names[object_class_id]} erkannt an Position: ({box_coordinates}) mit Wahrscheinlichkeit: {conf}")

                if self.yolo_detector.object_names[object_class_id] == 'cone':
                    if self._is_object_centered_x_axis(box_coordinates, img):
                        print('Cone is in Middle')
                        return_value = False
                    else:
                        print('Cone is NOT in Middle')

        return return_value
        
    def analyze_path(self, img):
        object_distances = {}
        is_cone_on_path = False
        is_barrier_on_path = False

        results = self.yolo_detector.detect_objects(img)

        for result in results:
            for box in result.boxes:
                box_coordinates = box.xyxy[0]  # Coordinates of Bounding Box (x1, y1, x2, y2)
                conf = box.conf[0]  # Confidence value
                object_class_name = self.yolo_detector.object_names[int(box.cls[0])]  # name of object class
                
                print(f"{object_class_name} erkannt an Position: ({box_coordinates}) mit Wahrscheinlichkeit: {conf}")

                if object_class_name == 'cone':
                    if self._is_object_centered_x_axis(box_coordinates, img):
                        print('Cone is on path')
                        is_cone_on_path = True
                        object_distances[object_class_name] = self._get_distance_to_object(box_coordinates, img)
                    else:
                        print('Cone is NOT on path')
                elif object_class_name == 'barrier':
                    if self._is_object_centered_x_axis(box_coordinates, img):
                        print('Barrier is on path')
                        is_barrier_on_path = True
                        object_distances[object_class_name] = self._get_distance_to_object(box_coordinates, img)
                    else:
                        print('Barrier is NOT on path')

        return is_cone_on_path, is_barrier_on_path, object_distances
        
    def _is_object_centered_x_axis(self, box_coordinates, img) -> bool:      
        # calculate center on the X axis of the object
        x1, _, x2, _ = map(int, box_coordinates)
        object_center_x = (x1 + x2) / 2

        # calculate center on the X axis of the image
        _, width, _ = img.shape
        image_center_x = width / 2

        if abs(object_center_x - image_center_x) < self.TOLERANCE:
            return True
        else:
            return False
    
    def _get_distance_to_object(self, box_coordinates, img) -> int:
        # select coorinates of the object
        _, y1, _, y2 = map(int, box_coordinates)
        print(f"y1: {y1}")
        print(f"y2: {y2}")

        # select img height
        height, _, _ = img.shape

        # calculate distance to object
        return height - y2


