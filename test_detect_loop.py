import time
import os
from detection.detection_service import DetectionService
from utils.log_config import get_logger
import cv2

logger = get_logger(__name__)

def main():
    logger.info("=== TESTING: Loop of 20 image captures with object detection and saving ===")
    
    detection_service = DetectionService()

    # Create folder for images
    output_dir = "captured_images"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, 21):  # Loop 20 times
        logger.info(f"Capturing image {i}/20...")
        
        img = detection_service.camera.take_picture()

        # Save image to file
        filename = os.path.join(output_dir, f"image_{i:02}.jpg")
        cv2.imwrite(filename, img)
        logger.info(f"Saved image to {filename}")

        # Run detection on image
        detection_service.detect_from_image(img)
        detected_objects = detection_service.get_detected_objects()

        if not detected_objects:
            logger.info(f"No objects detected in image {i}")
        else:
            logger.info(f"Detected {len(detected_objects)} objects in image {i}:")
            for obj in detected_objects:
                name = obj["name"]
                confidence = round(obj["confidence"] * 100, 1)
                box = obj["box"]
                logger.info(f"   - {name} ({confidence}%) at {box}")
        
        time.sleep(0.5)  # Short delay between captures

    logger.info("Finished 20 image detections.")

if __name__ == "__main__":
    main()
