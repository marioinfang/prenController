from time import sleep

from utils.raspberry_checker import is_raspberry_pi

try:
    from picamera2 import Picamera2
    RASPBERRY_PI = True
except ImportError:
    RASPBERRY_PI = False

def capture_image():
    if RASPBERRY_PI and is_raspberry_pi():
        print("Running on Raspberry Pi - Using Pi Camera")
        picam2 = Picamera2()
        picam2.start()
        sleep(2)  # Give the camera time to adjust
        image_path = "/home/pi/captured_image.jpg"
        picam2.capture_file(image_path)
        picam2.stop()
    else:
        print("Running on Local Machine - Using Hardcoded Image")
        image_path = "../../images/test_image_c_flipped.jpeg"  # Use a local test image

    return image_path

import cv2
import easyocr

def process_image(image_path):
    reader = easyocr.Reader(['en'])

    valid_letters = {"A", "B", "C"}

    image = cv2.imread(image_path)

    # OCR on original image
    result_original = reader.readtext(image, detail=0)
    detected_original = [text.strip().upper() for text in result_original if text.strip().upper() in valid_letters]

    # OCR on flipped image
    flipped = cv2.rotate(image, cv2.ROTATE_180)
    result_flipped = reader.readtext(flipped, detail=0)
    detected_flipped = [text.strip().upper() for text in result_flipped if text.strip().upper() in valid_letters]

    # Decide which result to use
    if detected_original:
        print("Detected from original orientation:", detected_original)
        return detected_original[0]  # Return first valid letter
    elif detected_flipped:
        print("Detected from flipped orientation:", detected_flipped)
        return detected_flipped[0]
    else:
        print("No valid letter (A, B, or C) detected.")
        return None

if __name__ == "__main__":
    img_path = capture_image()
    extracted_text = process_image(img_path)
    print("Extracted Text:", extracted_text)