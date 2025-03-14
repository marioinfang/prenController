from picamera2 import Picamera2
import cv2

class PiCamera:
    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.picam2.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
        self.camera.start()
    
    def take_picture(self):
        # take picture
        raw_img = self.camera.capture_array()
        print("took image")

        # rezie picture to trained model size
        resized_img = cv2.resize(raw_img, (640, 640), interpolation=cv2.INTER_LINEAR)

        # convertion from BGR to RGB
        img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        return img

