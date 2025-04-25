import cv2

from detection.angle_service import AngleService
from utils.log_config import get_logger
from utils.raspberry_checker import is_raspberry_pi

logger = get_logger(__name__)

detector = AngleService() 

def run_detecor():
    angles = None
    if is_raspberry_pi():
        from camera.pi_camera import PiCamera
        camera = PiCamera()
        
        while True:
            img = camera.take_picture()
            try:
                angles = detector.get_angles_of_waypoint(img)
            except Exception as e:
                logger.error(f"No cyrcle detected! Error: {e}")
            
            logger.info(f"Detected angles: {angles}")

            input("Drücke Enter für die nächste Berechnung...")
    else:
        img = cv2.imread("C:/Users/minfang/Downloads/teeeeeeeest.png")

        try:
            angles = detector.get_angles_of_waypoint(img)
        except Exception:
            logger.error("No cyrcle detected!")

        logger.info(f"Detected angles: {angles}")

if __name__ == "__main__":
    run_detecor()