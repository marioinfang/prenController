import cv2

from picamera2 import Picamera2
from utils.log_config import get_logger

logger = get_logger(__name__)

class PiCamera:
    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
        self.camera.start()
    
    def take_picture(self):
        raw_img = self.camera.capture_array() # take picture
        logger.info("Took image")

        img = cv2.rotate(raw_img, cv2.ROTATE_180)
        
        # rezie picture to trained model size
        img = cv2.resize(img, (640, 640), interpolation=cv2.INTER_LINEAR)

        # convertion from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return img

